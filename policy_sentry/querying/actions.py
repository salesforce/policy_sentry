"""
Methods that execute specific queries against the SQLite database for the ACTIONS table.
This supports the policy_sentry query functionality
"""
from sqlalchemy import and_
from policy_sentry.shared.database import ActionTable
from policy_sentry.util.actions import get_full_action_name
from policy_sentry.util.access_levels import transform_access_level_text


def get_actions_for_service(db_session, service):
    """
    Get a list of available actions per AWS service

    :param db_session: SQLAlchemy database session object
    :param service: An AWS service prefix, like `s3` or `kms`
    :return: A list of actions
    """
    results = []
    rows = db_session.query(ActionTable.service, ActionTable.name).filter(
        ActionTable.service.like(service))
    for row in rows:
        action = row.service + ':' + row.name
        if action not in results:
            results.append(action)
    return results


def get_action_data(db_session, service, name):
    """
    Get details about an IAM Action in JSON format.

    :param db_session: SQLAlchemy database session object
    :param service: An AWS service prefix, like `s3` or `kms`
    :param name: The name of an AWS IAM action, like `GetObject`.
    :return: A dictionary containing metadata about an IAM Action.
    """
    rows = db_session.query(ActionTable).filter(
        and_(ActionTable.service.ilike(service), ActionTable.name.ilike(name)))

    action_table_results = {}
    results = []

    for row in rows:
        action = row.service + ':' + row.name
        if row.condition_keys:
            condition_keys = row.condition_keys.split(",")
        else:
            condition_keys = None
        if row.dependent_actions:
            dependent_actions = row.dependent_actions.split(",")
        else:
            dependent_actions = None
        temp_dict = {
            "action": action,
            "description": row.description,
            "access_level": row.access_level,
            "resource_arn_format": row.resource_arn_format,
            "condition_keys": condition_keys,
            "dependent_actions": dependent_actions
        }
        results.append(temp_dict)

    action_table_results[service] = results
    return action_table_results


def get_actions_that_support_wildcard_arns_only(db_session, service):
    """
    Get a list of actions that do not support restricting the action to resource ARNs.

    :param db_session: SQLAlchemy database session object
    :param service: A single AWS service prefix, like `s3` or `kms`
    :return: A list of actions
    """
    actions_list = []
    rows = db_session.query(ActionTable.service, ActionTable.name).filter(and_(
        ActionTable.service.ilike(service),
        ActionTable.resource_arn_format.like("*"),
        ActionTable.name.notin_(db_session.query(ActionTable.name).filter(
            ActionTable.resource_arn_format.notlike('*')))
    ))
    for row in rows:
        actions_list.append(get_full_action_name(row.service, row.name))
    return actions_list


def get_actions_with_access_level(db_session, service, access_level):
    """
    Get a list of actions in a service under different access levels.

    :param db_session: SQLAlchemy database session object
    :param service: A single AWS service prefix, like `s3` or `kms`
    :param access_level: An access level as it is written in the database, such as 'Read', 'Write', 'List', 'Permisssions Management', or 'Tagging'

    :return: A list of actions
    """
    actions_list = []
    rows = db_session.query(ActionTable).filter(and_(
        ActionTable.service.like(service),
        ActionTable.access_level.ilike(access_level)
    ))
    # Create a list of actions under each service. Use this list to pass in to the remove_actions_not_matching_access_level function
    # which will give you the list of actions you want.
    for row in rows:
        action = get_full_action_name(row.service, row.name)
        if action not in actions_list:
            actions_list.append(action)
    return actions_list


def get_actions_with_arn_type_and_access_level(db_session, service, resource_type_name, access_level):
    """
    Get a list of actions in a service under different access levels, specific to an ARN format.

    :param db_session: SQLAlchemy database session object
    :param service: A single AWS service prefix, like `s3` or `kms`
    :param resource_type_name: The ARN type name, like `bucket` or `key`
    :return: A list of actions
    """
    actions_list = []
    rows = db_session.query(ActionTable).filter(and_(
        ActionTable.service.ilike(service),
        ActionTable.resource_type_name.ilike(resource_type_name),
        ActionTable.access_level.ilike(access_level)
    ))
    for row in rows:
        action = get_full_action_name(row.service, row.name)
        if action not in actions_list:
            actions_list.append(action)
    return actions_list


def get_actions_matching_condition_key(db_session, service, condition_key):
    """
    Get a list of actions under a service that allow the use of a specified condition key

    :param db_session: SQLAlchemy database session
    :param service: A single AWS service prefix
    :param condition_key: The condition key to look for.
    :return: A list of actions
    """
    actions_list = []
    looking_for = '%{0}%'.format(condition_key)
    if service:
        rows = db_session.query(ActionTable).filter(and_(
            ActionTable.service.ilike(service),
            ActionTable.condition_keys.ilike(looking_for)
        ))
        for row in rows:
            action = get_full_action_name(row.service, row.name)
            actions_list.append(action)
    else:
        rows = db_session.query(ActionTable).filter(and_(
            ActionTable.condition_keys.ilike(looking_for)
        ))
        for row in rows:
            action = get_full_action_name(row.service, row.name)
            actions_list.append(action)

    return actions_list


def remove_actions_not_matching_access_level(db_session, actions_list, access_level):
    """
    Given a list of actions, return a list of actions that match an access level

    :param db_session: The SQLAlchemy database session
    :param actions_list: A list of actions
    :param access_level: 'read', 'write', 'list', 'tagging', or 'permissions-management'
    :return: Updated list of actions, where the actions not matching the requested access level are removed.
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
            print(f"ValueError: {v_e} for the action {action}")
            continue
    return new_actions_list


def get_dependent_actions(db_session, actions_list):
    """
    Given a list of IAM Actions, query the database to determine if the action has dependent actions in the
    fifth column of the Resources, Actions, and Condition keys tables. If it does, add the dependent actions
    to the list, and return the updated list.

    To get dependent actions for a single given IAM action, just provide the action as a list with one item, like this:
    get_dependent_actions(db_session, ['kms:CreateCustomKeystore'])

    :param db_session: SQLAlchemy database session object
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
