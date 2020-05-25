provider "aws" {
  version = "~> 2.0"
  profile = var.aws_profile
  region = var.region
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnet_ids" "all" {
  vpc_id = data.aws_vpc.default.id
}

resource "aws_security_group" "default" {
  name = "${var.app_name}-${local.exp_env}"
  description = "SG for access RDS"

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

  tags = {
    Name = "RDS-CG"
  }
}
