output my-env {
  value = local.exp_env
}

output rds-id {
  value = aws_security_group.rds-cg.id
}