"""IAM Database queries that are not specific to either the Actions, ARNs, or Condition Keys tables."""
import logging
import functools
from policy_sentry.shared.iam_data import iam_definition

logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=1024)
def get_all_service_prefixes():
    """
    Gets all the AWS service prefixes from the actions table.

    If the action table does NOT have specific IAM actions (and therefore only supports * actions),
    then it will not be included in the response.

    Returns:
        List: A list of all AWS service prefixes present in the table.
    """
    results = [d["prefix"] for d in iam_definition]
    results = list(set(results))
    results.sort()
    return results


@functools.lru_cache(maxsize=1024)
def get_all_actions(lowercase=False):
    """
    Gets a huge list of all IAM actions. This is used as part of the policyuniverse approach to minimizing
    IAM Policies to meet AWS-mandated character limits on policies.

    :param lowercase: Set to true to have the list of actions be in all lowercase strings.
    :return: A list of all actions present in the database.
    """
    all_actions = set()

    for service_info in iam_definition:
        for privilege_info in service_info["privileges"]:
            if lowercase:
                all_actions.add(
                    f"{service_info['prefix']}:{privilege_info['privilege'].lower()}"
                )
            else:
                all_actions.add(
                    f"{service_info['prefix']}:{privilege_info['privilege']}"
                )

    # results = list(set(results))
    # results.sort()
    return all_actions
