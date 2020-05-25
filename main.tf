provider "aws" {
  profile = var.AWS_PROFILE
  region = "us-east-1"
}

resource "aws_lambda_function" "log_watcher" {
  filename = var.lambda_filename
  function_name = var.lambda_function_name
  role = aws_iam_role.iam_for_lambda.arn
  handler = var.lambda_handler

  source_code_hash = filebase64sha256("main.zip")

  runtime = "python3.7"

  environment {
    variables = {
      env = "dev"
      bucket_name = var.bucket_name
    }
  }

  vpc_config {
    subnet_ids         = [module.vpc.database_subnet_group]
    security_group_ids = [aws_security_group.rds.id]
  }
}


resource "aws_s3_bucket" "b" {
  bucket = var.bucket_name
  acl = "public-read-write"

  tags = {
    Name = "Log Watcher"
    Environment = "Dev"
  }
}

resource "aws_db_instance" "db_default" {
  allocated_storage = 20
  engine = var.db_engine
  engine_version = "5.7"
  instance_class = "db.t2.micro"
  name = var.db_name
  username = var.db_user_name
  password = var.db_user_password
  skip_final_snapshot = "true"

  publicly_accessible = true
  db_subnet_group_name = module.vpc.database_subnets[0]
  vpc_security_group_ids = [
    aws_security_group.rds.id]
}
