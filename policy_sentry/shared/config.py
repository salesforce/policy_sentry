# Manages the policy_sentry config directory and files
# Default location is $HOME/.policy_sentry
from pathlib import Path
import os
from policy_sentry.shared.file import read_this_file, create_directory_if_it_doesnt_exist, list_files_in_directory
import shutil

HOME = str(Path.home())
CONFIG_DIRECTORY = '/.policy_sentry/'
DATABASE_FILE_NAME = 'aws.sqlite3'
AUDIT_DIRECTORY_FOLDER = 'audit/'


def create_policy_sentry_config_directory():
    """
    Creates a config directory at $HOME/.policy_sentry/
    :return: the path of the database file
    """
    print("Creating the database...")

    database_path = HOME + CONFIG_DIRECTORY + DATABASE_FILE_NAME
    print("We will store the new database here: " + database_path)
    # If the database file already exists
    if os.path.exists(database_path):
        os.remove(database_path)
    elif os.path.exists(HOME+CONFIG_DIRECTORY):
        pass
    # If the config directory does not exist
    else:
        os.mkdir(HOME+CONFIG_DIRECTORY)
    return database_path


def create_audit_directory():
    """
    Creates directory for analyze_iam_policy audit files and places audit files there.
    """
    audit_directory_path = HOME + CONFIG_DIRECTORY + AUDIT_DIRECTORY_FOLDER
    create_directory_if_it_doesnt_exist(audit_directory_path)
    destination = audit_directory_path

    existing_audit_files_directory = os.path.abspath(os.path.dirname(__file__)) + '/data/audit/'
    source = existing_audit_files_directory
    file_list = list_files_in_directory(existing_audit_files_directory)

    for file in file_list:
        if file.endswith(".txt"):
            shutil.copy(source + '/' + file, destination)
            print("copying " + file + " to " + destination)

