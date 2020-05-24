#!/usr/bin/env python
import json
import os
import sys

base_path = os.path.dirname(__file__)
sys.path.append(base_path + "/lib")


def lambda_handler(event, context=None):
    print("Received event: " + json.dumps(event, indent=2))


if __name__ == '__main__':
    pass
