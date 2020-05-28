import json
import logging
import unittest
from unittest import mock

import botocore

from ..aws_api import S3, Executor


class TestS3API(unittest.TestCase):

    @mock.patch("boto3.client")
    def setUp(self, mock_client):
        logging.getLogger().setLevel(100)
        self.client = mock_client()
        self.s3 = S3(self.client)

    def test_bucket_is_valid(self):
        self.s3.is_not_available()
        self.client.head_bucket.assert_called_once()

    def test_bucket_is_invalid_404(self):
        error_response = {
            "ResponseMetadata": {"HTTPStatusCode": 404}
        }
        operation_name = "test"
        self.client.head_bucket = mock.MagicMock(
            side_effect=botocore.exceptions.ClientError(
                error_response=error_response,
                operation_name=operation_name
            )
        )
        error = self.s3.is_not_available()
        self.assertEqual(error, "Error: Bucket name provided not found")

    def test_bucket_is_invalid_unable_to_access(self):
        error_response = {
            "ResponseMetadata": {"HTTPStatusCode": 400},
            "Error": {"Message": "Test mock"}
        }
        operation_name = "test"
        self.client.head_bucket = mock.MagicMock(
            side_effect=botocore.exceptions.ClientError(
                error_response=error_response,
                operation_name=operation_name
            )
        )
        error = self.s3.is_not_available()
        error_msg = (
            f"Error: Unable to access bucket name, "
            f"error: Test mock"
        )
        self.assertEqual(error, error_msg)

    def test_get_last_written_time_success(self):
        class MockBody:
            def read(self, _):
                return json.dumps([100, 100])

        self.client.get_object.return_value = {
            "Body": MockBody(),
            "ContentLength": 100
        }
        self.s3.get_last_written_time()
        self.client.get_object.assert_called_once()


class TestExecutor(unittest.TestCase):

    @mock.patch("boto3.client")
    def setUp(self, mock_client):
        self.s3_client = mock_client()
        self.rds_client = mock_client()
        self.executor = Executor(
            s3_instance=self.s3_client,
            rds_client=self.rds_client
        )

    def test_run(self):
        self.rds_client.describe_db_log_files.return_value = {
            "DescribeDBLogFiles": [{
                "LogFileName": "test.log",
                "LastWritten": 8000,
            }],
            "LogFileName": "Test.log",

        }
        self.rds_client.download_db_log_file_portion.return_value = {
            "LogFileData": "",
            "LastWritten": 8000,
            "AdditionalDataPending": 0
        }
        self.executor.run()
        self.rds_client.describe_db_log_files.assert_called_once()
        self.rds_client.download_db_log_file_portion.assert_called_once()
        self.s3_client.client.put_object.assert_called_once()

