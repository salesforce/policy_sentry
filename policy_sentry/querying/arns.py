"""
Methods that execute specific queries against the SQLite database for the ARN table.
This supports the policy_sentry query functionality
"""
import logging
from policy_sentry.shared.iam_data import iam_definition, get_service_prefix_data

logger = logging.getLogger(__name__)


def get_arn_data(service_prefix, resource_type_name):
    """
    Get details about ARNs in JSON format.

    :param service_prefix: An AWS service prefix, like `s3` or `kms`
    :param resource_type_name: The name of a resource type, like `bucket` or `object`. To get details on ALL arns in a service, specify "*" here.
    :return: Metadata about an ARN type
    """
    results = []
    for service_data in iam_definition:
        if service_data["prefix"] == service_prefix:
            for resource in service_data["resources"]:
                if resource["resource"].lower() == resource_type_name.lower():
                    output = {
                        "resource_type_name": resource["resource"],
                        "raw_arn": resource["arn"],
                        "condition_keys": resource["condition_keys"],
                    }
                    results.append(output)
    return results


def get_raw_arns_for_service(service_prefix):
    """
    Get a list of available raw ARNs per AWS service

    :param service_prefix: An AWS service prefix, like `s3` or `kms`
    :return: A list of raw ARNs
    """
    results = []
    for service_data in iam_definition:
        if service_data["prefix"] == service_prefix:
            for resource in service_data["resources"]:
                results.append(resource["arn"])
    return results


def get_arn_types_for_service(service_prefix):
    """
    Get a list of available ARN short names per AWS service.

    :param service_prefix: An AWS service prefix, like `s3` or `kms`
    :return: A list of ARN types, like `bucket` or `object`
    """
    results = {}
    for service_data in iam_definition:
        if service_data["prefix"] == service_prefix:
            for resource in service_data["resources"]:
                results[resource["resource"]] = resource["arn"]
    return results


def get_arn_type_details(service_prefix, resource_type_name):
    """
    Get details about ARNs in JSON format.

    :param service_prefix: An AWS service prefix, like `s3` or `kms`
    :param resource_type_name: The name of a resource type, like `bucket` or `object`. To get details on ALL arns in a service, specify "*" here.
    :return: Metadata about an ARN type
    """
    service_prefix_data = get_service_prefix_data(service_prefix)
    output = {}
    for resource in service_prefix_data["resources"]:
        if resource["resource"].lower() == resource_type_name.lower():
            output = {
                "resource_type_name": resource["resource"],
                "raw_arn": resource["arn"],
                "condition_keys": resource["condition_keys"],
            }
            break
    return output


# pylint: disable=inconsistent-return-statements
def get_resource_type_name_with_raw_arn(raw_arn):
    """
    Given a raw ARN, return the resource type name as shown in the database.

    :param raw_arn: The raw ARN stored in the database, like 'arn:${Partition}:s3:::${BucketName}'
    :return: The resource type name, like bucket
    """
    elements = raw_arn.split(":", 5)
    service_prefix = elements[2]
    service_data = get_service_prefix_data(service_prefix)

    for resource in service_data["resources"]:
        if resource["arn"].lower() == raw_arn.lower():
            return resource["resource"]
