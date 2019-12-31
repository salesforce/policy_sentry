"""
Create the Policy Sentry config folder (~/.policy_sentry/) and the contents within
Create the SQLite database and fill it with the tables scraped from the AWS Docs
"""
import click
from policy_sentry.querying.all import get_all_service_prefixes
from policy_sentry.configuration.access_level_overrides import create_default_overrides_file
from policy_sentry.configuration.analysis import create_default_report_config_file
from policy_sentry.configuration.config_directory import create_policy_sentry_config_directory, \
    create_audit_directory, create_policy_analysis_directory, create_html_docs_directory
from policy_sentry.shared.database import connect_db, create_database
from policy_sentry.scraping.awsdocs import update_html_docs_directory, get_list_of_service_prefixes_from_links_file, \
    create_service_links_mapping_file
from policy_sentry.shared.constants import HOME, CONFIG_DIRECTORY, HTML_DIRECTORY_PATH, LINKS_YML_FILE_LOCAL


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
@click.option(
    '--fetch',
    is_flag=True,
    required=False,
    default=False,
    help='Specify this flag to fetch the HTML Docs directly from the AWS website. This will be helpful if the docs '
         'in the Git repository are behind the live docs and you need to use the latest version of the docs right '
         'now.'
)
def initialize(access_level_overrides_file, fetch):
    """
    Create a local database to store AWS IAM information, which can be used to generate IAM policies and analyze them
    for least privilege.
    """

    # Create the config directory
    database_path = create_policy_sentry_config_directory()

    # Copy over the html docs, which will be used to build the database
    create_html_docs_directory()

    # Create the directory to download IAM policies to
    create_policy_analysis_directory()

    # Create audit directory to host list of permissions for analyze_iam_policy
    create_audit_directory()

    # Create overrides file, which allows us to override the Access Levels
    # provided by AWS documentation
    create_default_overrides_file()

    # Create the default reporting configuration file. This is used by
    # analyze_iam_policy
    create_default_report_config_file()

    # If the user specifies fetch, wget the AWS IAM Actions, Resources and Condition Keys pages and store them locally.
    if fetch:
        # `wget` the html docs to the local directory
        update_html_docs_directory(HTML_DIRECTORY_PATH)
        # Update the links.yml file
        prefix_list = create_service_links_mapping_file(
            HTML_DIRECTORY_PATH, LINKS_YML_FILE_LOCAL)
        print(f"Services: {prefix_list}")

    # Connect to the database at that path with SQLAlchemy
    db_session = connect_db(database_path)
    # Use the list of services that were listed in the links.yml file
    all_aws_services = get_list_of_service_prefixes_from_links_file(
        LINKS_YML_FILE_LOCAL)
    print(f"Services to build for: ${LINKS_YML_FILE_LOCAL}")

    # Fill in the database with data on the AWS services
    create_database(db_session, all_aws_services, access_level_overrides_file)
    print("Created tables for all services!")

    # Query the database for all the services that are now in the database.
    all_aws_service_prefixes = get_all_service_prefixes(db_session)
    total_count_of_services = str(len(all_aws_service_prefixes))
    print(f"{total_count_of_services} AWS services in the database. \nServices: {all_aws_service_prefixes}")
