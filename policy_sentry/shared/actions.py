#!/usr/bin/env python3
from sqlalchemy import and_
from policy_sentry.shared.database import ActionTable
from policy_sentry.shared.file import read_yaml_file
import sys
import json
import os
import copy
from pathlib import Path


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


def get_actions_from_json_policy_file(json_file):
    """
    read the json policy file and return a list of actions
    """

    # FIXME use a try/expect here to validate the json file. I would create a generic json
    with open(json_file) as json_file:
        # validation function/parser as there is a lot of json floating around in this tool. [MJ]
        data = json.load(json_file)
        actions_list = []
        # Multiple statements are in the 'Statement' list
        for i in range(len(data['Statement'])):
            try:
                if isinstance(data['Statement'], dict):
                    try:

                        if isinstance(data['Statement']['Action'], str):
                            actions_list.append(data['Statement']['Action'])
                        elif isinstance(data['Statement']['Action'], list):
                            actions_list.extend(data['Statement']['Action'])
                        else:
                            print("Unknown error: The 'Action' is neither a list nor a string")
                            continue
                    except KeyError as e:
                        print(e)
                        exit()
                elif isinstance(data['Statement'], list):
                    try:
                        if isinstance(data['Statement'][i]['Action'], str):
                            actions_list.append(data['Statement'][i]['Action'])
                        elif isinstance(data['Statement'][i]['Action'], list):
                            actions_list.extend(data['Statement'][i]['Action'])
                        else:
                            print("Unknown error: The 'Action' is neither a list nor a string")
                            exit()
                    except KeyError as e:
                        print(e)
                        exit()
                else:
                    print("Unknown error: The 'Action' is neither a list nor a string")
                    exit()
            except TypeError as e:
                print(e)
                exit()
    try:
        actions_list = [x.lower() for x in actions_list]
    except AttributeError:
        print(actions_list)
        print("AttributeError: 'list' object has no attribute 'lower'")
    actions_list.sort()
    return actions_list

