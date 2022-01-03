"""IAM Database queries that are not specific to either the Actions, ARNs, or Condition Keys tables."""
import logging
import functools
from policy_sentry.shared.iam_data import iam_definition, get_service_prefix_data

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
    # results = [d["prefix"] for d in iam_definition]
    results = list(set([item['prefix'] for item in iam_definition]))
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

    all_service_prefixes = get_all_service_prefixes()
    for service_prefix in all_service_prefixes:
        service_prefix_data = get_service_prefix_data(service_prefix)
        for action_dict in service_prefix_data["privileges"]:
            if lowercase:
                all_actions.add(
                    f"{service_prefix}:{action_dict['privilege'].lower()}"
                )
            else:
                all_actions.add(
                    f"{service_prefix}:{action_dict['privilege']}"
                )

    # results = list(set(results))
    # results.sort()
    return all_actions


def get_service_authorization_url(service_prefix: str) -> str:
    """
    Gets the URL to the Actions, Resources, and Condition Keys page for a particular service.
    """
    result = next((item['service_authorization_url'] for item in iam_definition if item["prefix"] == service_prefix), None)
    return result
