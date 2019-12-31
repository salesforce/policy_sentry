"""
Functions to support creating the proper resources in the Policy Sentry Config directory - ~/.policy_sentry.
"""
import os
from pathlib import Path
import shutil
from policy_sentry.shared.constants import HOME, CONFIG_DIRECTORY, AUDIT_DIRECTORY_PATH, DATABASE_FILE_PATH, \
    HTML_DIRECTORY_PATH, HTML_DATA_DIRECTORY_SUBFOLDER
from policy_sentry.util.file import create_directory_if_it_doesnt_exist, list_files_in_directory


def create_policy_sentry_config_directory():
    """
    Creates a config directory at $HOME/.policy_sentry/
    :return: the path of the database file
    """
    print("Creating the database...")

    print("We will store the new database here: " + DATABASE_FILE_PATH)
    # If the database file already exists
    if os.path.exists(DATABASE_FILE_PATH):
        os.remove(DATABASE_FILE_PATH)
    elif os.path.exists(HOME + CONFIG_DIRECTORY):
        pass
    # If the config directory does not exist
    else:
        os.mkdir(HOME + CONFIG_DIRECTORY)
    return DATABASE_FILE_PATH


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
    # existing_html_docs_folder = os.path.abspath(
    #     os.path.dirname(__file__)) + HTML_DATA_DIRECTORY_SUBFOLDER
    existing_html_docs_folder = str(Path(
        os.path.dirname(__file__)).parent) + '/shared' + HTML_DATA_DIRECTORY_SUBFOLDER
    print(existing_html_docs_folder)
    if os.path.exists(HTML_DIRECTORY_PATH):
        shutil.rmtree(HTML_DIRECTORY_PATH)
    shutil.copytree(existing_html_docs_folder, HTML_DIRECTORY_PATH)
    # Copy the links.yml file from here to the config directory
    existing_links_file = str(Path(
        os.path.dirname(__file__)).parent) + '/shared/data/' + 'links.yml'
    target_links_file = HOME + CONFIG_DIRECTORY + 'links.yml'
    shutil.copy(existing_links_file, target_links_file)


def create_audit_directory():
    """
    Creates directory for analyze_iam_policy audit files and places audit files there.

    Essentially:
    mkdir -p ~/.policy_sentry/audit
    cp -r $MODULE_DIR/policy_sentry/shared/data/audit/ ~/.policy_sentry/audit/
    """
    create_directory_if_it_doesnt_exist(AUDIT_DIRECTORY_PATH)
    destination = AUDIT_DIRECTORY_PATH
    existing_audit_files_directory = str(
        Path(os.path.dirname(__file__)).parent) + '/shared/data/audit/'
    source = existing_audit_files_directory
    file_list = list_files_in_directory(existing_audit_files_directory)

    for file in file_list:
        if file.endswith(".txt"):
            shutil.copy(source + '/' + file, destination)
            print("copying " + file + " to " + destination)


def create_policy_analysis_directory():
    """
    Creates directory for analyze_iam_policy policies.

    Essentially:
    mkdir -p ~/.policy_sentry/analysis
    """
    policy_analysis_directory_path = HOME + CONFIG_DIRECTORY + 'analysis'
    if os.path.exists(policy_analysis_directory_path):
        pass
    else:
        os.mkdir(policy_analysis_directory_path)
