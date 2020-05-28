#!/usr/bin/env python
import datetime
import json
import logging
import os
from dataclasses import dataclass

import boto3
import botocore

BUCKET_NAME = os.getenv("BUCKET_NAME")
DB_IDENTIFIER = os.getenv("DB_IDENTIFIER")
DB_NAME = os.getenv("DB_NAME")
CONFIG_FILE = f"{DB_IDENTIFIER}.backup_config"


@dataclass
class S3:
    client: 'boto3.resource.factory.s3.Instance'
    last_written_time: int = 0
    last_written_line: str = ''

    def is_not_available(self) -> str:
        """Check if bucket exists and is available"""
        error_msg = ''
        try:
            self.client.head_bucket(Bucket=BUCKET_NAME)
        except botocore.exceptions.ClientError as e:
            error_code = int(e.response['ResponseMetadata']['HTTPStatusCode'])
            if error_code == 404:
                error_msg = "Error: Bucket name provided not found"
            else:
                error_msg = (
                    f"Error: Unable to access bucket name, "
                    f"error: {e.response['Error']['Message']}"
                )
            logging.error([error_code, error_msg])
            return error_msg
        return error_msg

    def get_last_written_time(self):
        """Check if exists config file, and set last written time"""
        try:
            response = self.client.get_object(
                Bucket=BUCKET_NAME, Key=CONFIG_FILE
            )
            config = json.loads(
                response['Body'].read(response['ContentLength'])
            )
            self.last_written_time = int(config[1])
            self.last_written_line = config[0]
            logging.info(
                f"Found marker from last log download, "
                f"retrieving log files with "
                f"lastWritten time after %s {self.last_written_time}"
            )

        except botocore.exceptions.ClientError as e:
            error_code = int(e.response['ResponseMetadata']['HTTPStatusCode'])
            if error_code == 404:
                logging.info(
                    "It appears this is the first log import, all files "
                    "will be retrieved from RDS"
                )
            else:
                logging.error(
                    f"Error: Unable to access config file, "
                    f"error: {e.response['Error']['Message']}"
                )
        return self


@dataclass
class Executor:
    """Class responsible for the backup of the logs"""

    rds_client: 'boto3.resource.factory.rds.Instance'
    s3_instance: S3
    file_name: str = ''
    copied_file_count: int = 0
    last_line_run = ""
    last_written_this_run = 0
    log_marker = ""
    more_logs_remaining = True
    db_logs = None

    def run(self):
        """loop the logs and save on s3"""
        backup_start_time = datetime.datetime.now()

        while self.more_logs_remaining:
            self.download_all_log_files()
            # loop all files and save logs
            self.copy_logs(backup_start_time=backup_start_time)
        logging.info(f"Copied {self.copied_file_count} file(s) to s3")
        self.copied_file_count = self.copied_file_count

        # Update the last written time in the config
        if self.last_written_this_run > 0:
            self.update_config_file()

        logging.info("Log file export complete")

    def get_last_log_data(self, db_log):
        """Get last log data"""
        if db_log['LastWritten'] == self.s3_instance.last_written_time:
            return
        logging.info(f"FileNumber: {self.copied_file_count + 1}")
        logging.info(
            f"Downloading log file: {db_log['LogFileName']} "
            f"found and with LastWritten value of: "
            f"{db_log['LastWritten']} "
        )
        if int(db_log['LastWritten']) > self.last_written_this_run:
            self.last_written_this_run = int(db_log['LastWritten'])

        # download the log file
        log_file_data = self.download_log_file(db_log)
        return log_file_data

    def prepare_data_to_upload(self, db_log, backup_start_time, log_file_data):
        """Prepare data to upload"""

        log_file_data_cleaned = log_file_data.encode(errors='ignore')

        file_name = db_log['LogFileName'].split("/")[1]
        object_name = (
            f"{file_name}_backup_{backup_start_time.isoformat()}.log"
        )
        file_list = log_file_data_cleaned.decode().strip().split("\n")
        self.last_line_run = file_list[-1]

        if self.s3_instance.last_written_line:
            last_idx = file_list.index(
                self.s3_instance.last_written_line
            ) + 1
            file_to_save = str("\n".join(file_list[last_idx:])).encode()
        else:
            file_to_save = str("\n".join(file_list)).encode()

        return file_to_save, object_name

    def copy_logs(self, backup_start_time):
        """Loop all files, sanitize and save on S3 Bucket."""
        # copy logs
        for db_log in self.db_logs['DescribeDBLogFiles']:
            log_file_data = self.get_last_log_data(db_log)
            if not log_file_data:
                continue
            file_to_save, object_name = self.prepare_data_to_upload(
                db_log, backup_start_time, log_file_data
            )
            try:
                self.s3_instance.client.put_object(
                    Bucket=BUCKET_NAME,
                    Key=object_name,
                    Body=file_to_save
                )
                self.copied_file_count += 1
            except botocore.exceptions.ClientError as e:
                logging.error(
                    f"Error writing object to S3 bucket, "
                    f"S3 ClientError: {e.response['Error']['Message']}"
                )
                return

            logging.info(
                f"Uploaded log file {object_name} "
                f"to S3 bucket {BUCKET_NAME}"
            )
            self.file_name = object_name

    def download_all_log_files(self):
        """Download all log files, filter by audit type"""
        self.db_logs = self.rds_client.describe_db_log_files(
            DBInstanceIdentifier=DB_IDENTIFIER,
            FileLastWritten=self.s3_instance.last_written_time,
            FilenameContains='audit',
            Marker=self.log_marker)

        if not self.db_logs['DescribeDBLogFiles']:
            logging.info("Empty LogFiles")
            return

        if 'Marker' in self.db_logs and self.db_logs['Marker'] != "":
            self.log_marker = self.db_logs['Marker']
        else:
            self.more_logs_remaining = False

    def download_log_file(self, db_log):
        """Download specific log file """
        log_file_data = ""
        try:
            log_file = self.rds_client.download_db_log_file_portion(
                DBInstanceIdentifier=DB_IDENTIFIER,
                LogFileName=db_log['LogFileName'], Marker='0'
            )
            log_file_data = log_file['LogFileData']
            while log_file['AdditionalDataPending']:
                log_file = self.rds_client.download_db_log_file_portion(
                    DBInstanceIdentifier=DB_IDENTIFIER,
                    LogFileName=db_log['LogFileName'],
                    Marker=log_file['Marker'])
                log_file_data += log_file['LogFileData']
        except Exception as e:
            logging.error("File download failed: ", e)

        return log_file_data

    def update_config_file(self):
        """Update config file with last line and last timestamp"""
        logging.info("Update last writen time")
        config = json.dumps([
            self.last_line_run, self.last_written_this_run
        ])
        try:
            self.s3_instance.client.put_object(
                Bucket=BUCKET_NAME, Key=CONFIG_FILE,
                Body=str.encode(str(config))
            )
        except botocore.exceptions.ClientError as e:
            logging.error(
                f"Error writting the config to S3 bucket, "
                f"S3 ClientError: {e.response['Error']['Message']}"
            )
            return
        logging.info(
            f"Wrote new Last Written file to {CONFIG_FILE} "
            f"in Bucket {BUCKET_NAME}"
        )
