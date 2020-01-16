"""
Methods that execute specific queries against the SQLite database for the CONDITIONS table.
This supports the policy_sentry query functionality
"""
from sqlalchemy import and_
from policy_sentry.shared.database import ConditionTable


# Per service
def get_condition_keys_for_service(db_session, service):
    """
    Get a list of available conditions per AWS service

    :param db_session: SQLAlchemy database session object
    :param service: An AWS service prefix, like `s3` or `kms`
    :return: A list of condition keys
    """
    results = []
    rows = db_session.query(ConditionTable.condition_key_name, ConditionTable.condition_value_type,
                            ConditionTable.description).filter(ConditionTable.service.like(service))
    for row in rows:
        results.append(str(row.condition_key_name))
    return results


# Per condition key name
def get_condition_key_details(db_session, service, condition_key_name):
    """
    Get details about a specific condition key in JSON format

    :param db_session: SQLAlchemy database session object
    :param service: An AWS service prefix, like `ec2` or `kms`
    :param condition_key_name: The name of a condition key, like `ec2:Vpc`
    :return: Metadata about the condition key
    """
    rows = db_session.query(ConditionTable.condition_key_name, ConditionTable.condition_value_type,
                            ConditionTable.description).filter(and_(ConditionTable.condition_key_name.like(condition_key_name), ConditionTable.service.like(service)))
    result = rows.first()
    output = {
        'name': result.condition_key_name,
        'description': result.description,
        'condition_value_type': result.condition_value_type
    }
    return output

