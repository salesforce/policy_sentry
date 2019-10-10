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
import fnmatch
import pprint
from pathlib import Path
import os.path
import json
from policy_sentry.command.write_policy import write_policy_with_actions
from policy_sentry.shared.database import connect_db
from policyuniverse import all_permissions
from policy_sentry.shared.file import read_this_file
from policy_sentry.shared.actions import get_actions_by_access_level

HOME = str(Path.home())
CONFIG_DIRECTORY = '/.policy_sentry/'
DATABASE_FILE_NAME = 'aws.sqlite3'
AUDIT_DIRECTORY_FOLDER = '/audit'
audit_directory_path = HOME + CONFIG_DIRECTORY + AUDIT_DIRECTORY_FOLDER
audit_file_name = '/permissions-access-level.txt'
audit_file_path = audit_directory_path + audit_file_name
database_file_path = HOME + CONFIG_DIRECTORY + DATABASE_FILE_NAME


def read_json_policy_file(json_file):
    """
    read the json policy file and return a list of actions
    """

    # FIXME use a try/expect here to validate the json file. I would create a generic json
    with open(json_file) as json_file:
        # validation function/parser as there is a lot of json floating around in this tool. [MJ]
        data = json.load(json_file)
        actions_list = []
        # Multiple statements are in the 'Statement' list
        for statement in range(len(data['Statement'])):
            actions_list.extend(data['Statement'][statement]['Action'])
    actions_list = [x.lower() for x in actions_list]
    return actions_list


def read_risky_iam_permissions_text_file(audit_file):
    """
    read in the audit file of high risk actions
    """

    risky_actions = read_this_file(audit_file)
    return risky_actions


def determine_risky_actions(requested_actions, audit_file):
    """
    compare the actions in the policy against the audit file of high risk actions
    """

    risky_actions = read_risky_iam_permissions_text_file(audit_file)
    print("Auditing for risky actions...")
    for action in requested_actions:
        if action in risky_actions:
            print("Please justify why you need {}".format(action))
    print("Auditing for risky actions complete!")


def expand(action):  # FIXME [MJ] change the name to be more descriptive
    """
    expand the action wildcards into a full action
    """

    if isinstance(action, list):
        expanded_actions = []
        for item in action:
            expanded_actions.extend(expand(item))
        return expanded_actions

    if "*" in action:
        expanded = [
            expanded_action.lower()
            for expanded_action in all_permissions
            if fnmatch.fnmatchcase(expanded_action.lower(), action.lower())
        ]

        # if we get a wildcard for a tech we've never heard of, just return the wildcard
        if not expanded:
            print(
                "ERROR: The action {} references a wildcard for an unknown resource.".format(action))
            return [action.lower()]

        return expanded
    return [action.lower()]


def determine_actions_to_expand(action_list):
    """
    check to see if an action needs to get expanded
    """

    # FIXME why is this new, what is the change? Set a more descriptive variable name, this is a temp/local var
    # TODO Consider using enumerate instead of iterating with range and len
    new_action_list = []
    for action in range(len(action_list)):
        if "*" in action_list[action]:
            expanded_action = expand(action_list[action])
            new_action_list.extend(expanded_action)
        else:
            # If there is no wildcard, copy that action name over to the new_action_list
            # TODO do we check for dupes here to make sure we are staying DRY? [MJ] create issue for this
            new_action_list.append(action_list[action])
    return new_action_list


@click.command()
@click.option(
    '--audit-file',
    type=str,
    default=audit_file_path,
    help='The file containing AWS actions to audit. Default path is $HOME/.policy_sentry/audit/permissions-access-level.txt.'
)
@click.option(
    '--show',
    required=False,
    type=click.Choice(['read', 'write', 'list', 'tagging', 'permissions-management'], case_sensitive=False),
    help='Show CRUD levels. Acceptable values are read, write, list, tagging, permissions-management'
)
@click.option(
    '--print-policy',
    help='Print the example policy where actions are restricted to ARNs. Defaults to false.'
)
@click.option(
    '--file',
    required=True,
    help='Supply the requestors IAM policy as a JSON file. Accepts relative path.'
)
def analyze_iam_policy(audit_file, print_policy, file, show):
    """
    Analyze IAM Actions given a JSON policy file
    """
    db_session = connect_db(database_file_path)

    if os.path.exists(file):
        print("Evaluating: " + file)
    else:
        print("File does not exist or is formatted incorrectly: " + file + "\nPlease provide a valid path.")

    requested_actions = read_json_policy_file(file)
    expanded_actions = determine_actions_to_expand(requested_actions)

    if show:
        levels = get_actions_by_access_level(db_session, expanded_actions, show)
        print("Access level: " + show)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(levels)
    else:
        print("These are the expanded actions")
        print(expanded_actions)
        determine_risky_actions(expanded_actions, audit_file)
        if print_policy:
            write_policy_with_actions(expanded_actions, db_session)
