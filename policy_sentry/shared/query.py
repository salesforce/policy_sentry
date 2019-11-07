from sqlalchemy import and_
from policy_sentry.shared.database import ActionTable, ArnTable, ConditionTable


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


def query_arn_table(db_session, service):
    """Get a list of available ARNs per AWS service"""
    results = []
    rows = db_session.query(ArnTable.raw_arn).filter(ArnTable.service.like(service))
    for row in rows:
        results.append(str(row.raw_arn))
    return results


def query_arn_table_by_name(db_session, service, name):
    """Get details about a resource ARN type name in JSON format."""
    rows = db_session.query(ArnTable.resource_type_name, ArnTable.raw_arn).filter(
        ArnTable.resource_type_name.like(name), ArnTable.service.like(service))
    result = rows.first()
    output = {
        'resource_type_name': result.resource_type_name,
        'raw_arn': result.raw_arn
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
    # TODO: Before submitting #29, Throw an error if it doesn't match. This is likely because the user is likely to
    #  provide `service:action_name` as the name at first, and we want to direct them to just use the action name.

    # TODO: Before submitting #29, Handle cases where the actions match multiple times - for example,
    #  there are multiple entries for ram:TagResource due to the two different ARN formats.
    action_table_results = {}
    results = []

    for row in rows:
        action = row.service + ':' + row.name
        # if row.condition_keys: # TODO: Split the condition keys based on commas.
        # if row.dependent_actions: # TODO: Split the dependent actions based on commas.
        # if row.dependent_actions is None:
        #     # We have to do this otherwise the output will officially be "dependent_actions": null
        #     dependent_actions = None
        # else:
        #     dependent_actions = row.dependent_actions
        temp_dict = {
            "action": action,
            "description": row.description,
            "access_level": row.access_level,
            "resource_arn_format": row.resource_arn_format,
            "condition_keys": row.condition_keys,
            "dependent_actions": row.dependent_actions
        }
        results.append(temp_dict)

    action_table_results[service] = results
    return action_table_results
