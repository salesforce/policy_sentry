"""
Functions to support creating the proper resources in the Policy Sentry Config directory - ~/.policy_sentry.
"""
import os
import logging
import shutil
from policy_sentry.shared.constants import (
    CONFIG_DIRECTORY,
    LOCAL_HTML_DIRECTORY_PATH,
    LOCAL_DATABASE_FILE_PATH,
    LOCAL_LINKS_YML_FILE,
    BUNDLED_LINKS_YML_FILE,
    BUNDLED_HTML_DIRECTORY_PATH,
)
from policy_sentry.util.file import create_directory_if_it_doesnt_exist

logger = logging.getLogger(__name__)


def create_policy_sentry_config_directory():
    """
    Creates a config directory at $HOME/.policy_sentry/
    :return: the path of the database file
    """
    print("Creating the database...")
    logger.debug("We will store the new database here: %s", LOCAL_DATABASE_FILE_PATH)
    # If the database file already exists

    if os.path.exists(LOCAL_DATABASE_FILE_PATH):
        os.remove(LOCAL_DATABASE_FILE_PATH)
    elif os.path.exists(CONFIG_DIRECTORY):
        pass
    # If the config directory does not exist
    else:
        os.mkdir(CONFIG_DIRECTORY)
    return LOCAL_DATABASE_FILE_PATH


def create_html_docs_directory():
    """
    Copies the HTML files from the pip package over to its own folder in the CONFIG_DIRECTORY.
    Also copies over the links.yml file, which is a mapping of services and relevant HTML links in the AWS docs.
    Essentially:
    mkdir -p ~/.policy_sentry/data/docs
    cp -r $MODULE_DIR/policy_sentry/shared/data/docs ~/.policy_sentry/data/docs
    :return:
    """
    create_directory_if_it_doesnt_exist(LOCAL_HTML_DIRECTORY_PATH)
    # Copy from the existing html docs folder - the path ./policy_sentry/shared/data/docs within this repository
    logger.debug(BUNDLED_HTML_DIRECTORY_PATH)
    if os.path.exists(LOCAL_HTML_DIRECTORY_PATH):
        shutil.rmtree(LOCAL_HTML_DIRECTORY_PATH)
    shutil.copytree(BUNDLED_HTML_DIRECTORY_PATH, LOCAL_HTML_DIRECTORY_PATH)
    # Copy the links.yml file from here to the config directory
    shutil.copy(BUNDLED_LINKS_YML_FILE, LOCAL_LINKS_YML_FILE)
