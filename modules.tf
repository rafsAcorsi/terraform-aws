module "vpc"{
  source = "terraform-aws-modules/vpc/aws"
  name = "my-vpc"

  cidr = "10.0.0.0/16"

  azs = [
    "us-east-1a"]
  private_subnets = [
    "10.0.1.0/24"]
  database_subnets = [
    "10.0.11.0/24"]
  public_subnets = [
    "10.0.101.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true
  enable_dns_hostnames = true
}
