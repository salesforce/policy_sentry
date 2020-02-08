"""
Functions to support creating the proper resources in the Policy Sentry Config directory - ~/.policy_sentry.
"""
from pathlib import Path
from os.path import exists, dirname
from os import remove, mkdir
import logging
import shutil
from policy_sentry.shared.constants import (
    HOME,
    CONFIG_DIRECTORY,
    DATABASE_FILE_NAME,
    HTML_DIRECTORY_PATH,
    HTML_DATA_DIRECTORY_SUBFOLDER,
)
from policy_sentry.util.file import create_directory_if_it_doesnt_exist

logger = logging.getLogger(__name__)


def create_policy_sentry_config_directory():
    """
    Creates a config directory at $HOME/.policy_sentry/
    :return: the path of the database file
    """
    print("Creating the database...")
    database_file_path = HOME + CONFIG_DIRECTORY + DATABASE_FILE_NAME
    logger.debug("We will store the new database here: %s", database_file_path)
    # If the database file already exists

    if exists(database_file_path):
        remove(database_file_path)
    elif exists(HOME + CONFIG_DIRECTORY):
        pass
    # If the config directory does not exist
    else:
        mkdir(HOME + CONFIG_DIRECTORY)
    return database_file_path


def create_html_docs_directory():
    """
    Copies the HTML files from the pip package over to its own folder in the CONFIG_DIRECTORY.
    Also copies over the links.yml file, which is a mapping of services and relevant HTML links in the AWS docs.
    Essentially:
    mkdir -p ~/.policy_sentry/data/docs
    cp -r $MODULE_DIR/policy_sentry/shared/data/docs ~/.policy_sentry/data/docs
    :return:
    """
    create_directory_if_it_doesnt_exist(HTML_DIRECTORY_PATH)
    # Copy from the existing html docs folder - the path ./policy_sentry/shared/data/docs within this repository
    # existing_html_docs_folder = abspath(
    #     dirname(__file__)) + HTML_DATA_DIRECTORY_SUBFOLDER
    existing_html_docs_folder = (
        str(Path(dirname(__file__)).parent) + "/shared" + HTML_DATA_DIRECTORY_SUBFOLDER
    )
    logger.debug(existing_html_docs_folder)
    if exists(HTML_DIRECTORY_PATH):
        shutil.rmtree(HTML_DIRECTORY_PATH)
    shutil.copytree(existing_html_docs_folder, HTML_DIRECTORY_PATH)
    # Copy the links.yml file from here to the config directory
    existing_links_file = (
        str(Path(dirname(__file__)).parent) + "/shared/data/" + "links.yml"
    )
    target_links_file = HOME + CONFIG_DIRECTORY + "links.yml"
    shutil.copy(existing_links_file, target_links_file)
