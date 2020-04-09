#!/usr/bin/env python3
"""
Parses the AWS HTML docs to create a YML file that understands the mapping between services and HTML files.
We store the HTML files in this manner so that the user can be more confident in the integrity of the data -
that it has not been altered in any way. The user can reproduce our steps with the original content at any time,
or update the HTML files on their own.
"""
import sys
import os
import csv
from pathlib import Path
sys.path.append(str(Path(os.path.dirname(__file__)).parent))
# from policy_sentry.scraping.awsdocs import update_html_docs_directory, create_service_links_mapping_file, \
#     get_list_of_service_prefixes_from_links_file
from policy_sentry.shared.awsdocs import create_database, update_html_docs_directory
from policy_sentry.shared.constants import (
    BUNDLED_LINKS_YML_FILE,
    BUNDLED_ACCESS_OVERRIDES_FILE,
    BUNDLED_HTML_DIRECTORY_PATH,
    BUNDLED_DATASTORE_FILE_PATH,
    BUNDLED_ACCESS_OVERRIDES_FILE,
    BUNDLED_DATA_DIRECTORY
)
# , ActionTable, ArnTable, ConditionTable, create_database

# BUNDLED_DATABASE_FILE_PATH = str(Path(
#     os.path.dirname(__file__)).parent) + '/policy_sentry/shared/data/' + 'aws.sqlite3'
BASE_DIR = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

#
# def build_database():
#     db_path = os.path.join(BASE_DIR, BUNDLED_DATABASE_FILE_PATH)
#     print(db_path)
#
#     if os.path.exists(db_path):
#         os.remove(db_path)
#         print(f"Pre-existing bundled database at {db_path} removed; it will be replaced now.")
#     db_session = connect_db(db_path, initialization=True)
#     all_aws_services = get_list_of_service_prefixes_from_links_file(
#         BUNDLED_LINKS_YML_FILE)
#     create_database(db_session, all_aws_services, BUNDLED_ACCESS_OVERRIDES_FILE)
#
#
# def update_docs():
#     print("Reminder: Run this from the main directory of the code repository.")
#     print(f"Updating the HTML docs directory at {BUNDLED_HTML_DIRECTORY_PATH}.")
#     update_html_docs_directory(BUNDLED_HTML_DIRECTORY_PATH)
#     print("Creating the service links mapping file.")
#     create_service_links_mapping_file(BUNDLED_HTML_DIRECTORY_PATH, BUNDLED_LINKS_YML_FILE)
#
#
# def write_action_table_csv(db_session):
#
#     rows = db_session.query(ActionTable)
#     f = open(os.path.join(BASE_DIR, 'policy_sentry', 'shared', 'data', 'action_table.csv'), 'w')
#     out = csv.writer(f, delimiter=';')
#     out.writerow([
#         'service',
#         'name',
#         'description',
#         'access_level',
#         'resource_type_name',
#         'resource_type_name_append_wildcard',
#         'resource_arn_format']
#     )
#     for row in rows:
#         # print(row)
#         out.writerow([
#             row.service,
#             row.name,
#             row.description,
#             row.access_level,
#             row.resource_type_name,
#             row.resource_type_name_append_wildcard,
#             row.resource_arn_format
#         ])
#         f.flush()
#     f.close()
#
#
# def write_arn_table_csv(db_session):
#     rows = db_session.query(ArnTable)
#     f = open(os.path.join(BASE_DIR, 'policy_sentry', 'shared', 'data', 'arn_table.csv'), 'w')
#     out = csv.writer(f, delimiter=';')
#     out.writerow([
#         'resource_type_name',
#         'raw_arn',
#         'originating_service',
#         'arn',
#         'partition',
#         'service',
#         'region',
#         'account',
#         'resource_path',
#         'condition_keys'
#     ])
#     for row in rows:
#         out.writerow([
#             row.resource_type_name,
#             row.raw_arn,
#             row.originating_service,
#             row.arn,
#             row.partition,
#             row.service,
#             row.region,
#             row.account,
#             row.resource_path,
#             row.condition_keys,
#         ])
#         f.flush()
#     f.close()
#
#
# def write_condition_table_csv(db_session):
#     rows = db_session.query(ConditionTable)
#     f = open(os.path.join(BASE_DIR, 'policy_sentry', 'shared', 'data',  'condition_table.csv'), 'w')
#     out = csv.writer(f, delimiter=';')
#     out.writerow([
#         'service',
#         'condition_key_name',
#         'condition_key_service',
#         'description',
#         'condition_value_type',
#     ])
#     for row in rows:
#         out.writerow([
#             row.service,
#             row.condition_key_name,
#             row.condition_key_service,
#             row.description,
#             row.condition_value_type,
#         ])
#         f.flush()
#     f.close()
#

# def write_iam_database_to_csv():
    # db_session = connect_ db(os.path.join(BASE_DIR, 'policy_sentry', 'shared', 'data', 'aws.sqlite3'))
    # table_files = [
    #     os.path.join(BASE_DIR, 'policy_sentry', 'shared', 'data', 'action_table.csv'),
    #     os.path.join(BASE_DIR, 'policy_sentry', 'shared', 'data', 'arn_table.csv'),
    #     os.path.join(BASE_DIR, 'policy_sentry', 'shared', 'data',  'condition_table.csv')
    # ]
    # for table_file in table_files:
    #     if os.path.exists(table_file):
    #         os.remove(table_file)
    # print("Writing Action Table to CSV...")
    # write_action_table_csv(db_session)
    # print("Writing ARN Table to CSV...")
    # write_arn_table_csv(db_session)
    # print("Writing Condition Table to CSV...")
    # write_condition_table_csv(db_session)


if __name__ == '__main__':
    print("Downloading the latest AWS documentation from the Actions, Resources, and Condition Keys page")
    # update_html_docs_directory(BUNDLED_HTML_DIRECTORY_PATH)
    print("Building the IAM database")
    create_database(BUNDLED_DATA_DIRECTORY, BUNDLED_ACCESS_OVERRIDES_FILE)
    # print("Exporting the IAM database to CSV")
    # write_iam_database_to_csv()

