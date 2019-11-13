#!/usr/bin/env python3

"""
    analyze_iam_policy will audit the policy for any security concerns

    Approach:
    * Compile list of actions, as-is, from the policy. This includes wildcards in the actions
    * Look them up in the database
    * write_policy with those actions (since the teams will likely provide * in resources, we want to give them something restricted to ARNs)

    list of managed policies
    https://gist.github.com/0xdabbad00/645837c1fcd043876d13a56819188227
    https://github.com/SummitRoute/aws_managed_policies
"""

import click
import pprint
from pathlib import Path
import os.path
from policy_sentry.shared.database import connect_db
from policy_sentry.shared.actions import get_actions_by_access_level, get_actions_from_json_policy_file
from policy_sentry.shared.analyze import determine_actions_to_expand, determine_risky_actions, analyze
from policy_sentry.shared.file import list_files_in_directory


HOME = str(Path.home())
CONFIG_DIRECTORY = '/.policy_sentry/'
DATABASE_FILE_NAME = 'aws.sqlite3'
AUDIT_DIRECTORY_FOLDER = '/audit'
audit_directory_path = HOME + CONFIG_DIRECTORY + AUDIT_DIRECTORY_FOLDER
audit_file_name = '/permissions-access-level.txt'
audit_file_path = audit_directory_path + audit_file_name
database_file_path = HOME + CONFIG_DIRECTORY + DATABASE_FILE_NAME


@click.command()
@click.option(
    '--from-audit-file',
    type=str,
    default=audit_file_path,
    help='The file containing AWS actions to audit. Default path is $HOME/.policy_sentry/audit/permissions-access-level.txt.'
)
@click.option(
    '--from-access-level',
    required=False,
    type=click.Choice(['read', 'write', 'list', 'tagging',
                       'permissions-management'], case_sensitive=False),
    help='Show CRUD levels. Acceptable values are read, write, list, tagging, permissions-management'
)
@click.option(
    '--policy',
    required=True,
    help='Supply the requestors IAM policy as a JSON file. Accepts relative path.'
)
def analyze_iam_policy(from_audit_file, policy, from_access_level):
    """
    Analyze IAM Actions given a JSON policy file
    """
    db_session = connect_db(database_file_path)

    if os.path.exists(policy):
        if os.path.isdir(policy):
            print("Evaluating policy files in " + policy)
        else:
            print("Evaluating policy file: " + policy)
    else:
        print("File/directory does not exist: " +
              policy + "\nPlease provide a valid path.")
        exit()

    if os.path.isdir(policy):
        file_list = list_files_in_directory(policy)
        print("Access level: " + from_access_level)
        for file in file_list:
            this_file = policy + '/' + file
            analyze(this_file, db_session, from_access_level, from_audit_file)
    elif os.path.isfile(policy):
        analyze(policy, db_session, from_access_level, from_audit_file)
