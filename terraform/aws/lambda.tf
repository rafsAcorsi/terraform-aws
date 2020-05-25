resource "aws_lambda_function" "log_watcher" {
  filename = var.lambda_filename
  function_name = var.lambda_function_name
  role = aws_iam_role.iam_for_lambda.arn
  handler = var.lambda_handler

  source_code_hash = filebase64sha256("main.zip")

  runtime = "python3.7"

  environment {
    variables = {
      env = var.env
      bucket_name = var.bucket_name
    }
  }
}