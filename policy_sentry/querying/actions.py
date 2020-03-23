"""
Methods that execute specific queries against the SQLite database for the ACTIONS table.
This supports the policy_sentry query functionality
"""
import logging
from sqlalchemy import and_
from policy_sentry.shared.database import ActionTable
from policy_sentry.querying.all import get_all_service_prefixes
from policy_sentry.util.actions import get_full_action_name
from policy_sentry.util.arns import get_service_from_arn
from policy_sentry.util.access_levels import transform_access_level_text

logger = logging.getLogger(__name__)


def get_actions_for_service(db_session, service):
    """
    Get a list of available actions per AWS service

    :param db_session: SQLAlchemy database session object
    :param service: An AWS service prefix, like `s3` or `kms`
    :return: A list of actions
    """
    results = []
    rows = db_session.query(ActionTable.service, ActionTable.name).filter(
        ActionTable.service.like(service)
    )
    for row in rows:
        action = row.service + ":" + row.name
        if action not in results:
            results.append(action)
    return results


def get_action_data(db_session, service, name):
    """
    Get details about an IAM Action in JSON format.

    :param db_session: SQLAlchemy database session object
    :param service: An AWS service prefix, like `s3` or `kms`. Case insensitive.
    :param name: The name of an AWS IAM action, like `GetObject`. To get data about all actions in a service, specify "*". Case insensitive.
    :return: A dictionary containing metadata about an IAM Action.
    """
    if name == "*":
        rows = db_session.query(ActionTable).filter(ActionTable.service.ilike(service))
    else:
        rows = db_session.query(ActionTable).filter(
            and_(ActionTable.service.ilike(service), ActionTable.name.ilike(name))
        )
    action_table_results = {}
    results = []

    for row in rows:
        action = row.service + ":" + row.name
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
            "dependent_actions": dependent_actions,
        }
        results.append(temp_dict)

    action_table_results[service] = results
    return action_table_results


def get_actions_that_support_wildcard_arns_only(db_session, service):
    """
    Get a list of actions that do not support restricting the action to resource ARNs.
    Set service to "all" to get a list of actions across all services.

    :param db_session: SQLAlchemy database session object
    :param service: A single AWS service prefix, like `s3` or `kms`
    :return: A list of actions
    """
    actions_list = []
    if service == "all":
        rows = db_session.query(ActionTable.service, ActionTable.name).filter(
            and_(
                ActionTable.resource_arn_format.like("*"),
                ActionTable.name.notin_(
                    db_session.query(ActionTable.name).filter(
                        ActionTable.resource_arn_format.notlike("*")
                    )
                ),
            )
        )
    else:
        rows = db_session.query(ActionTable.service, ActionTable.name).filter(
            and_(
                ActionTable.service.ilike(service),
                ActionTable.resource_arn_format.like("*"),
                ActionTable.name.notin_(
                    db_session.query(ActionTable.name).filter(
                        ActionTable.resource_arn_format.notlike("*")
                    )
                ),
            )
        )
    for row in rows:
        actions_list.append(get_full_action_name(row.service, row.name))
    return actions_list


def get_actions_at_access_level_that_support_wildcard_arns_only(
    db_session, service, access_level
):
    """
    Get a list of actions at an access level that do not support restricting the action to resource ARNs.
    Set service to "all" to get a list of actions across all services.

    :param db_session: SQLAlchemy database session object
    :param service: A single AWS service prefix, like `s3` or `kms`
    :param access_level: An access level as it is written in the database, such as 'Read', 'Write', 'List', 'Permisssions management', or 'Tagging'
    :return: A list of actions
    """
    actions_list = []
    if service == "all":
        rows = db_session.query(ActionTable.service, ActionTable.name).filter(
            and_(
                ActionTable.resource_arn_format.like("*"),
                ActionTable.access_level.ilike(access_level),
                ActionTable.name.notin_(
                    db_session.query(ActionTable.name).filter(
                        ActionTable.resource_arn_format.notlike("*")
                    )
                ),
            )
        )
    else:
        rows = db_session.query(ActionTable.service, ActionTable.name).filter(
            and_(
                ActionTable.service.ilike(service),
                ActionTable.resource_arn_format.like("*"),
                ActionTable.access_level.ilike(access_level),
                ActionTable.name.notin_(
                    db_session.query(ActionTable.name).filter(
                        ActionTable.resource_arn_format.notlike("*")
                    )
                ),
            )
        )
    for row in rows:
        actions_list.append(get_full_action_name(row.service, row.name))
    return actions_list


def get_actions_with_access_level(db_session, service, access_level):
    """
    Get a list of actions in a service under different access levels.

    :param db_session: SQLAlchemy database session object
    :param service: A single AWS service prefix, like `s3` or `kms`
    :param access_level: An access level as it is written in the database, such as 'Read', 'Write', 'List', 'Permisssions management', or 'Tagging'

    :return: A list of actions
    """
    actions_list = []
    all_services = get_all_service_prefixes(db_session)
    if service == "all":
        for serv in all_services:
            output = get_actions_with_access_level(db_session, serv, access_level)
            actions_list.extend(output)
    rows = db_session.query(ActionTable).filter(
        and_(
            ActionTable.service.like(service),
            ActionTable.access_level.ilike(access_level),
        )
    )
    # Create a list of actions under each service. Use this list to pass in to the remove_actions_not_matching_access_level function
    # which will give you the list of actions you want.
    for row in rows:
        action = get_full_action_name(row.service, row.name)
        if action not in actions_list:
            actions_list.append(action)
    return actions_list


