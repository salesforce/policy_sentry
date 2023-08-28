from __future__ import annotations

import warnings
from typing import Any

from policy_sentry.shared.iam_data import get_service_prefix_data


def get_arn_type_details_v1(service_prefix: str, resource_type_name: str) -> dict[str, Any]:
    """
    DEPRECATED: Please recreate the IAM datastore file!

    Get details about ARNs in JSON format (v1).

    Arguments:
        service_prefix: An AWS service prefix, like `s3` or `kms`
        resource_type_name: The name of a resource type, like `bucket` or `object`. To get details on ALL arns in a service, specify "*" here.
    Returns:
        Dictionary: Metadata about an ARN type
    """
    warnings.warn("Please recreate the IAM datastore file!", DeprecationWarning)

    service_prefix_data = get_service_prefix_data(service_prefix)
    output = {}
    for resource_name, resource_data in service_prefix_data["resources"].items():
        if resource_data["resource"].lower() == resource_type_name.lower():
            output = {
                "resource_type_name": resource_data["resource"],
                "raw_arn": resource_data["arn"],
                "condition_keys": resource_data["condition_keys"],
            }
            break
    return output
