resource "aws_s3_bucket" "b" {
  bucket = var.bucket_name
  acl = "public-read-write"

  tags = {
    Name = "Log Watcher"
    Environment = "Dev"
  }
}