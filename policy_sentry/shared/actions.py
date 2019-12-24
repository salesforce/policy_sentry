"""
Functions to support:
* querying the actions table in the database based on different criteria.
* Transforming lists of actions in various ways required for writing policies
"""
import json
import sys
import logging
from sqlalchemy import and_
from policy_sentry.shared.database import ActionTable

logging.basicConfig()
logger = logging.getLogger(__name__)


def get_all_actions(db_session):
    """
    Gets a huge list of all IAM actions. This is used as part of the policyuniverse approach to minimizing
    IAM Policies to meet AWS-mandated character limits on policies.
    """
    all_actions = set()
    rows = db_session.query(ActionTable.service, ActionTable.name).distinct(
        and_(ActionTable.service, ActionTable.name))
    for row in rows:
        all_actions.add(str(row.service + ":" + row.name))
    # Remove duplicates
    # all_actions = set(dict.fromkeys(all_actions))
    return all_actions


def get_all_services_from_action_table(db_session):
    """
    Gets all the services from the actions table
    :param db_session: The SQLAlchemy database session
    :return: service_prefixes: A list of all AWS service prefixes present in the table.
    """
    service_prefixes = []
    rows = db_session.query(ActionTable.service).distinct(ActionTable.service)
    for row in rows:
        if row.service not in service_prefixes:
            service_prefixes.append(row.service)
    # Remove duplicates
    service_prefixes = list(dict.fromkeys(
        service_prefixes))  # remove duplicates
    service_prefixes.sort()
    return service_prefixes


def get_actions_by_access_level(db_session, actions_list, access_level):
    """
    Given a list of actions, return a list of actions that match an access level
    :param db_session: The SQLAlchemy database session
    :param actions_list: A list of actions
    :param access_level: read, write, list, tagging, or permissions-management
    :return:
    """

    new_actions_list = []
    for action in actions_list:
        try:
            service, action_name = action.split(':')
            action = str.lower(action)
            first_result = None  # Just to appease nosetests
            level = transform_access_level_text(access_level)
            query_actions_access_level = db_session.query(ActionTable).filter(
                and_(ActionTable.service.like(service),
                     ActionTable.name.like(str.lower(action_name)),
                     ActionTable.access_level.like(level)
                     ))
            first_result = query_actions_access_level.first()
            if first_result is None:
                pass
            else:
                # Just take the first result
                new_actions_list.append(action)
        except ValueError as v_e:
            logger.debug(f"ValueError: {v_e} for the action {action}")
            continue
    return new_actions_list


def transform_access_level_text(access_level):
    """This takes the Click choices for access levels, like permissions-management, and
    returns the text format matching that access level, but in the format that SQLite database expects"""
    if access_level == "read":
        level = "Read"
    elif access_level == "write":
        level = "Write"
    elif access_level == "list":
        level = "List"
    elif access_level == "tagging":
        level = "Tagging"
    elif access_level == "permissions-management":
        level = "Permissions management"
    else:
        logger.debug("Error: Please specify the correct access level.")
        sys.exit(0)
    return level


def get_service_from_action(action):
    """
    Returns the service name from a service:action combination
    :param action: ec2:DescribeInstance
    :return: ec2
    """
    service, action_name = action.split(':')  # pylint: disable=unused-variable
    return str.lower(service)


def get_action_name_from_action(action):
    """
    Returns the lowercase action name from a service:action combination
    :param action: ec2:DescribeInstance
    :return: describeinstance
    """
    service, action_name = action.split(':')  # pylint: disable=unused-variable
    return str.lower(action_name)


def get_lowercase_action_list(action_list):
    """
    Given a list of actions, return the list but in lowercase format
    """
    new_action_list = []
    for action in action_list:
        new_action_list.append(str.lower(action))
    return new_action_list


def get_full_action_name(service, action_name):
    """
    Gets the proper formatting for an action - the service, plus colon, plus action name.
    :param service: service name, like s3
    :param action_name: action name, like createbucket
    :return: the resulting string
    """
    action = service + ':' + action_name
    return action


