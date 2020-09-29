"""
Methods that execute specific queries against the SQLite database for the CONDITIONS table.
This supports the policy_sentry query functionality
"""
import logging
import functools
from policy_sentry.shared.iam_data import get_service_prefix_data
from policy_sentry.util.conditions import is_condition_key_match
from policy_sentry.querying.actions import get_action_data

logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=1024)
def get_condition_keys_for_service(service_prefix):
    """
    Get a list of available conditions per AWS service

    Arguments:
        service_prefix: An AWS service prefix, like `s3` or `kms`
    Returns:
        List: A list of condition keys
    """
    service_prefix_data = get_service_prefix_data(service_prefix)
    results = list(dict.fromkeys(service_prefix_data["conditions"].keys()))
    return results


# Per condition key name
# pylint: disable=inconsistent-return-statements
def get_condition_key_details(service_prefix, condition_key_name):
    """
    Get details about a specific condition key in JSON format

    Arguments:
        service_prefix: An AWS service prefix, like `ec2` or `kms`
        condition_key_name: The name of a condition key, like `ec2:Vpc`
    Returns:
        Dictionary: Metadata about the condition key
    """
    service_prefix_data = get_service_prefix_data(service_prefix)
    for condition_name, condition_data in service_prefix_data["conditions"].items():
        if is_condition_key_match(condition_data["condition"], condition_key_name):
            output = {
                "name": condition_data["condition"],
                "description": condition_data["description"],
                "condition_value_type": condition_data["type"].lower(),
            }
            return output


def get_conditions_for_action_and_raw_arn(action, raw_arn):
    """
    Get a list of conditions available to an action.

    Arguments:
        action: The IAM action, like s3:GetObject
        raw_arn: The raw ARN format specific to the action
    Returns:
        List: A list of condition keys
    """
    service_prefix, action_name = action.split(":")
    action_data = get_action_data(service_prefix, action_name)
    conditions = []
    for action_info in action_data[service_prefix]:
        if action_info["resource_arn_format"].lower() == raw_arn.lower():
            conditions.extend(action_info["condition_keys"])
    return conditions


def get_condition_keys_available_to_raw_arn(raw_arn):
    """
    Get a list of condition keys available to a RAW ARN

    Arguments:
        raw_arn: The value in the database, like arn:${Partition}:s3:::${BucketName}/${ObjectName}
    Returns:
        List: A list of condition keys
    """
    results = []
    elements = raw_arn.split(":", 5)
    service_prefix = elements[2]
    service_prefix_data = get_service_prefix_data(service_prefix)
    for resource_name, resource_data in service_prefix_data["resources"].items():
        if resource_data["arn"] == raw_arn:
            results.extend(resource_data["condition_keys"])
    results = list(dict.fromkeys(results))
    return results


# pylint: disable=inconsistent-return-statements
def get_condition_value_type(condition_key):
    """
    Get the data type of the condition key - like Date, String, etc.

    Arguments:
        condition_key: A condition key, like a4b:filters_deviceType
    Returns:
        String: type of the condition key, like Bool, Date, String, etc.
    """
    service_prefix, condition_name = condition_key.split(":")
    service_prefix_data = get_service_prefix_data(service_prefix)

    for condition_key_entry, condition_key_data in service_prefix_data["conditions"].items():
        if is_condition_key_match(condition_key_data["condition"], condition_key):
            return condition_key_data["type"].lower()
