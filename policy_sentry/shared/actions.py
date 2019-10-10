#!/usr/bin/env python3
from sqlalchemy import and_
from policy_sentry.shared.database import ActionTable
import sys


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
        service, action_name = action.split(':')
        action = str.lower(action)
        first_result = None  # Just to appease nosetests
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
            print("Error: Please specify the correct access level.")
            sys.exit(0)
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
    return new_actions_list


def get_service_from_action(action):
    """
    Returns the service name from a service:action combination
    :param action: ec2:DescribeInstance
    :return: ec2
    """
    service, action_name = action.split(':')
    return str.lower(service)


def get_action_name_from_action(action):
    """
    Returns the lowercase action name from a service:action combination
    :param action: ec2:DescribeInstance
    :return: describeinstance
    """
    service, action_name = action.split(':')
    return str.lower(action_name)


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
        for row in db_session.query(ActionTable).filter(and_(ActionTable.service.like(service), ActionTable.name.like(str.lower(action_name)))):
            # Just take the first result
            if 1 == 1:
                first_result = row.dependent_actions

        # We store the blank result as the literal string 'None' instead of Null.
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
            # If there is no comma, there is just one dependent action in the database
            else:
                # Add the action used for the current iteration of the loop
                new_actions_list.append(action)
                # Add the dependent action. Transform tuple to list
                new_actions_list.append(str.lower(first_result))
        else:
            new_actions_list.append(action)

    return new_actions_list
