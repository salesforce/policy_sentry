from __future__ import annotations

import logging
import warnings
from typing import Any

from policy_sentry.querying.all import get_all_service_prefixes
from policy_sentry.querying.arns import (
    get_matching_raw_arns,
    get_resource_type_name_with_raw_arn,
)
from policy_sentry.shared.iam_data import get_service_prefix_data
from policy_sentry.util.arns import get_service_from_arn

all_service_prefixes = get_all_service_prefixes()
logger = logging.getLogger(__name__)


def get_action_data_v1(
    service: str, action_name: str
) -> dict[str, list[dict[str, Any]]]:
    """
    DEPRECATED: Please recreate the IAM datastore file!

    Get details about an IAM Action in JSON format (v1).

    Arguments:
        service: An AWS service prefix, like `s3` or `kms`. Case insensitive.
        action_name: The name of an AWS IAM action, like `GetObject`. To get data about all actions in a service, specify "*". Case insensitive.

    Returns:
        List: A dictionary containing metadata about an IAM Action.
    """
    warnings.warn("Please recreate the IAM datastore file!", DeprecationWarning)

    results = []
    action_data_results = {}
    try:
        service_prefix_data = get_service_prefix_data(service)
        for this_action_name, this_action_data in service_prefix_data[
            "privileges"
        ].items():
            # Get the baseline conditions and dependent actions
            condition_keys = []
            dependent_actions = []
            rows = []
            if action_name == "*":
                # rows = this_action_data["resource_types"]
                for resource_type_entry in this_action_data["resource_types"]:
                    rows.append(this_action_data["resource_types"][resource_type_entry])
            else:
                for resource_type_entry in this_action_data["resource_types"]:
                    if this_action_name.lower() == action_name.lower():
                        rows.append(
                            this_action_data["resource_types"][resource_type_entry]
                        )
            for row in rows:
                # Set default value for if no other matches are found
                resource_arn_format = "*"
                # Get the dependent actions
                if row["dependent_actions"]:
                    dependent_actions.extend(row["dependent_actions"])
                # Get the condition keys
                for service_resource_name, service_resource_data in service_prefix_data[
                    "resources"
                ].items():
                    if row["resource_type"] == "":
                        continue
                    if (
                        row["resource_type"].strip("*")
                        == service_resource_data["resource"]
                    ):
                        resource_arn_format = service_resource_data.get("arn", "*")
                        condition_keys = service_resource_data.get("condition_keys")
                        break
                temp_dict = {
                    "action": f"{service_prefix_data['prefix']}:{this_action_name}",
                    "description": this_action_data["description"],
                    "access_level": this_action_data["access_level"],
                    "api_documentation_link": this_action_data.get(
                        "api_documentation_link"
                    ),
                    "resource_arn_format": resource_arn_format,
                    "condition_keys": condition_keys,
                    "dependent_actions": dependent_actions,
                }
                results.append(temp_dict)
        action_data_results[service] = results
    except TypeError as t_e:
        logger.debug(t_e)

    return action_data_results


def get_action_matching_access_level_v1(
    service_prefix: str, action_name: str, access_level: str
) -> str | None:
    """
    DEPRECATED: Please recreate the IAM datastore file!

    Get the action under a service that match the given access level (v1)

    Arguments:
        service_prefix: A single AWS service prefix
        action_name: Name of the action
        access_level: Access level like "Read" or "List" or "Permissions management"
    Returns:
        List: action or None
    """
    warnings.warn("Please recreate the IAM datastore file!", DeprecationWarning)

    result = None
    service_prefix_data = get_service_prefix_data(service_prefix.lower())
    if service_prefix_data:
        privileges = service_prefix_data.get("privileges")
        if privileges:
            for this_action_name, action_data in privileges.items():
                if action_data["access_level"] == access_level:
                    if this_action_name.lower() == action_name.lower():
                        result = f"{service_prefix}:{this_action_name}"
                        break

    return result


