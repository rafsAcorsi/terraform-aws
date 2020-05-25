resource "aws_security_group" "rds-cg" {
  name = "rds-cg-security_group"
  description = "SG for access RDS"

  dynamic "ingress" {
    for_each = var.default_ingress
    content {
      description = ingress.value["description"]
      from_port = ingress.key
      to_port = ingress.key
      protocol = "tcp"
      cidr_blocks = ingress.value["cidr_blocks"]
    }
  }

  tags = {
    Name = "RDS-CG"
  }
}

resource "aws_iam_policy" "policy" {
  name = "write_s3"


  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
      {
          "Effect": "Allow",
          "Action": [
              "logs:*"
          ],
          "Resource": "arn:aws:logs:*:*:*"
      },
      {
          "Effect": "Allow",
          "Action": [
              "s3:*"
          ],
          "Resource": "arn:aws:s3:::*"
      }
  ]
}
EOF
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

//
//#===================
//# old
//resource "aws_iam_policy" "policy" {
//  name = "write_s3"
//
//
//  policy = <<EOF
//{
//  "Version": "2012-10-17",
//  "Statement": [
//      {
//          "Effect": "Allow",
//          "Action": [
//              "logs:*"
//          ],
//          "Resource": "arn:aws:logs:*:*:*"
//      },
//      {
//          "Effect": "Allow",
//          "Action": [
//              "s3:*"
//          ],
//          "Resource": "arn:aws:s3:::*"
//      }
//  ]
//}
//EOF
//}
//
//resource "aws_iam_role" "iam_for_lambda" {
//  name = "iam_for_lambda"
//
//  assume_role_policy = <<EOF
//{
//  "Version": "2012-10-17",
//  "Statement": [
//    {
//      "Action": "sts:AssumeRole",
//      "Principal": {
//        "Service": "lambda.amazonaws.com"
//      },
//      "Effect": "Allow",
//      "Sid": ""
//    }
//  ]
//}
//EOF
//}
//
//
