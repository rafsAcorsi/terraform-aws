data "archive_file" "lambda_zip" {
  type = "zip"
  output_path = "lambda/main.zip"
  source_dir = "lambda"
}

resource "aws_lambda_function" "log_watcher" {
  filename = data.archive_file.lambda_zip.output_path
  function_name = var.lambda_function_name
  role = aws_iam_role.iam_for_lambda.arn
  handler = var.lambda_handler
  runtime = "python3.7"

  environment {
    variables = {
      env = local.exp_env
      bucket_name = var.bucket_name
    }
  }
}