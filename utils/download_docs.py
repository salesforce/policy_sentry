#!/usr/bin/env python3
"""
Parses the AWS HTML docs to create a YML file that understands the mapping between services and HTML files.
We store the HTML files in this manner so that the user can be more confident in the integrity of the data -
that it has not been altered in any way. The user can reproduce our steps with the original content at any time,
or update the HTML files on their own.
"""
import sys
import os
from pathlib import Path
sys.path.append(str(Path(os.path.dirname(__file__)).parent))
from policy_sentry.shared.awsdocs import create_database, update_html_docs_directory
from policy_sentry.shared.constants import (
    BUNDLED_ACCESS_OVERRIDES_FILE,
    BUNDLED_DATA_DIRECTORY,
    BUNDLED_DATASTORE_FILE_PATH,
    BUNDLED_HTML_DIRECTORY_PATH
)

BASE_DIR = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


if __name__ == '__main__':
    print("Downloading the latest AWS documentation from the Actions, Resources, and Condition Keys page")
    # update_html_docs_directory(BUNDLED_HTML_DIRECTORY_PATH)
    # Can't use the version of the same variable from the policy_sentry/shares/constants.py
    # file because of some syspath nonsense.
    # BUNDLED_DATASTORE_FILE_PATH = os.path.join(
    #     str(Path(os.path.dirname(__file__))), "policy_sentry", "shared", "data", "iam-definition.json"
    # )
    print("Data store file path: " + str(BUNDLED_DATASTORE_FILE_PATH))
    if os.path.exists(BUNDLED_DATASTORE_FILE_PATH):
        print("Datastore exists. Deleting then rebuilding...")
        os.remove(BUNDLED_DATASTORE_FILE_PATH)
    print("Building the IAM database")
    create_database(BUNDLED_DATA_DIRECTORY, BUNDLED_ACCESS_OVERRIDES_FILE)
    # print("Exporting the IAM database to CSV")
    # write_iam_database_to_csv()

    print("Checking the size of the IAM database as a sanity check.")
    file_size = os.path.getsize(BUNDLED_DATASTORE_FILE_PATH)
    # 1 Megabyte == 1024*1024 Bytes
    file_size = file_size/(1024*1024)
    print(f"IAM Definition file size in MB: {file_size} MB")
    assert file_size > 5

