data "archive_file" "lambda_zip" {
  type = "zip"
  output_path = "main.zip"
  source_dir = "lambda"
}

resource "aws_lambda_function" "log_watcher" {
  filename = data.archive_file.lambda_zip.output_path
  function_name = "${var.lambda_function_name}-${local.exp_env}"
  role = aws_iam_role.lambda_role.arn
  handler = var.lambda_handler
  runtime = "python3.7"

  environment {
    variables = {
      ENV = local.exp_env
      BUCKET_NAME = "${var.bucket_name}-${local.exp_env}"
      DB_NAME = "${var.db_name}${local.exp_env}"
      DB_IDENTIFIER = "${var.db_name}-${local.exp_env}"
    }
  }
}