def get_dependent_actions(db_session, actions_list):
    """
    Given a list of IAM Actions, query the database to determine if the action has dependent actions in the
    fifth column of the Resources, Actions, and Condition keys tables. If it does, add the dependent actions
    to the list, and return the updated list.
    :param db_session: SQLAlchemy database session
    :param actions_list: A list of actions to use in querying the database for dependent actions
    :return: Updated list of actions, including dependent actions if applicable.
    """
    new_actions_list = []
    for action in actions_list:
        service, action_name = action.split(':')
        action = str.lower(action)
        first_result = None  # Just to appease nosetests
        for row in db_session.query(ActionTable).filter(and_(ActionTable.service.like(service),
                                                             ActionTable.name.like(str.lower(action_name)))):
            # Just take the first result
            if 1 == 1:  # pylint: disable=comparison-with-itself
                first_result = row.dependent_actions

        # We store the blank result as the literal string 'None' instead of
        # Null.
        if first_result is None:
            new_actions_list.append(action)
        elif first_result is not None:
            # Comma means there are multiple dependent actions
            if ',' in first_result:
                split_result = first_result.split(',')
                for i in range(len(split_result)):
                    temp = split_result[i]
                    split_result[i] = str.lower(temp)
                # Add the action used for the current iteration of the loop
                new_actions_list.append(action)
                # Add the dependent actions. Transform tuple to list
                new_actions_list.extend(split_result)
            # If there is no comma, there is just one dependent action in the
            # database
            else:
                # Add the action used for the current iteration of the loop
                new_actions_list.append(action)
                # Add the dependent action. Transform tuple to list
                new_actions_list.append(str.lower(first_result))
        else:
            new_actions_list.append(action)

    return new_actions_list


# pylint: disable=too-many-branches,too-many-statements
def get_actions_from_policy(data):
    """Given a policy, create a list of the actions"""
    actions_list = []
    # Multiple statements are in the 'Statement' list
    # pylint: disable=too-many-nested-blocks
    for i in range(len(data['Statement'])):
        try:
            # Statement must be a dict if it's a single statement. Otherwise it will be a list of statements
            if isinstance(data['Statement'], dict):
                # We only want to evaluate policies that have Effect = "Allow"
                # pylint: disable=no-else-continue, literal-comparison
                if data['Statement']['Effect'] is 'Deny':
                    continue
                else:
                    try:
                        # Action = "s3:GetObject"
                        if isinstance(data['Statement']['Action'], str):
                            actions_list.append(
                                data['Statement']['Action'])
                        # Action = ["s3:GetObject", "s3:ListBuckets"]
                        elif isinstance(data['Statement']['Action'], list):
                            actions_list.extend(
                                data['Statement']['Action'])
                        elif 'Action' not in data['Statement']:
                            logger.debug(
                                'Action is not a key in the statement')
                        else:
                            logger.debug(
                                "Unknown error: The 'Action' is neither a list nor a string")
                    except KeyError as k_e:
                        logger.critical(
                            f"KeyError at get_actions_from_policy {k_e}")
                        exit()

            # Otherwise it will be a list of Sids
            elif isinstance(data['Statement'], list):
                # We only want to evaluate policies that have Effect = "Allow"
                try:
                    if data['Statement'][i]['Effect'] == 'Deny':
                        continue
                    else:
                        if 'Action' in data['Statement'][i]:
                            if isinstance(data['Statement'][i]['Action'], str):
                                actions_list.append(
                                    data['Statement'][i]['Action'])
                            elif isinstance(data['Statement'][i]['Action'], list):
                                actions_list.extend(
                                    data['Statement'][i]['Action'])
                            elif data['Statement'][i]['NotAction'] and not data['Statement'][i]['Action']:
                                logger.debug('Skipping due to NotAction')
                            else:
                                logger.critical(
                                    "Unknown error: The 'Action' is neither a list nor a string")
                                exit()
                        else:
                            continue
                except KeyError as k_e:
                    logger.critical(
                        f"KeyError at get_actions_from_policy {k_e}")
                    exit()
            else:
                logger.critical(
                    "Unknown error: The 'Action' is neither a list nor a string")
                # exit()
        except TypeError as t_e:
            logger.critical(f"TypeError at get_actions_from_policy {t_e}")
            exit()
    try:
        actions_list = [x.lower() for x in actions_list]
    except AttributeError as a_e:
        logger.debug(actions_list)
        logger.debug(f"AttributeError: {a_e}")
    actions_list.sort()
    return actions_list


# pylint: disable=too-many-branches,too-many-statements
def get_actions_from_json_policy_file(file):
    """
    read the json policy file and return a list of actions
    """

    # FIXME use a try/expect here to validate the json file. I would create a generic json
    try:
        with open(file) as json_file:
            # validation function/parser as there is a lot of json floating around
            # in this tool. [MJ]
            data = json.load(json_file)
            actions_list = get_actions_from_policy(data)

    except:  # pylint: disable=bare-except
        logger.debug("General Error at get_actions_from_json_policy_file.")
        actions_list = []
    return actions_list
