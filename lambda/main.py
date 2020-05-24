#!/usr/bin/env python
import json
import os
import sys

base_path = os.path.dirname(__file__)
sys.path.append(base_path + "/lib")


def response(status=200, headers={'Content-Type': 'application/json'}, body=''):
    if not body:
        return {'statusCode': status}
    return {
        'statusCode': status,
        'headers': headers,
        'body': json.dumps(body)
    }


def lambda_handler(event, context):
    print(event)
    return response(status=200)


if __name__ == '__main__':
    pass
