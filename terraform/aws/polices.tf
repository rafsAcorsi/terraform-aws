resource "aws_iam_role" "lambda_role" {
  name = "${var.app_name}-lambda-role-${local.exp_env}"

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

data "aws_iam_policy_document" "rds_create_db" {
  statement {
    effect = "Allow"
    actions = [
      "logs:*",
      "s3:*",
      "rds:*"
    ]
    resources = ["*"]
  }
}


resource "aws_iam_role_policy" "lambda_policy" {
  name = "${var.app_name}-lambda-policy-${local.exp_env}"

  role = aws_iam_role.lambda_role.id

  policy = data.aws_iam_policy_document.rds_create_db.json
}
