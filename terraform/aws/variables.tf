variable "lambda_function_name" {
  default = "log_watcher"
}

variable "lambda_filename" {
  default = "main.zip"
}

variable "lambda_handler" {
  default = "main.lambda_handler"
}

variable "region" {
  default = "us-east-1"
}

variable env {
  type = map(string)
  description = "Map for environment"
  default = {
    default = "Default Env"
    dev = "Dev Env"
    prod = "Prod Env"
  }
}

locals {
  exp_env = lookup(var.env, terraform.workspace)
}

variable default_ingress {
  type = map(object({
    description = string,
    cidr_blocks = list(string)
  }))
  default = {
    3306 = {
      description = "Inbound for mysql",
      cidr_blocks = [
        "127.0.0.1/32"]
    }
  }
}


# Inside security.tfvars
variable "aws_profile" {}
variable "db_name" {}
variable "db_user_name" {}
variable "db_user_password" {}
variable "bucket_name" {}