"""
Functions to support the analyze capability in this tool
"""
import fnmatch
import copy
import logging
import re
from policy_sentry.querying.actions import remove_actions_not_matching_access_level
from policy_sentry.querying.all import get_all_actions
from policy_sentry.util.actions import get_lowercase_action_list
from policy_sentry.util.policy_files import (
    get_actions_from_json_policy_file,
    get_actions_from_policy,
    get_actions_from_statement,
)
from policy_sentry.util.file import read_this_file

logger = logging.getLogger(__name__)


def read_risky_iam_permissions_text_file(audit_file):
    """
    read in the audit file of high risk actions

    :param audit_file: Path to the file containing a list of risky actions
    :return risky_actions: A list of actions from the file
    """

    risky_actions = read_this_file(audit_file)
    return risky_actions


def determine_risky_actions_from_list(requested_actions, risky_actions):
    """
    compare the actions in the policy against a list of high risk actions

    :param requested_actions: A list of the actions that are requested by the policy under evaluation
    :param risky_actions: A list of risky IAM actions to evaluate.
    :return: a list of any actions that are included in the file of risky actions
    """

    risky_actions_lowercase = get_lowercase_action_list(risky_actions)
    actions_to_triage = []
    for action in requested_actions:
        if action.lower() in risky_actions_lowercase:
            actions_to_triage.append(action)
    return actions_to_triage


def determine_risky_actions(requested_actions, audit_file):
    """
    compare the actions in the policy against the audit file of high risk actions

    :param requested_actions: A list of the actions that are requested by the policy under evaluation
    :param audit_file: The absolute path to the file that contains a list of IAM action to evaluate.
    :return: a list of any actions that are included in the file of risky actions
    """

    risky_actions = read_risky_iam_permissions_text_file(audit_file)
    return determine_risky_actions_from_list(requested_actions, risky_actions)


def expand(action, db_session):
    """
    expand the action wildcards into a full action

    :param action: An action in the form with a wildcard - like s3:Get*, or s3:L*
    :param db_session: SQLAlchemy database session object
    :return: A list of all the expanded actions (like actions matching s3:Get*)
    :rtype: list
    """

    all_actions = get_all_actions(db_session)

    if isinstance(action, list):
        expanded_actions = []
        for item in action:
            expanded_actions.extend(expand(item, db_session))
        return expanded_actions

    if "*" in action:
        expanded = [
            expanded_action
            # for expanded_action in all_permissions
            for expanded_action in all_actions
            if fnmatch.fnmatchcase(expanded_action.lower(), action.lower())
        ]

        # if we get a wildcard for a tech we've never heard of, just return the
        # wildcard
        if not expanded:
            logger.warning(
                "ERROR: The action %s references a wildcard for an unknown resource.",
                action,
            )
            return [action]

        return expanded
    return [action]


def determine_actions_to_expand(db_session, action_list):
    """
    Determine if an action needs to get expanded from its wildcard

    :param db_session: A SQLAlchemy database session object
    :param action_list: A list of actions
    :return: A list of actions
    :rtype: list
    """
    new_action_list = []
    for action in range(len(action_list)):
        if "*" in action_list[action]:
            expanded_action = expand(action_list[action], db_session)
            new_action_list.extend(expanded_action)
        else:
            # If there is no wildcard, copy that action name over to the new_action_list
            new_action_list.append(action_list[action])
    new_action_list.sort()
    return new_action_list


def analyze_policy_file(
    db_session,
    policy_file,
    account_id,
    from_audit_file,
    finding_type,
    excluded_role_patterns,
):
    """
    Given a policy file, determine risky actions based on a separate file containing a list of actions.
    If it matches a policy exclusion pattern from the report-config.yml file, that policy file will be skipped.

    :param db_session: SQLAlchemy database session object
    :param policy_file: The path to the policy file to be evaluated
    :param account_id: The AWS Account ID
    :param from_audit_file: The file containing the list of problematic actions
    :param finding_type: The type of finding - resource_exposure, privilege_escalation, network_exposure, or credentials_exposure
    :param excluded_role_patterns: A RegEx pattern for excluding policy names from evaluation.

    :return: False if the policy name matches excluded role patterns, or if it does not, a dictionary containing the findings.
    :rtype: dict
    """
    requested_actions = get_actions_from_json_policy_file(db_session, policy_file)
    expanded_actions = determine_actions_to_expand(db_session, requested_actions)

    finding = {}
    policy_findings = {}

    policy_name = policy_file.rsplit(".", 1)[0]  # after the extension
    policy_name_split = str.split(policy_name, "/")
    # if there are multiple folders deep pick `file` from `path/to/file`
    policy_name = policy_name_split[-1:][0]

    # If the policy name matches excluded role patterns, skip it
    reg_list = map(re.compile, excluded_role_patterns)
    if any(regex.match(policy_name) for regex in reg_list):
        return False
    else:
        actions_list = determine_risky_actions(expanded_actions, from_audit_file)
        actions_list.sort()  # sort in alphabetical order
        actions_list = list(dict.fromkeys(actions_list))  # remove duplicates
        if actions_list:
            finding[finding_type] = copy.deepcopy(actions_list)
            # Store the account ID
            finding["account_id"] = account_id
            policy_findings[policy_name] = copy.deepcopy(finding)
        else:
            # Just store the account ID
            finding["account_id"] = account_id
        return policy_findings


def analyze_by_access_level(db_session, policy_json, access_level):
    """
    Determine if a policy has any actions with a given access level. This is particularly useful when determining who
    has 'Permissions management' level access

    :param db_session: SQLAlchemy database session
    :param policy_json: a dictionary representing the AWS JSON policy
    :param access_level: The normalized access level - either 'read', 'list', 'write', 'tagging', or 'permissions-management'
    """
    requested_actions = get_actions_from_policy(db_session, policy_json)
    expanded_actions = determine_actions_to_expand(db_session, requested_actions)
    actions_by_level = remove_actions_not_matching_access_level(
        db_session, expanded_actions, access_level
    )
    return actions_by_level


def analyze_statement_by_access_level(db_session, statement_json, access_level):
    """
    Determine if a statement has any actions with a given access level.

    :param db_session: SQLAlchemy database session
    :param statement_json: a dictionary representing a statement from an AWS JSON policy
    :param access_level: The normalized access level - either 'read', 'list', 'write', 'tagging', or 'permissions-management'
    """
    requested_actions = get_actions_from_statement(statement_json)
    expanded_actions = determine_actions_to_expand(db_session, requested_actions)
    actions_by_level = remove_actions_not_matching_access_level(
        db_session, expanded_actions, access_level
    )
    return actions_by_level
