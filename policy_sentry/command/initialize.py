#!/usr/bin/env python3

import click
from policy_sentry.shared.config import create_policy_sentry_config_directory, \
    create_audit_directory, create_default_overrides_file, create_policy_analysis_directory, \
    create_default_report_config_file
from pathlib import Path
from policy_sentry.shared.database import connect_db, create_database
from policy_sentry.shared.file import get_list_of_service_prefixes_from_links_file
from policy_sentry.shared.constants import HOME, CONFIG_DIRECTORY


@click.command(
    short_help='Create a local database to store AWS IAM information.'
)
@click.option(
    '--access-level-overrides-file',
    type=str,
    required=False,
    default=HOME + CONFIG_DIRECTORY + 'access-level-overrides.yml',
    help='Path to access level overrides file, used to override the Access Levels per action provided by AWS docs'
)
def initialize(access_level_overrides_file):
    """
    Create a local database to store AWS IAM information, which can be used to generate IAM policies and analyze them for least privilege.
    """

    # Create the config directory
    database_path = create_policy_sentry_config_directory()
    # Create the directory to download IAM policies to
    create_policy_analysis_directory()
    # Create audit directory to host list of permissions for analyze_iam_policy
    create_audit_directory()
    # Create overrides file, which allows us to override the Access Levels
    # provided by AWS documentation
    create_default_overrides_file()
    # Create the default reporting configuration file. This is used by analyze_iam_policy
    create_default_report_config_file()
    # Connect to the database at that path with sqlalchemy
    db_session = connect_db(database_path)
    all_aws_services = get_list_of_service_prefixes_from_links_file()
    # Fill in the database with data on the AWS services
    create_database(db_session, all_aws_services, access_level_overrides_file)
    print("Created tables for all services!")
