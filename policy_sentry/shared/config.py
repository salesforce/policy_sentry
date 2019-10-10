# Manages the policy_sentry config directory and files
# Default location is $HOME/.policy_sentry
from pathlib import Path
import os
from policy_sentry.shared.file import read_this_file

HOME = str(Path.home())
CONFIG_DIRECTORY = '/.policy_sentry/'
DATABASE_FILE_NAME = 'aws.sqlite3'
AUDIT_DIRECTORY_FOLDER = '/audit'


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
    Creates directory for analyze_iam_policy audit files and places a single audit file there.
    """
    audit_directory_path = HOME + CONFIG_DIRECTORY + AUDIT_DIRECTORY_FOLDER
    if os.path.exists(audit_directory_path):
        pass
    else:
        os.mkdir(audit_directory_path)

    permissions_audit_file = os.path.abspath(os.path.dirname(__file__)) + '/data/audit/permissions-access-level.txt'
    lines = read_this_file(permissions_audit_file)
    audit_file_name = '/permissions-access-level.txt'
    new_audit_file = audit_directory_path + audit_file_name
    with open(new_audit_file, 'w+') as fileobj:
        for line in lines:
            fileobj.write(line)
            fileobj.write('\n')
            fileobj.flush()
    fileobj.close()

