"""A few methods for parsing policies."""
import json
import logging
from policy_sentry.querying.actions import get_action_data

logger = logging.getLogger(__name__)


def get_actions_from_statement(statement):
    """Given a statement dictionary, create a list of the actions"""
    actions_list = []
    # We only want to evaluate policies that have Effect = "Allow"
    if statement.get("Effect") == "Deny":
        return actions_list
    else:
        action_clause = statement.get("Action")
        if not action_clause:
            logger.debug("No actions contained in statement")
            return actions_list
        # Action = "s3:GetObject"
        if isinstance(action_clause, str):
            actions_list.append(action_clause)
        # Action = ["s3:GetObject", "s3:ListBuckets"]
        elif isinstance(action_clause, list):
            actions_list.extend(action_clause)
        else:
            logger.debug("Unknown error: The 'Action' is neither a list nor a string")
    return actions_list


# pylint: disable=too-many-branches,too-many-statements
def get_actions_from_policy(db_session, data):
    """Given a policy dictionary, create a list of the actions"""
    actions_list = []
    statement_clause = data.get("Statement")
    # Statement must be a dict if it's a single statement. Otherwise it will be a list of statements
    if isinstance(statement_clause, dict):
        actions_list.extend(get_actions_from_statement(statement_clause))
    # Otherwise it will be a list of Sids
    elif isinstance(statement_clause, list):
        for statement in data["Statement"]:
            actions_list.extend(get_actions_from_statement(statement))
    else:
        logger.critical("Unknown error: The 'Statement' is neither a dict nor a list")
    actions_list = [x.lower() for x in actions_list]

    new_actions_list = []
    if db_session:
        for action in actions_list:
            service, action_name = action.split(":")
            action_data = get_action_data(db_session, service, action_name)
            if service in action_data.keys():
                if len(action_data[service]) > 0:
                    new_actions_list.append(action_data[service][0]["action"])

        new_actions_list.sort()
        return new_actions_list
    else:
        actions_list.sort()
        return actions_list


# pylint: disable=too-many-branches,too-many-statements
def get_actions_from_json_policy_file(db_session, file):
    """
    read the json policy file and return a list of actions
    """

    # FIXME use a try/expect here to validate the json file. I would create a generic json
    try:
        with open(file) as json_file:
            # validation function/parser as there is a lot of json floating around
            # in this tool. [MJ]
            data = json.load(json_file)
            actions_list = get_actions_from_policy(db_session, data)

    except:  # pylint: disable=bare-except
        logger.debug("General Error at get_actions_from_json_policy_file.")
        actions_list = []
    return actions_list
