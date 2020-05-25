#!/usr/bin/env python
import json
import os
import sys
import boto3

base_path = os.path.dirname(__file__)
sys.path.append(base_path + "/lib")


def lambda_handler(event, context=None):
    bucket_name = os.getenv("bucket_name")

    encoded_string = json.dumps(event, indent=2).encode("utf-8")

    file_name = "teste.txt"
    s3_path = "1/" + file_name

    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)

    print("Received event: " + json.dumps(event, indent=2))


if __name__ == '__main__':
    pass
