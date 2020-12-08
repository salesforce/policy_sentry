"""
Create the Policy Sentry config folder (~/.policy_sentry/) and the contents within
Create the SQLite datastore and fill it with the tables scraped from the AWS Docs
"""
import os
import shutil
import logging
import click
from policy_sentry.querying.all import get_all_service_prefixes
from policy_sentry.shared.awsdocs import (
    update_html_docs_directory,
    create_database,
)
from policy_sentry.shared.constants import (
    LOCAL_HTML_DIRECTORY_PATH,
    CONFIG_DIRECTORY,
    LOCAL_DATASTORE_FILE_PATH,
    DATASTORE_FILE_PATH,
    LOCAL_ACCESS_OVERRIDES_FILE,
    BUNDLED_HTML_DIRECTORY_PATH,
    BUNDLED_DATASTORE_FILE_PATH,
    BUNDLED_DATA_DIRECTORY,
)
from policy_sentry import set_stream_logger

logger = logging.getLogger(__name__)


@click.command(name="initialize", short_help="Create a local datastore to store AWS IAM information.")
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
    help="Build the IAM data file from the HTML files rather than copying the data file from "
         "the python package. Defaults to false",
)
@click.option(
    '--verbose', '-v',
    type=click.Choice(['critical', 'error', 'warning', 'info', 'debug'],
                      case_sensitive=False))
def initialize_command(access_level_overrides_file, fetch, build, verbose):
    """
    CLI command for initializing the local data file
    """
    if verbose:
        log_level = getattr(logging, verbose.upper())
        set_stream_logger(level=log_level)

    initialize(access_level_overrides_file, fetch, build)


def initialize(access_level_overrides_file=None, fetch=False, build=False):
    """
    Initialize the local data file to store AWS IAM information, which can be used to generate IAM policies, and for
    querying the database.
    """
    if not access_level_overrides_file:
        overrides_file = LOCAL_ACCESS_OVERRIDES_FILE
    else:
        overrides_file = access_level_overrides_file
    # Create the config directory
    database_path = create_policy_sentry_config_directory()

    # Copy over the html docs, which will be used to build the database
    create_html_docs_directory()

    # Create overrides file, which allows us to override the Access Levels
    # provided by AWS documentation
    file_list = [
        f
        for f in os.listdir(BUNDLED_DATA_DIRECTORY)
        if os.path.isfile(os.path.join(BUNDLED_DATA_DIRECTORY, f))
    ]

    for file in file_list:
        if file.endswith(".yml"):
            shutil.copy(os.path.join(BUNDLED_DATA_DIRECTORY, file), CONFIG_DIRECTORY)
            logger.debug("copying overrides file %s to %s", file, CONFIG_DIRECTORY)
    print("Database will be stored here: " + database_path)

    if not build and not fetch:
        # copy from the bundled database location to the destination path
        shutil.copy(BUNDLED_DATASTORE_FILE_PATH, database_path)

    # --fetch: wget the AWS IAM Actions, Resources and Condition Keys pages and store them locally.
    if fetch:
        # `wget` the html docs to the local directory
        update_html_docs_directory(LOCAL_HTML_DIRECTORY_PATH)

    # --build
    if build or access_level_overrides_file or fetch:
        create_database(CONFIG_DIRECTORY, overrides_file)
        print("Created the database!")

    # Query the database for all the services that are now in the database.
    all_aws_service_prefixes = get_all_service_prefixes()
    total_count_of_services = str(len(all_aws_service_prefixes))
    print("Initialization complete!")
    print(f"Total AWS services in the IAM database: {total_count_of_services}")
    logger.debug("\nService prefixes:")
    logger.debug(", ".join(all_aws_service_prefixes))


def create_policy_sentry_config_directory():
    """
    Creates a config directory at $HOME/.policy_sentry/
    :return: the path of the database file
    """
    print("Creating the database...")
    logger.debug(f"We will store the new database here: {DATASTORE_FILE_PATH}")
    # If the database file already exists, remove it
    if os.path.exists(LOCAL_DATASTORE_FILE_PATH):
        logger.debug(f"The database at {DATASTORE_FILE_PATH} already exists. Removing and replacing it.")
        os.remove(LOCAL_DATASTORE_FILE_PATH)
    elif os.path.exists(CONFIG_DIRECTORY):
        pass
    # If the config directory does not exist
    else:
        os.mkdir(CONFIG_DIRECTORY)
    return LOCAL_DATASTORE_FILE_PATH


def create_html_docs_directory():
    """
    Copies the HTML files from the pip package over to its own folder in the CONFIG_DIRECTORY.
    Essentially:
    mkdir -p ~/.policy_sentry/data/docs
    cp -r $MODULE_DIR/policy_sentry/shared/data/docs ~/.policy_sentry/data/docs
    :return:
    """
    if os.path.exists(LOCAL_HTML_DIRECTORY_PATH):
        pass
    else:
        os.makedirs(LOCAL_HTML_DIRECTORY_PATH)
    # Copy from the existing html docs folder - the path ./policy_sentry/shared/data/docs within this repository
    logger.debug(BUNDLED_HTML_DIRECTORY_PATH)
    if os.path.exists(LOCAL_HTML_DIRECTORY_PATH):
        shutil.rmtree(LOCAL_HTML_DIRECTORY_PATH)
    shutil.copytree(BUNDLED_HTML_DIRECTORY_PATH, LOCAL_HTML_DIRECTORY_PATH)
