#!/usr/bin/env python
import datetime
import os
import time
from typing import List, Dict, Final, Tuple

import boto3

DB_NAME: Final = os.getenv("DB_NAME")


def describe_logs_files(rds: boto3.client) -> List[Dict]:
    d_now = datetime.datetime.now()
    d_yesterday = d_now.replace(day=d_now.day - 1)
    d_to_posix = int(time.mktime(d_yesterday.timetuple()))

    response = rds.describe_db_log_files(
        DBInstanceIdentifier=DB_NAME,
        FileLastWritten=d_to_posix
    )
    return response['DescribeDBLogFiles']


def download_logs_file(rds: boto3.client, log_file: str) -> Tuple[str, bytes]:
    token = '0'
    response = rds.download_db_log_file_portion(
        DBInstanceIdentifier=DB_NAME,
        LogFileName=log_file,
        Marker=token
    )

    log_files_data = response['LogFileData']
    while response['AdditionalDataPending']:
        token = response['Marker']
        log_files_data += response['LogFileData']

        response = rds.download_db_log_file_portion(
            DBInstanceIdentifier=DB_NAME,
            LogFileName=log_file,
            Marker=token
        )
    result_log_file = str.encode(log_files_data)
    return log_file, result_log_file


def lambda_handler(event, context):
    print("Start process")
    session = boto3.Session(profile_name="default")
    rds = session.client("rds")
    s3 = session.client('s3')
    dnow = datetime.datetime.now()
    dstr = dnow.strftime('%Y-%m-%d %H:%M:%S')
    print(describe_logs_files(rds))

    log_file_list = describe_logs_files(rds)

    for i in log_file_list:
        logfilename, downloads = download_logs_file(rds, i['LogFileName'])
        s3.put_object(Bucket='log-watcher', Key='AWSRdsLogs/{}/'.format(dstr) + logfilename, Body=downloads)


if __name__ == '__main__':
    event, context = [], []
    lambda_handler(event, context)
