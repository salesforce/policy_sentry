from __future__ import annotations

import warnings

from policy_sentry.shared.iam_data import get_service_prefix_data


def get_all_actions_v1(
    all_service_prefixes: set[str], lowercase: bool = False
) -> set[str]:
    """
    DEPRECATED: Please recreate the IAM datastore file!

    Gets a huge list of all IAM actions. This is used as part of the policyuniverse approach to minimizing
    IAM Policies to meet AWS-mandated character limits on policies (v1).

    :param lowercase: Set to true to have the list of actions be in all lowercase strings.
    :return: A list of all actions present in the database.
    """
    warnings.warn(
        "Please recreate the IAM datastore file!", DeprecationWarning, stacklevel=2
    )

    all_actions = set()

    for service_prefix in all_service_prefixes:
        service_prefix_data = get_service_prefix_data(service_prefix)
        for action_name in service_prefix_data["privileges"]:
            if lowercase:
                all_actions.add(f"{service_prefix}:{action_name.lower()}")
            else:
                all_actions.add(f"{service_prefix}:{action_name}")

    return all_actions
