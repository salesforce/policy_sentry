"""
Create the Policy Sentry config folder (~/.policy_sentry/) and the contents within
Create the SQLite database and fill it with the tables scraped from the AWS Docs
"""
import shutil
import logging
import click
import click_log
from policy_sentry.configuration.access_level_overrides import (
    create_default_overrides_file,
)
from policy_sentry.configuration.config_directory import (
    create_policy_sentry_config_directory,
    create_html_docs_directory,
)
from policy_sentry.querying.all import get_all_service_prefixes
from policy_sentry.scraping.awsdocs import (
    update_html_docs_directory,
    get_list_of_service_prefixes_from_links_file,
    create_service_links_mapping_file,
)
from policy_sentry.shared.database import connect_db, create_database
from policy_sentry.shared.constants import (
    HOME,
    CONFIG_DIRECTORY,
    HTML_DIRECTORY_PATH,
    LINKS_YML_FILE_LOCAL,
    BUNDLED_DATABASE_FILE_PATH,
)

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.command(short_help="Create a local database to store AWS IAM information.")
@click.option(
    "--access-level-overrides-file",
    type=str,
    required=False,
    help="Path to access level overrides file, used to override the Access Levels per action provided by AWS docs",
)
@click.option(
    "--fetch",
    is_flag=True,
    required=False,
    default=False,
    help="Specify this flag to fetch the HTML Docs directly from the AWS website. This will be helpful if the docs "
    "in the Git repository are behind the live docs and you need to use the latest version of the docs right "
    "now.",
)
@click.option(
    "--build",
    is_flag=True,
    required=False,
    default=False,
    help="Build the SQLite database from the HTML files rather than copying the SQLite database file from "
    "the python package. Defaults to false",
)
@click_log.simple_verbosity_option(logger)
def initialize(access_level_overrides_file, fetch, build):
    """
    Initialize the local database to store AWS IAM information, which can be used to generate IAM policies, and for
    querying the database.
    """

    if not access_level_overrides_file:
        overrides_file = HOME + CONFIG_DIRECTORY + "access-level-overrides.yml"
    else:
        overrides_file = access_level_overrides_file
    # Create the config directory
    database_path = create_policy_sentry_config_directory()

    # Copy over the html docs, which will be used to build the database
    create_html_docs_directory()

    # Create overrides file, which allows us to override the Access Levels
    # provided by AWS documentation
    create_default_overrides_file()

    print("Database will be stored here: %s", database_path)

    if not build and not fetch:
        # copy from the bundled database location to the destination path
        shutil.copy(BUNDLED_DATABASE_FILE_PATH, database_path)

    # Connect to the database at that path with SQLAlchemy
    db_session = connect_db(database_path, initialization=True)

    # --fetch: wget the AWS IAM Actions, Resources and Condition Keys pages and store them locally.
    # if --build and --fetch are both supplied, just do --fetch
    if fetch:
        # `wget` the html docs to the local directory
        update_html_docs_directory(HTML_DIRECTORY_PATH)
        # Update the links.yml file
        prefix_list = create_service_links_mapping_file(
            HTML_DIRECTORY_PATH, LINKS_YML_FILE_LOCAL
        )
        print(f"Services: {prefix_list}")

    # initialize --build
    if build or access_level_overrides_file or fetch:
        # Use the list of services that were listed in the links.yml file
        all_aws_services = get_list_of_service_prefixes_from_links_file(
            LINKS_YML_FILE_LOCAL
        )
        logger.debug("Services to build are stored in: %s", LINKS_YML_FILE_LOCAL)
        # Fill in the database with data on the AWS services
        create_database(db_session, all_aws_services, overrides_file)
        print("Created tables for all services!")

    # Query the database for all the services that are now in the database.
    all_aws_service_prefixes = get_all_service_prefixes(db_session)
    total_count_of_services = str(len(all_aws_service_prefixes))
    print("Initialization complete!")
    print(f"Total AWS services in the IAM database: {total_count_of_services}")
    logger.debug("\nService prefixes:")
    logger.debug(", ".join(all_aws_service_prefixes))
