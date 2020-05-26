resource "aws_db_instance" "db_default" {
  identifier = "${var.db_name}-${local.exp_env}"
  allocated_storage = 20
  engine = var.db_engine
  engine_version = var.db_version
  instance_class = "db.t2.micro"
  name = "${var.db_name}${local.exp_env}"
  username = var.db_user_name
  password = var.db_user_password
  skip_final_snapshot = "true"
  publicly_accessible = true
  backup_retention_period = 0
  apply_immediately = true
  option_group_name = aws_db_option_group.db_options.name
  vpc_security_group_ids = [aws_security_group.default.id]

}

resource "aws_db_option_group" "db_options" {
  engine_name = var.db_engine
  major_engine_version = var.db_version
  name = "db-option"

  # Enable RDS audit for mysql
  option {
    option_name = "MARIADB_AUDIT_PLUGIN"

    option_settings {
      name = "SERVER_AUDIT_EVENTS"
      value = "CONNECT"
    }

    option_settings {
      name = "SERVER_AUDIT_FILE_ROTATIONS"
      value = "20"
    }

  }

}
