"""Scripts for Makefile"""
import argparse
import os
import subprocess
from functools import partial

SECURITY_PATH = "terraform/aws/security.tfvars"
AWS_PROFILE = os.getenv("AWS_PROFILE")
DB_NAME = os.getenv("DB_NAME")
DB_USER_NAME = os.getenv("DB_USER_NAME")
DB_USER_PASSWORD = os.getenv("DB_USER_PASSWORD")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")


def check_env_variables():
    if not all([
        AWS_PROFILE, DB_NAME, DB_USER_NAME, DB_USER_PASSWORD, AWS_BUCKET_NAME
    ]):
        print(
            "\n\nPlease export env variables, check README.md on root path\n\n"
        )
        return False
    return True


def check_security_vars(func):
    """Decorator for check security vars"""

    def wrapper(*args):
        if not security_vars_exists():
            create_security_vars()
        if not check_env_variables():
            return
        func(*args)

    return wrapper


@check_security_vars
def terraform_apply(env=None):
    """Terraform Apply check security first"""
    workspace = subprocess.run(
        ["terraform", "workspace", "list"],
        capture_output=True
    )
    command = "new"
    if env in workspace.stdout.decode():
        command = "select"

    subprocess.call(["terraform", "workspace", command, env])

    subprocess.call([
        "terraform",
        "apply",
        "-var-file=terraform/aws/security.tfvars",
        "terraform/aws"
    ])


terraform_apply_dev = partial(terraform_apply, "dev")
terraform_apply_prod = partial(terraform_apply, "prod")


def security_vars_exists():
    """Check if security vars exists"""
    return os.path.exists(SECURITY_PATH)


def create_security_vars():
    template = """
aws_profile         = "{0}"
db_name             = "{1}"
db_user_name        = "{2}"
db_user_password    = "{3}"
bucket_name         = "{4}" """.format(
        AWS_PROFILE, DB_NAME, DB_USER_NAME, DB_USER_PASSWORD, AWS_BUCKET_NAME
    ).lstrip()
    with open(SECURITY_PATH, "w+") as file:
        file.write(template)


@check_security_vars
def terraform_destroy():
    """Terraform destroy check security first"""
    return subprocess.call([
        "terraform",
        "destroy",
        "-var-file=terraform/aws/security.tfvars",
        "terraform/aws"
    ])


@check_security_vars
def terraform_init():
    """Terraform destroy check security first"""
    return subprocess.call([
        "terraform",
        "init",
        "terraform/aws"
    ])


@check_security_vars
def lambda_invoke():
    workspace = subprocess.run([
        "terraform",
        "workspace",
        "show"
    ], capture_output=True)
    workspace = workspace.stdout.decode().strip()

    lambda_name = "log-watcher-{}".format(workspace)

    return subprocess.call([
        'aws',
        'lambda',
        'invoke',
        '--function-name',
        lambda_name,
        '--profile',
        AWS_PROFILE,
        '--log-type',
        'Tail',
        'response.json'])


def run_test():
    import unittest
    from lambda_func.test import test_aws_api
    suite = unittest.TestLoader().loadTestsFromModule(test_aws_api)
    unittest.TextTestRunner().run(suite)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make script')
    parser_map = {
        'destroy': terraform_destroy,
        'init': terraform_init,
        'invoke': lambda_invoke,
        'prod': terraform_apply_prod,
        'dev': terraform_apply_dev,
        'test': run_test
    }

    parser.add_argument('command', choices=parser_map.keys())

    args = parser.parse_args()

    func_parsed = parser_map[args.command]
    func_parsed()
