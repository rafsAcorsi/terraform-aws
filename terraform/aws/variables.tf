variable "app_name" {
  default = "hot"
}

variable "lambda_function_name" {
  default = "log-watcher"
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

variable "zone" {
  default = "us-east-1a"
}

variable "env" {
  type = map(string)
  description = "Map for environment"
  default = {
    default = "default"
    dev = "dev"
    prod = "prod"
  }
}

locals {
  exp_env = lookup(var.env, terraform.workspace)
}

variable "cidr_default" {
  default = "10.10.10.0/24"
}

variable "default_ingress" {
  type = map(object({
    description = string,
    cidr_blocks = list(string)
  }))
  default = {
    3306 = {
      description = "Inbound for mysql",
      cidr_blocks = ["10.10.10.0/24"]
    }
  }
}

variable "db_engine" {
  default = "mysql"
}

variable "db_version" {
  default = "5.7"
}

# Inside security.tfvars
variable "aws_profile" {}
variable "db_name" {}
variable "db_user_name" {}
variable "db_user_password" {}
variable "bucket_name" {}