"""
Methods that execute specific queries against the SQLite database for the ARN table.
This supports the policy_sentry query functionality
"""
from __future__ import annotations

import logging
import functools
import warnings
from typing import Any

from policy_sentry.querying.arns_v1 import get_arn_type_details_v1
from policy_sentry.shared.constants import POLICY_SENTRY_SCHEMA_VERSION_V2
from policy_sentry.shared.iam_data import (
    get_service_prefix_data,
    get_iam_definition_schema_version,
)
from policy_sentry.util.arns import does_arn_match, get_service_from_arn

logger = logging.getLogger(__name__)


def get_arn_data(service_prefix: str, resource_type_name: str) -> list[dict[str, Any]]:
    """
    DEPRECATED: Please use get_arn_type_details() instead!

    Get details about ARNs in JSON format.

    Arguments:
        service_prefix: An AWS service prefix, like `s3` or `kms`
        resource_type_name: The name of a resource type, like `bucket` or `object`. To get details on ALL arns in a service, specify "*" here.
    Returns:
        Dictionary: Metadata about an ARN type
    """
    warnings.warn("Please use get_arn_type_details() instead", DeprecationWarning)

    results = []
    service_prefix_data = get_service_prefix_data(service_prefix)
    for resource_name, resource_data in service_prefix_data["resources"].items():
        if resource_data["resource"].lower() == resource_type_name.lower():
            output = {
                "resource_type_name": resource_data["resource"],
                "raw_arn": resource_data["arn"],
                "condition_keys": resource_data["condition_keys"],
            }
            results.append(output)
    return results


@functools.lru_cache(maxsize=1024)
def get_raw_arns_for_service(service_prefix: str) -> list[str]:
    """
    Get a list of available raw ARNs per AWS service

    Arguments:
        service_prefix: An AWS service prefix, like `s3` or `kms`
    Returns:
        List: A list of raw ARNs
    """
    service_prefix_data = get_service_prefix_data(service_prefix)
    return [
        resource_data["arn"]
        for resource_data in service_prefix_data["resources"].values()
    ]


@functools.lru_cache(maxsize=1024)
def get_arn_types_for_service(service_prefix: str) -> dict[str, str]:
    """
    Get a list of available ARN short names per AWS service.

    Arguments:
        service_prefix: An AWS service prefix, like `s3` or `kms`
    Returns:
        List: A list of ARN types, like `bucket` or `object`
    """
    service_prefix_data = get_service_prefix_data(service_prefix)
    return {
        resource_name: resource_data["arn"]
        for resource_name, resource_data in service_prefix_data["resources"].items()
    }


def get_arn_type_details(
    service_prefix: str, resource_type_name: str
) -> dict[str, Any]:
    """
    Get details about ARNs in JSON format.

    Arguments:
        service_prefix: An AWS service prefix, like `s3` or `kms`
        resource_type_name: The name of a resource type, like `bucket` or `object`. To get details on ALL arns in a service, specify "*" here.
    Returns:
        Dictionary: Metadata about an ARN type
    """
    schema_version = get_iam_definition_schema_version()
    if schema_version == POLICY_SENTRY_SCHEMA_VERSION_V2:
        return get_arn_type_details_v2(
            service_prefix=service_prefix, resource_type_name=resource_type_name
        )

    return get_arn_type_details_v1(
        service_prefix=service_prefix, resource_type_name=resource_type_name
    )


def get_arn_type_details_v2(
    service_prefix: str, resource_type_name: str
) -> dict[str, Any]:
    """
    Get details about ARNs in JSON format (v2).

    Arguments:
        service_prefix: An AWS service prefix, like `s3` or `kms`
        resource_type_name: The name of a resource type, like `bucket` or `object`. To get details on ALL arns in a service, specify "*" here.
    Returns:
        Dictionary: Metadata about an ARN type
    """
    output = {}
    service_prefix_data = get_service_prefix_data(service_prefix)
    this_resource_type_name = service_prefix_data["resources_lower_name"].get(resource_type_name.lower())
    if this_resource_type_name:
        resource_data = service_prefix_data["resources"][this_resource_type_name]
        output = {
            "resource_type_name": this_resource_type_name,
            "raw_arn": resource_data["arn"],
            "condition_keys": resource_data["condition_keys"],
        }

    return output


# pylint: disable=inconsistent-return-statements
def get_resource_type_name_with_raw_arn(raw_arn: str) -> str | None:
    """
    Given a raw ARN, return the resource type name as shown in the database.

    Arguments:
        raw_arn: The raw ARN stored in the database, like 'arn:${Partition}:s3:::${BucketName}'
    Returns:
        String: The resource type name, like bucket
    """
    elements = raw_arn.split(":", 5)
    service_prefix = elements[2]
    service_data = get_service_prefix_data(service_prefix)

    for resource_name, resource_data in service_data["resources"].items():
        if resource_data["arn"].lower() == raw_arn.lower():
            return resource_name

    return None


def get_matching_raw_arns(arn: str) -> list[str]:
    """
    Given a user-supplied ARN, return the list of raw_arns since that is used as a unique identifier throughout this library

    Arguments:
        arn: The user-supplied arn, like arn:aws:s3:::mybucket
    Returns:
        list(str): The list of raw ARNs stored in the database, like 'arn:${Partition}:s3:::${BucketName}'
    """
    result = []
    service_in_scope = get_service_from_arn(arn)
    # Determine which resource it applies to
    all_raw_arns_for_service = get_raw_arns_for_service(service_in_scope)
    # Get the raw ARN specific to the provided one
    for raw_arn in all_raw_arns_for_service:
        if does_arn_match(arn, raw_arn) and raw_arn not in result:
            result.append(raw_arn)
    return result
