provider "aws" {
  version = "~> 2.0"
  profile = var.aws_profile
  region = var.region
}

resource "aws_vpc" "default" {
  cidr_block = "10.10.0.0/16"
  enable_dns_hostnames = true
}

resource "aws_subnet" "private" {
  cidr_block = var.cidr_default
  vpc_id = aws_vpc.default.id
  availability_zone = var.zone
}

resource "aws_security_group" "default" {
  name = "${var.app_name}-${local.exp_env}"
  description = "SG for access RDS"
  vpc_id = aws_vpc.default.id

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
}