def get_actions_with_arn_type_and_access_level_v1(
    service_prefix: str, resource_type_name: str, access_level: str
) -> list[str]:
    """
    DEPRECATED: Please recreate the IAM datastore file!

    Get a list of actions in a service under different access levels, specific to an ARN format (v1).

    Arguments:
        service_prefix: A single AWS service prefix, like `s3` or `kms`
        resource_type_name: The ARN type name, like `bucket` or `key`
        access_level: Access level like "Read" or "List" or "Permissions management"
    Return:
        List: A list of actions that have that ARN type and Access level
    """
    warnings.warn("Please recreate the IAM datastore file!", DeprecationWarning)

    service_prefix_data = get_service_prefix_data(service_prefix)
    results = []

    if service_prefix == "all":
        for some_prefix in all_service_prefixes:
            service_prefix_data = get_service_prefix_data(some_prefix)
            for action_name, action_data in service_prefix_data["privileges"].items():
                if action_data["access_level"] == access_level:
                    for resource_name, resource_data in action_data[
                        "resource_types"
                    ].items():
                        this_resource_type = resource_data["resource_type"].strip("*")
                        if this_resource_type.lower() == resource_type_name.lower():
                            results.append(
                                f"{service_prefix}:{action_data['privilege']}"
                            )
                            break
    else:
        for action_name, action_data in service_prefix_data["privileges"].items():
            if action_data["access_level"] == access_level:
                for resource_name, resource_data in action_data[
                    "resource_types"
                ].items():
                    this_resource_type = resource_data["resource_type"].strip("*")
                    if this_resource_type.lower() == resource_type_name.lower():
                        results.append(f"{service_prefix}:{action_data['privilege']}")
                        break
    return results


def get_actions_matching_arn_type_v1(
    service_prefix: str, resource_type_name: str
) -> list[str]:
    """
    DEPRECATED: Please recreate the IAM datastore file!

    Get a list of actions in a service specific to ARN type (v1).

    Arguments:
        service_prefix: A single AWS service prefix, like `s3` or `kms`
        resource_type_name: The ARN type name, like `bucket` or `key`
    Return:
        List: A list of actions that have that ARN type
    """
    warnings.warn("Please recreate the IAM datastore file!", DeprecationWarning)

    service_prefix_data = get_service_prefix_data(service_prefix)
    results = []

    if service_prefix == "all":
        for some_prefix in all_service_prefixes:
            service_prefix_data = get_service_prefix_data(some_prefix)
            for action_name, action_data in service_prefix_data["privileges"].items():
                for resource_name, resource_data in action_data[
                    "resource_types"
                ].items():
                    this_resource_type = resource_data["resource_type"].strip("*")
                    if this_resource_type.lower() == resource_type_name.lower():
                        results.append(f"{service_prefix}:{action_data['privilege']}")
                        break
    else:
        for action_name, action_data in service_prefix_data["privileges"].items():
            for resource_name, resource_data in action_data["resource_types"].items():
                this_resource_type = resource_data["resource_type"].strip("*")
                if this_resource_type.lower() == resource_type_name.lower():
                    results.append(f"{service_prefix}:{action_data['privilege']}")
                    break
    return results


def get_actions_matching_arn_v1(arn: str) -> list[str]:
    """
    DEPRECATED: Please recreate the IAM datastore file!

    Given a user-supplied ARN, get a list of all actions that correspond to that ARN.

    Arguments:
        arn: A user-supplied arn
    Returns:
        List: A list of all actions that can match it.
    """
    warnings.warn("Please recreate the IAM datastore file!", DeprecationWarning)

    raw_arns = get_matching_raw_arns(arn)
    results = []
    for raw_arn in raw_arns:
        resource_type_name = get_resource_type_name_with_raw_arn(raw_arn)
        if resource_type_name is None:
            continue

        service_prefix = get_service_from_arn(raw_arn)
        service_prefix_data = get_service_prefix_data(service_prefix)
        for action_name, action_data in service_prefix_data["privileges"].items():
            # for some_action in service_prefix_data["privileges"]:
            for resource_name, resource_data in action_data["resource_types"].items():
                this_resource_type = resource_data["resource_type"].strip("*")
                if this_resource_type.lower() == resource_type_name.lower():
                    results.append(f"{service_prefix}:{action_data['privilege']}")
    results = list(dict.fromkeys(results))

    return results
