from sqlalchemy import and_
from policy_sentry.shared.database import ActionTable, ArnTable, ConditionTable
from policy_sentry.shared.actions import get_actions_by_access_level, get_full_action_name
from policy_sentry.shared.actions import get_service_from_action, get_action_name_from_action


# Per service
def query_condition_table(db_session, service):
    """Get a list of available conditions per AWS service"""
    results = []
    rows = db_session.query(ConditionTable.condition_key_name, ConditionTable.condition_value_type,
                            ConditionTable.description).filter(ConditionTable.service.like(service))
    for row in rows:
        results.append(str(row.condition_key_name))
    return results


# Per condition key name
def query_condition_table_by_name(db_session, service, condition_key_name):
    """Get details about a specific condition key in JSON format"""
    rows = db_session.query(ConditionTable.condition_key_name, ConditionTable.condition_value_type,
                            ConditionTable.description).filter(and_(ConditionTable.condition_key_name.like(condition_key_name), ConditionTable.service.like(service)))
    result = rows.first()
    output = {
        'name': result.condition_key_name,
        'description': result.description,
        'condition_value_type': result.condition_value_type
    }
    return output


def query_arn_table_for_raw_arns(db_session, service):
    """Get a list of available raw ARNs per AWS service"""
    results = []
    rows = db_session.query(ArnTable.raw_arn).filter(ArnTable.service.like(service))
    for row in rows:
        results.append(str(row.raw_arn))
    return results


def query_arn_table_for_arn_types(db_session, service):
    """Get a list of available ARN short names per AWS service"""
    results = {}
    rows = db_session.query(ArnTable.resource_type_name, ArnTable.raw_arn).filter(ArnTable.service.like(service))
    for row in rows:
        results[row.resource_type_name] = row.raw_arn
    return results


def query_arn_table_by_name(db_session, service, name):
    """Get details about a resource ARN type name in JSON format."""
    rows = db_session.query(ArnTable).filter(
        ArnTable.resource_type_name.like(name), ArnTable.service.like(service))
    result = rows.first()
    if result.condition_keys:
        condition_keys = result.condition_keys.split(",")
    else:
        condition_keys = None
    output = {
        'resource_type_name': result.resource_type_name,
        'raw_arn': result.raw_arn,
        'condition_keys': condition_keys
        # TODO: After #33 is fixed, add the items from the condition keys column here.
    }
    return output


def query_action_table(db_session, service):
    """Get a list of available actions per AWS service"""
    results = []
    rows = db_session.query(ActionTable.service, ActionTable.name).filter(ActionTable.service.like(service))
    for row in rows:
        action = row.service + ':' + row.name
        if action not in results:
            results.append(action)
    return results


def query_action_table_by_name(db_session, service, name):
    """Get details about an IAM Action in JSON format."""
    rows = db_session.query(ActionTable).filter(and_(ActionTable.service.ilike(service), ActionTable.name.ilike(name)))

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


def query_action_table_for_actions_supporting_wildcards_only(db_session, service):
    actions_list = []
    rows = db_session.query(ActionTable.service, ActionTable.name).filter(and_(
        ActionTable.service.ilike(service),
        ActionTable.resource_arn_format.like("*"),
        ActionTable.name.notin_(db_session.query(ActionTable.name).filter(ActionTable.resource_arn_format.notlike('*')))
    ))
    for row in rows:
        actions_list.append(get_full_action_name(row.service, row.name))
    return actions_list


def query_action_table_by_access_level(db_session, service, access_level):
    """Get a list of actions in a service under different access levels."""
    actions_list = []
    rows = db_session.query(ActionTable).filter(and_(
        ActionTable.service.like(service),
        ActionTable.access_level.ilike(access_level)
    ))
    # Create a list of actions under each service. Use this list to pass in to the get_actions_by_access_level function
    # which will give you the list of actions you want.
    for row in rows:
        action = get_full_action_name(row.service, row.name)
        if action not in actions_list:
            actions_list.append(action)
    return actions_list


def query_action_table_by_arn_type_and_access_level(db_session, service, resource_type_name, access_level):
    """Get a list of actions in a service under different access levels, specific to an ARN format."""
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


def query_action_table_for_all_condition_key_matches(db_session, service, condition_key):
    results = []
    looking_for = '%{0}%'.format(condition_key)
    if service:
        rows = db_session.query(ActionTable).filter(and_(
            ActionTable.service.ilike(service),
            ActionTable.condition_keys.ilike(looking_for)
        ))
        for row in rows:
            action = get_full_action_name(row.service, row.name)
            results.append(action)
    else:
        rows = db_session.query(ActionTable).filter(and_(
            ActionTable.condition_keys.ilike(looking_for)
        ))
        for row in rows:
            action = get_full_action_name(row.service, row.name)
            results.append(action)

    return results


def remove_actions_that_are_not_wildcard_arn_only(db_session, actions_list):
    # remove duplicates, if there are any
    actions_list_unique = list(dict.fromkeys(actions_list))
    actions_list_placeholder = []
    for action in actions_list_unique:
        service = get_service_from_action(action)
        action_name = get_action_name_from_action(action)

        rows = db_session.query(ActionTable.service, ActionTable.name).filter(and_(
            ActionTable.service.ilike(service),
            ActionTable.name.ilike(action_name),
            ActionTable.resource_arn_format.like("*"),
            ActionTable.name.notin_(
                db_session.query(ActionTable.name).filter(ActionTable.resource_arn_format.notlike('*')))
        ))
        for row in rows:
            if row.service == service and row.name == action_name:
                actions_list_placeholder.append(get_full_action_name(service, action_name))
    return actions_list_placeholder
