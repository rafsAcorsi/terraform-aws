variable "app_name" {
  default = "hot"
}

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
    default = "default"
    dev = "development"
    prod = "production"
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
        "0.0.0.0/32"]
    }
  }
}

variable "db_engine" {
  default = "mysql"
}

variable "db_version" {
  default = "5.7"
}

variable "map_public_ip_on_launch" {
  default = true
}

# Inside security.tfvars
variable "aws_profile" {}
variable "db_name" {}
variable "db_user_name" {}
variable "db_user_password" {}
variable "bucket_name" {}