variable "lambda_function_name" {
  default = "log_watcher"
}

variable "lambda_filename" {
  default = "main.zip"
}

variable "lambda_handler" {
  default = "main.lambda_handler"
}

variable "AWS_PROFILE" {
  default = "acorsi"
}

variable "bucket_name" {
  default = "log-watcher"
}

variable "db_name" {
  default = "defaultDB"
}

variable "db_user_name" {
  default = "admin"
}

variable "db_user_password" {
  default = "1a2b3c4d5!"
}

variable "db_engine" {
  default = "mysql"
}