"""
Methods that execute specific queries against the SQLite database for the CONDITIONS table.
This supports the policy_sentry query functionality
"""
from sqlalchemy import and_
from policy_sentry.shared.database import ConditionTable, ActionTable, ArnTable
from policy_sentry.util.conditions import translate_condition_key_data_types


# Per service
def get_condition_keys_for_service(db_session, service):
    """
    Get a list of available conditions per AWS service

    :param db_session: SQLAlchemy database session object
    :param service: An AWS service prefix, like `s3` or `kms`
    :return: A list of condition keys
    """
    results = []
    rows = db_session.query(
        ConditionTable.condition_key_name,
        ConditionTable.condition_value_type,
        ConditionTable.description,
    ).filter(ConditionTable.service.like(service))
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
    rows = db_session.query(
        ConditionTable.condition_key_name,
        ConditionTable.condition_value_type,
        ConditionTable.description,
    ).filter(
        and_(
            ConditionTable.condition_key_name.like(condition_key_name),
            ConditionTable.service.like(service),
        )
    )
    result = rows.first()
    output = {
        "name": result.condition_key_name,
        "description": result.description,
        "condition_value_type": result.condition_value_type,
    }
    return output


def get_conditions_for_action_and_raw_arn(db_session, action, raw_arn):
    """
    Get a list of conditions available to an action.

    :param db_session: SQLAlchemy database session object
    :param action: The IAM action, like s3:GetObject
    :param raw_arn: The raw ARN format specific to the action
    :return:
    """
    service, action_name = action.split(":")

    if raw_arn == "*":
        rows = db_session.query(ActionTable).filter(
            and_(
                ActionTable.service.ilike(service),
                ActionTable.name.ilike(action_name),
                ActionTable.resource_arn_format.is_(raw_arn),
            )
        )
    else:
        rows = db_session.query(ActionTable).filter(
            and_(
                ActionTable.service.ilike(service),
                ActionTable.name.ilike(action_name),
                ActionTable.resource_arn_format.ilike(raw_arn),
            )
        )
    result = rows.first()
    if result.condition_keys is None:
        return False
    else:
        condition_keys_list = result.condition_keys.split(",")
        return condition_keys_list


def get_condition_keys_available_to_raw_arn(db_session, raw_arn):
    """
    Get a list of condition keys available to a RAW ARN

    :param db_session: SQLAlchemy database session object
    :param raw_arn: The value in the database, like arn:${Partition}:s3:::${BucketName}/${ObjectName}
    """
    rows = db_session.query(ArnTable).filter(ArnTable.raw_arn.like(raw_arn))
    result = rows.first()
    if result.condition_keys:
        condition_keys = result.condition_keys.split(",")
        return condition_keys
    else:
        return False


def get_condition_value_type(db_session, condition_key):
    """
    Get the data type of the condition key - like Date, String, etc.
    :param db_session: SQLAlchemy database session object
    :param condition_key: A condition key, like a4b:filters_deviceType
    :return:
    """
    rows = db_session.query(ConditionTable).filter(
        ConditionTable.condition_key_name.ilike(condition_key)
    )
    result = rows.first()
    if result is None:
        raise Exception(
            f"There is no condition key titled {condition_key}. Please provide a valid condition key. "
            f"\nYou can query available condition keys with query command, such as the following: "
            f"\n\tpolicy_sentry query condition-table --service ec2"
        )
    condition_value_type = translate_condition_key_data_types(
        result.condition_value_type
    )
    return condition_value_type
