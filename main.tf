provider "aws" {
  region  = "${var.region}"
  version = "~> 2.7"
//  profile = "brrafs"
}

resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_lambda_function" "test_lambda" {
  filename      = "main.zip"
  function_name = "teste"
  role          = "${aws_iam_role.iam_for_lambda.arn}"
  handler       = "main.py"

  source_code_hash = "${filebase64sha256("main.zip")}"

  runtime = "python3.7"

  environment {
    variables = {
      foo = "dev"
    }
  }
}