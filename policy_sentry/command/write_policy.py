"""
Given a Policy Sentry YML template, write a least-privilege IAM Policy in CRUD mode or Actions mode.
"""
import json
import click
from policy_sentry.shared.actions import get_all_actions, get_dependent_actions
from policy_sentry.shared.database import connect_db
from policy_sentry.shared.minimize import minimize_statement_actions
from policy_sentry.shared.policy import ArnActionGroup
from policy_sentry.shared.roles import Roles
from policy_sentry.shared.file import read_yaml_file
from policy_sentry.shared.constants import DATABASE_FILE_PATH, POLICY_LANGUAGE_VERSION


def print_policy(
        arn_dict_with_actions_and_resources,
        db_session,
        minimize=None):
    """
    Prints the least privilege policy
    """
    statement = []
    all_actions = get_all_actions(db_session)

    for sid in arn_dict_with_actions_and_resources:
        actions = arn_dict_with_actions_and_resources[sid]['actions']
        if minimize is not None and isinstance(minimize, int):
            actions = minimize_statement_actions(
                actions, all_actions, minchars=minimize)
        statement.append({
            "Sid": arn_dict_with_actions_and_resources[sid]['name'],
            "Effect": "Allow",
            "Action": actions,
            "Resource": arn_dict_with_actions_and_resources[sid]['arns']
        })

    policy = {
        "Version": POLICY_LANGUAGE_VERSION,
        "Statement": statement
    }
    return policy


def write_policy_with_access_levels(cfg, db_session, minimize_statement=False):
    """
    Writes an IAM policy given a dict containing Access Levels and ARNs.
    """
    arn_action_group = ArnActionGroup()
    arn_dict = arn_action_group.process_resource_specific_acls(cfg, db_session)
    policy = print_policy(arn_dict, db_session, minimize_statement)
    return policy


def write_policy_with_actions(cfg, db_session, minimize_statement=False):
    """
    Writes an IAM policy given a dict containing lists of actions.
    """
    policy_with_actions = Roles()
    policy_with_actions.process_actions_config(cfg)
    supplied_actions = []
    for role in policy_with_actions.get_roles():
        supplied_actions.extend(role[3].copy())
    supplied_actions = get_dependent_actions(db_session, supplied_actions)
    arn_action_group = ArnActionGroup()
    arn_dict = arn_action_group.process_list_of_actions(
        supplied_actions, db_session)
    policy = print_policy(arn_dict, db_session, minimize_statement)
    return policy


@click.command(
    short_help='Write least-privilege IAM policies, restricting all actions to resource ARNs.'
)
# pylint: disable=duplicate-code
@click.option(
    '--input-file',
    type=str,
    required=True,
    help='Path of the YAML File used for generating policies'
)
@click.option(
    '--crud',
    is_flag=True,
    required=False,
    help='Use the CRUD functionality. Defaults to false'
)
@click.option(
    '--minimize',
    required=False,
    type=int,
    help='Minimize the resulting statement with *safe* usage of wildcards to reduce policy length. '
         'Set this to the character length you want - for example, 4'
)
def write_policy(input_file, crud, minimize):
    """
    Write a least-privilege IAM Policy by supplying either a list of actions or
    access levels specific to resource ARNs!
    """
    # TODO: JSON Validation function

    db_session = connect_db(DATABASE_FILE_PATH)

    cfg = read_yaml_file(input_file)

    # User supplies file containing resource-specific access levels
    if crud:
        policy = write_policy_with_access_levels(cfg, db_session, minimize)
    # User supplies file containing a list of IAM actions
    else:
        policy = write_policy_with_actions(cfg, db_session, minimize)
    print(json.dumps(policy, indent=4))
    return policy