def get_actions_with_arn_type_and_access_level(
    db_session, service, resource_type_name, access_level
):
    """
    Get a list of actions in a service under different access levels, specific to an ARN format.

    :param db_session: SQLAlchemy database session object
    :param service: A single AWS service prefix, like `s3` or `kms`
    :param resource_type_name: The ARN type name, like `bucket` or `key`
    :return: A list of actions
    """
    actions_list = []
    rows = db_session.query(ActionTable).filter(
        and_(
            ActionTable.service.ilike(service),
            ActionTable.resource_type_name.ilike(resource_type_name),
            ActionTable.access_level.ilike(access_level),
        )
    )
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
    looking_for = "%{0}%".format(condition_key)
    if service:
        rows = db_session.query(ActionTable).filter(
            and_(
                ActionTable.service.ilike(service),
                ActionTable.condition_keys.ilike(looking_for),
            )
        )
        for row in rows:
            action = get_full_action_name(row.service, row.name)
            actions_list.append(action)
    else:
        rows = db_session.query(ActionTable).filter(
            and_(ActionTable.condition_keys.ilike(looking_for))
        )
        for row in rows:
            action = get_full_action_name(row.service, row.name)
            actions_list.append(action)

    return actions_list


def get_actions_matching_condition_crud_and_arn(
    db_session, condition_key, access_level, raw_arn
):
    """
    Get a list of IAM Actions matching a condition key, CRUD level, and raw ARN format.

    :param db_session: SQL Alchemy database session
    :param condition_key: A condition key, like aws:TagKeys
    :param access_level: Access level that matches the database value. "Read", "Write", "List", "Tagging", or "Permissions management"
    :param raw_arn: The raw ARN format in the database, like arn:${Partition}:s3:::${BucketName}
    :return: List of IAM Actions
    """
    actions_list = []
    looking_for = "%{0}%".format(condition_key)
    if raw_arn == "*":
        rows = db_session.query(ActionTable).filter(
            and_(
                # ActionTable.service.ilike(service),
                ActionTable.access_level.ilike(access_level),
                ActionTable.resource_arn_format.is_(raw_arn),
                ActionTable.condition_keys.ilike(looking_for),
            )
        )
    else:
        service = get_service_from_arn(raw_arn)
        rows = db_session.query(ActionTable).filter(
            and_(
                ActionTable.service.ilike(service),
                ActionTable.access_level.ilike(access_level),
                ActionTable.resource_arn_format.ilike(raw_arn),
                ActionTable.condition_keys.ilike(looking_for),
            )
        )

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
            service, action_name = action.split(":")
            first_result = None  # Just to appease nosetests
            level = transform_access_level_text(access_level)
            query_actions_access_level = db_session.query(ActionTable).filter(
                and_(
                    ActionTable.service.ilike(service),
                    ActionTable.name.ilike(action_name),
                    ActionTable.access_level.ilike(level),
                )
            )
            first_result = query_actions_access_level.first()
            if first_result is None:
                pass
            else:
                # Just take the first result
                new_actions_list.append(f"{first_result.service}:{first_result.name}")
        except ValueError as v_e:
            logger.debug("ValueError: %s for the action %s", v_e, action)
            continue
    return new_actions_list


def get_dependent_actions(db_session, actions_list):
    """
    Given a list of IAM Actions, query the database to determine if the action has dependent actions in the
    fifth column of the Resources, Actions, and Condition keys tables. If it does, add the dependent actions
    to the list, and return the updated list.

    It includes the original action in there as well. So, if you supply kms:CreateCustomKeyStore, it will give you kms:CreateCustomKeyStore as well as cloudhsm:DescribeClusters

    To get dependent actions for a single given IAM action, just provide the action as a list with one item, like this:
    get_dependent_actions(db_session, ['kms:CreateCustomKeystore'])

    :param db_session: SQLAlchemy database session object
    :param actions_list: A list of actions to use in querying the database for dependent actions
    :return: Updated list of actions, including dependent actions if applicable.
    """
    new_actions_list = []
    for action in actions_list:
        service, action_name = action.split(":")
        rows = get_action_data(db_session, service, action_name)
        for row in rows[service]:
            if row["dependent_actions"] is not None:
                # new_actions_list.append(action)
                # dependent_actions = [x.lower() for x in row["dependent_actions"]]
                new_actions_list.extend(row["dependent_actions"])

    new_actions_list = list(dict.fromkeys(new_actions_list))
    return new_actions_list


def remove_actions_that_are_not_wildcard_arn_only(db_session, actions_list):
    """
    Given a list of actions, remove the ones that CAN be restricted to ARNs, leaving only the ones that cannot.

    :param db_session: SQL Alchemy database session object
    :param actions_list: A list of actions
    :return: An updated list of actions
    :rtype: list
    """
    # remove duplicates, if there are any
    actions_list_unique = list(dict.fromkeys(actions_list))
    actions_list_placeholder = []
    for action in actions_list_unique:
        service_name, action_name = action.split(":")

        rows = db_session.query(ActionTable.service, ActionTable.name).filter(
            and_(
                ActionTable.service.ilike(service_name),
                ActionTable.name.ilike(action_name),
                ActionTable.resource_arn_format.like("*"),
                ActionTable.name.notin_(
                    db_session.query(ActionTable.name).filter(
                        ActionTable.resource_arn_format.notlike("*")
                    )
                ),
            )
        )
        for row in rows:
            if (
                row.service.lower() == service_name.lower()
                and row.name.lower() == action_name.lower()
            ):
                actions_list_placeholder.append(f"{row.service}:{row.name}")
    return actions_list_placeholder
