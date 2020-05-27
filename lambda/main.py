#!/usr/bin/env python
import datetime
import json
import logging
import os
from dataclasses import dataclass
from typing import Tuple

import boto3
import botocore

DB_IDENTIFIER: str = os.getenv("DB_IDENTIFIER")
DB_NAME: str = os.getenv("DB_NAME")
BUCKET_NAME: str = os.getenv("BUCKET_NAME")
CONFIG_FILE: str = f"{DB_IDENTIFIER}.backup_config"

logging.getLogger().setLevel(logging.INFO)


def create_session() -> Tuple[
    'boto3.resource.factory.rds.Instance',
    'boto3.resource.factory.s3.Instance'
]:
    rds = boto3.client("rds")
    s3 = boto3.client("s3")

    return rds, s3


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


@dataclass
class Executor:
    """Class responsible for the backup of the logs"""

    rds_client: 'boto3.resource.factory.rds.Instance'
    s3_instance: S3
    file_name: str = ''
    copied_file_count: int = 0

    def run(self):
        """loop the logs and save on s3"""
        last_line_run = ""
        copied_file_count = 0
        last_written_this_run = 0
        log_marker = ""
        more_logs_remaining = True
        last_written_time = self.s3_instance.last_written_time
        backup_start_time = datetime.datetime.now()

        while more_logs_remaining:
            db_logs = self.rds_client.describe_db_log_files(
                DBInstanceIdentifier=DB_IDENTIFIER,
                FileLastWritten=last_written_time,
                FilenameContains='audit',
                Marker=log_marker)

            if not db_logs['DescribeDBLogFiles']:
                logging.info("Empty LogFiles")
                return

            if 'Marker' in db_logs and db_logs['Marker'] != "":
                log_marker = db_logs['Marker']
            else:
                more_logs_remaining = False

            # copy logs
            for db_log in db_logs['DescribeDBLogFiles']:
                if db_log['LastWritten'] == last_written_time:
                    continue
                logging.info(f"FileNumber: {copied_file_count + 1}")
                logging.info(
                    f"Downloading log file: {db_log['LogFileName']} "
                    f"found and with LastWritten value of: "
                    f"{db_log['LastWritten']} "
                )
                if int(db_log['LastWritten']) > last_written_this_run:
                    last_written_this_run = int(db_log['LastWritten'])

                # download the log file
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
                    continue

                log_file_data_cleaned = log_file_data.encode(errors='ignore')

                # upload the log file to S3
                file_name = db_log['LogFileName'].split("/")[1]
                object_name = (
                    f"{file_name}_backup_{backup_start_time.isoformat()}.log"
                )
                file_list = log_file_data_cleaned.decode().strip().split("\n")
                last_line_run = file_list[-1]

                if self.s3_instance.last_written_line:

                    last_idx = file_list.index(
                        self.s3_instance.last_written_line
                    ) + 1
                    file_to_save = str("\n".join(file_list[last_idx:])).encode()
                else:
                    file_to_save = str("\n".join(file_list)).encode()
                try:
                    self.s3_instance.client.put_object(
                        Bucket=BUCKET_NAME,
                        Key=object_name,
                        Body=file_to_save
                    )
                    copied_file_count += 1
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
        logging.info(f"Copied {copied_file_count} file(s) to s3")
        self.copied_file_count = copied_file_count

        # Update the last written time in the config
        if last_written_this_run > 0:
            logging.info("Update last writen time")
            config = json.dumps([last_line_run, last_written_this_run])
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

        logging.info("Log file export complete")


def lambda_handler(event, context):
    """Lambda handler"""

    rds_client, s3_client = create_session()
    s3_instance = S3(client=s3_client)
    s3_is_not_available = s3_instance.is_not_available()

    if s3_is_not_available:
        logging.error("S3 is not available")
        return {"Error": s3_is_not_available}
    s3_instance.get_last_written_time()
    executor = Executor(rds_client=rds_client, s3_instance=s3_instance)
    executor.run()
    return {
        "file_output": executor.file_name,
        "copied_file_count": executor.copied_file_count
    }


if __name__ == '__main__':
    event, context = [], []
    lambda_handler(event, context)
