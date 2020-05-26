resource "aws_s3_bucket" "b" {
  bucket = "${var.bucket_name}-${local.exp_env}"
  acl = "private"
  force_destroy = "true"

  tags = {
    Name = "Log Watcher"
    Environment = local.exp_env
  }
}