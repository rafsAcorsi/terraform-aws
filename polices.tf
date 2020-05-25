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


resource "aws_db_option_group" "db_options" {
  engine_name = var.db_engine
  major_engine_version = "5.7"
  name = "db-option"

  # Enable RDS audit for mysql
  option {
    option_name = "MARIADB_AUDIT_PLUGIN"

    option_settings {
      name = "SERVER_AUDIT_FILE_ROTATIONS"
      value = "15"
    }
  }
}

resource "aws_security_group" "rds" {
  name = "rds.myapp"
  vpc_id = module.vpc.vpc_id
  description = "Security group for RDS"

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = [
      "0.0.0.0/0"]
  }

  ingress {
    from_port = 3306
    to_port = 3306
    protocol = "tcp"
    cidr_blocks = [
      "0.0.0.0/0"]
  }
}