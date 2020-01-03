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
from policy_sentry.scraping.awsdocs import update_html_docs_directory, create_service_links_mapping_file, \
    get_list_of_service_prefixes_from_links_file
from policy_sentry.shared.constants import LINKS_YML_FILE_IN_PACKAGE, DEFAULT_ACCESS_OVERRIDES_FILE
from policy_sentry.shared.database import connect_db, create_database

BUNDLED_DATABASE_FILE_PATH = str(Path(
    os.path.dirname(__file__)).parent) + '/policy_sentry/shared/data/' + 'aws.sqlite3'


def build_database():
    print(BUNDLED_DATABASE_FILE_PATH)
    db_session = connect_db(BUNDLED_DATABASE_FILE_PATH)
    all_aws_services = get_list_of_service_prefixes_from_links_file(
        LINKS_YML_FILE_IN_PACKAGE)
    create_database(db_session, all_aws_services, DEFAULT_ACCESS_OVERRIDES_FILE)


def update_docs():
    html_directory_path = str(Path(os.path.dirname(__file__)).parent) + '/policy_sentry/shared/data/docs/'
    links_yml_file = str(Path(os.path.dirname(__file__)).parent) + '/policy_sentry/shared/data/links.yml'
    print("Reminder: Run this from the main directory of the code repository.")
    print(f"Updating the HTML docs directory at {html_directory_path}.")
    update_html_docs_directory(html_directory_path)
    print("Creating the service links mapping file.")
    create_service_links_mapping_file(html_directory_path, links_yml_file)


if __name__ == '__main__':
    update_docs()
    build_database()
