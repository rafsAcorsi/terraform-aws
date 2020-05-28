#!/usr/bin/env python
import logging

import boto3

from aws_api import S3, Executor

logging.getLogger().setLevel(logging.INFO)


def create_session():
    rds = boto3.client("rds")
    s3 = boto3.client("s3")

    return rds, s3


def lambda_handler(event, context):
    """Lambda handler"""

    rds_client, s3_client = create_session()
    s3_instance = S3(client=s3_client)
    s3_is_not_available = s3_instance.is_not_available()

    if s3_is_not_available:
        logging.error("S3 is not available")
        return {"Error": s3_is_not_available}
    s3_instance = s3_instance.get_last_written_time()
    executor = Executor(rds_client=rds_client, s3_instance=s3_instance)
    executor.run()
    return {
        "file_output": executor.file_name,
        "copied_file_count": executor.copied_file_count
    }


if __name__ == '__main__':
    event, context = [], []
    lambda_handler(event, context)
