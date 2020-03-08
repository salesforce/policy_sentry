"""
Methods that execute specific queries against the SQLite database for the ARN table.
This supports the policy_sentry query functionality
"""
from sqlalchemy import and_
from policy_sentry.shared.database import ArnTable


def get_arn_data(db_session, service, name):
    """
    Get details about ARNs in JSON format.

    :param db_session: SQLAlchemy database session object
    :param service: An AWS service prefix, like `s3` or `kms`
    :param name: The name of a resource type, like `bucket` or `object`. To get details on ALL arns in a service, specify "*" here.
    :return: Metadata about an ARN type
    """
    results = []
    arn_table_results = {}

    if name == "*":
        rows = db_session.query(ArnTable).filter(ArnTable.service.like(service))
    else:
        rows = db_session.query(ArnTable).filter(
            ArnTable.resource_type_name.like(name), ArnTable.service.like(service)
        )

    for row in rows:
        if row.condition_keys:
            condition_keys = row.condition_keys.split(",")
        else:
            condition_keys = None
        output = {
            "resource_type_name": row.resource_type_name,
            "raw_arn": row.raw_arn,
            "condition_keys": condition_keys,
        }
        results.append(output)
    arn_table_results[service] = results
    return arn_table_results


def get_raw_arns_for_service(db_session, service):
    """
    Get a list of available raw ARNs per AWS service

    :param db_session: SQLAlchemy database session object
    :param service: An AWS service prefix, like `s3` or `kms`
    :return: A list of raw ARNs
    """
    results = []
    rows = db_session.query(ArnTable.raw_arn).filter(ArnTable.service.like(service))
    for row in rows:
        results.append(str(row.raw_arn))
    return results


def get_arn_types_for_service(db_session, service):
    """
    Get a list of available ARN short names per AWS service.

    :param db_session: SQLAlchemy database session object
    :param service: An AWS service prefix, like `s3` or `kms`
    :return: A list of ARN types, like `bucket` or `object`
    """
    results = {}
    rows = db_session.query(ArnTable.resource_type_name, ArnTable.raw_arn).filter(
        ArnTable.service.like(service)
    )
    for row in rows:
        results[row.resource_type_name] = row.raw_arn
    return results


def get_arn_type_details(db_session, service, name):
    """
    Get details about a resource ARN type name in JSON format.

    :param db_session: SQLAlchemy database session object
    :param service: An AWS service prefix, like `s3` or `kms`
    :param name: The name of a resource type, like `bucket` or `object`
    :return: Metadata about an ARN type
    """
    rows = db_session.query(ArnTable).filter(
        ArnTable.resource_type_name.like(name), ArnTable.service.like(service)
    )
    result = rows.first()
    if result.condition_keys:
        condition_keys = result.condition_keys.split(",")
    else:
        condition_keys = None
    output = {
        "resource_type_name": result.resource_type_name,
        "raw_arn": result.raw_arn,
        "condition_keys": condition_keys,
    }
    return output


def get_resource_type_name_with_raw_arn(db_session, raw_arn):
    """
    Given a raw ARN, return the resource type name as shown in the database.

    :param db_session: SQLAlchemy database session object
    :param raw_arn: The raw ARN stored in the database, like 'arn:${Partition}:s3:::${BucketName}'
    :return: The resource type name, like bucket
    """
    from policy_sentry.util.arns import get_service_from_arn

    service_prefix = get_service_from_arn(raw_arn)
    query_resource_type_name = db_session.query(ArnTable.resource_type_name).filter(
        and_(
            ArnTable.raw_arn.startswith(raw_arn),
            ArnTable.originating_service.ilike(service_prefix),
        )
    )
    # TODO: Figure out the imagebuilder and kmsKey use case
    result = query_resource_type_name.first()
    resource_type_name = str(result.resource_type_name)
    return resource_type_name.lower()
