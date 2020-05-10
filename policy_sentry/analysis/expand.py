"""Functions to expand wilcard actions into a full list of actions."""
import logging
import copy
import fnmatch
from policy_sentry.querying.all import get_all_actions
from policy_sentry.util.policy_files import get_actions_from_statement

logger = logging.getLogger(__name__)


def expand(action):
    """
    expand the action wildcards into a full action

    Arguments:
        action: An action in the form with a wildcard - like s3:Get*, or s3:L*
    Returns:
        List: A list of all the expanded actions (like actions matching s3:Get*)
    """

    all_actions = get_all_actions()

    if isinstance(action, list):
        expanded_actions = []
        for item in action:
            expanded_actions.extend(expand(item))
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
            logger.debug(
                "ERROR: The action %s references a wildcard for an unknown resource.",
                action,
            )
            return [action]

        return expanded
    return [action]


def determine_actions_to_expand(action_list):
    """
    Determine if an action needs to get expanded from its wildcard

    Arguments:
        action_list: A list of actions
    Returns:
        List: A list of actions
    """
    new_action_list = []
    for action in range(len(action_list)):
        if "*" in action_list[action]:
            expanded_action = expand(action_list[action])
            new_action_list.extend(expanded_action)
        else:
            # If there is no wildcard, copy that action name over to the new_action_list
            new_action_list.append(action_list[action])
    new_action_list.sort()
    return new_action_list


def get_expanded_policy(policy):
    """
    Given a policy, expand the * Actions in IAM policy files to improve readability

    Arguments:
        policy: dictionary containing valid AWS IAM Policy
    Returns:
        Dictionary: the policy that has the `*` expanded
    """
    modified_policy = copy.deepcopy(policy)

    if isinstance(modified_policy["Statement"], dict):
        requested_actions = get_actions_from_statement(modified_policy["Statement"])
        expanded_actions = determine_actions_to_expand(requested_actions)
        if "NotAction" in modified_policy["Statement"]:
            if isinstance(modified_policy["Statement"]["NotAction"], list):
                modified_policy["Statement"]["NotAction"].clear()
                modified_policy["Statement"]["NotAction"].extend(expanded_actions)
            elif isinstance(modified_policy["Statement"]["NotAction"], str):
                modified_policy["Statement"]["NotAction"] = []
            logger.warning(
                "NotAction is in the statement. Policy Sentry will expand any wildcard actions "
                "that are in the NotAction list, but it will not factor the NotAction actions into any analysis about "
                "whether or not the actions are allowed by the policy. "
                "If you are concerned about this, please review this specific policy manually."
            )
        elif "Action" in modified_policy["Statement"]:
            if isinstance(modified_policy["Statement"]["Action"], list):
                modified_policy["Statement"]["Action"].clear()
                modified_policy["Statement"]["Action"].extend(expanded_actions)
            elif isinstance(modified_policy["Statement"]["Action"], str):
                modified_policy["Statement"]["Action"] = []
    # Otherwise it will be a list of Sids
    elif isinstance(modified_policy["Statement"], list):
        for statement in modified_policy["Statement"]:
            requested_actions = get_actions_from_statement(statement)
            expanded_actions = determine_actions_to_expand(
                requested_actions
            )
            if "NotAction" in statement:
                if isinstance(statement["NotAction"], list):
                    statement["NotAction"].clear()
                    statement["NotAction"].extend(expanded_actions)
                elif isinstance(statement["NotAction"], str):
                    statement["NotAction"] = []
                logger.warning(
                    "NotAction is in the statement. Policy Sentry will expand any wildcard actions "
                    "that are in the NotAction list, but it will not factor the NotAction actions into any analysis "
                    "about whether or not the actions are allowed by the policy."
                    "If you are concerned about this, please review this specific policy manually."
                )
            elif "Action" in statement:
                if isinstance(statement["Action"], list):
                    statement["Action"].clear()
                elif isinstance(statement["Action"], str):
                    statement["Action"] = []
                statement["Action"].extend(expanded_actions)
    else:
        logger.critical("Unknown error: The 'Statement' is neither a dict nor a list")
    return modified_policy
