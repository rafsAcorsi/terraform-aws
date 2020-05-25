resource "aws_s3_bucket" "b" {
  bucket = var.bucket_name
  acl = "public-read-write"
  force_destroy = "true"

  tags = {
    Name = "Log Watcher"
    Environment = "Dev"
  }
}