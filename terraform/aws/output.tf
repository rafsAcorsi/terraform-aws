output my-env {
  value = local.exp_env
}

output aws-security-id {
  value = aws_security_group.default.id
}

output bucket-name {
  value = aws_s3_bucket.b.id
}

output db-name {
  value = aws_db_instance.db_default.name
}

output vpc_id {
  value = aws_vpc.default.id
}
