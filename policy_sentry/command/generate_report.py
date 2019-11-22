from pathlib import Path
import sys
import click
from policy_sentry.shared.download import download_remote_policies, download_policies_recursively
from policy_sentry.shared.login import get_list_of_aws_profiles
from policy_sentry.shared.analyze import analyze_policy_directory
from policy_sentry.shared.database import connect_db

HOME = str(Path.home())
DEFAULT_CREDENTIALS_FILE = HOME + '/.aws/credentials'
AUDIT_DIRECTORY_FOLDER = '/audit'
CONFIG_DIRECTORY = '/.policy_sentry/'
audit_directory_path = HOME + CONFIG_DIRECTORY + AUDIT_DIRECTORY_FOLDER
DATABASE_FILE_NAME = 'aws.sqlite3'
database_file_path = HOME + CONFIG_DIRECTORY + DATABASE_FILE_NAME


@click.command(
    short_help='Download customer-managed policies from all accounts in credentials file and generate a report.'
)
@click.option(
    '--credentials-file',
    default=DEFAULT_CREDENTIALS_FILE,
    help='Path to the AWS Credentials file. Defaults to ~/.aws/credentials.'
)
@click.option(
    '--include-unattached',
    is_flag=True,
    default=False,
    help='Download both attached and unattached policies.'
)
@click.option(
    '--report-config',
    default=False,
    help='Custom report configuration file. Contains policy name exclusions and custom risk score weighting.'
)
@click.option(
    '--output',
    default='report',
    help='Report file location. Defaults to ./report/'
)
def generate_report(credentials_file, output, report_config, include_unattached):
    """Download remote IAM policies to a directory for use in the analyze-iam-policies command."""
    # Consolidated these because we want the default to be attached policies only, with a boolean flag.
    # Only use the --include-unattached flag if you want to download those too.
    # Otherwise they would have to use a really long command every time.
    if include_unattached:
        attached_only = False
    else:
        attached_only = True
    # Only evaluate customer managed policies
    customer_managed = True
    profiles = get_list_of_aws_profiles(credentials_file)
    download_directories = download_policies_recursively(credentials_file, profiles)

    audit_files = {
        "privilege-escalation": "",
        "permissions-management": "",
        "credentials-exposure": "",
    }
    db_session = connect_db(database_file_path)
    for file in audit_files:
        analyze_policy_directory(download_directories, db_session, None, file)


