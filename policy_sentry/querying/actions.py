"""
Methods that execute specific queries against the database for the ACTIONS table.
This supports the Policy Sentry query functionality
"""
import logging
import functools
from policy_sentry.shared.iam_data import iam_definition, get_service_prefix_data
from policy_sentry.querying.all import get_all_service_prefixes
from policy_sentry.querying.arns import get_matching_raw_arns, get_resource_type_name_with_raw_arn
from policy_sentry.util.arns import get_service_from_arn

all_service_prefixes = get_all_service_prefixes()
logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=1024)
def get_actions_for_service(service_prefix):
    """
    Get a list of available actions per AWS service

    Arguments:
        service_prefix: List: An AWS service prefix, like `s3` or `kms`
    Returns:
        List: A list of actions
    """
    service_prefix_data = get_service_prefix_data(service_prefix)
    results = []
    for item in service_prefix_data["privileges"]:
        results.append(f"{service_prefix}:{item['privilege']}")
    return results


@functools.lru_cache(maxsize=1024)
def get_action_data(service, action_name):
    """
    Get details about an IAM Action in JSON format.

    Arguments:
        service: An AWS service prefix, like `s3` or `kms`. Case insensitive.
        action_name: The name of an AWS IAM action, like `GetObject`. To get data about all actions in a service, specify "*". Case insensitive.

    Returns:
        List: A dictionary containing metadata about an IAM Action.
    """
    results = []
    action_data_results = {}
    try:
        service_info = get_service_prefix_data(service)
        for privilege_info in service_info["privileges"]:
            # Get the baseline conditions and dependent actions
            condition_keys = []
            dependent_actions = []
            rows = []
            if action_name == "*":
                rows = privilege_info["resource_types"]
            else:
                for resource_type_entry in privilege_info["resource_types"]:
                    if privilege_info["privilege"].lower() == action_name.lower():
                        rows.append(resource_type_entry)
            # for resource_type_entry in privilege_info["resource_types"]:
            for row in rows:
                # Set default value for if no other matches are found
                resource_arn_format = "*"
                # Get the dependent actions
                if row["dependent_actions"]:
                    dependent_actions.extend(row["dependent_actions"])
                # Get the condition keys
                for service_resource in service_info["resources"]:
                    if row["resource_type"] == "":
                        continue
                    if row["resource_type"].strip("*") == service_resource["resource"]:
                        resource_arn_format = service_resource.get("arn", "*")
                        condition_keys = service_resource.get("condition_keys")
                        break
                temp_dict = {
                    "action": f"{service_info['prefix']}:{privilege_info['privilege']}",
                    "description": privilege_info["description"],
                    "access_level": privilege_info["access_level"],
                    "resource_arn_format": resource_arn_format,
                    "condition_keys": condition_keys,
                    "dependent_actions": dependent_actions,
                }
                results.append(temp_dict)
        action_data_results[service] = results
    except TypeError as t_e:
        logger.debug(t_e)

    # if results:
    return action_data_results
    # else:
    #     return False
    # raise Exception("Unknown action {}:{}".format(service, action_name))


def get_actions_that_support_wildcard_arns_only(service_prefix):
    """
    Get a list of actions that do not support restricting the action to resource ARNs.
    Set service to "all" to get a list of actions across all services.

    Arguments:
        service_prefix: A single AWS service prefix, like `s3` or `kms`

    Returns:
        List: A list of actions that do not support resource ARN constraints
    """
    results = []
    if service_prefix == "all":
        for some_prefix in all_service_prefixes:
            service_prefix_data = get_service_prefix_data(some_prefix)
            for some_action in service_prefix_data["privileges"]:
                if len(some_action["resource_types"]) == 1:
                    if some_action["resource_types"][0]["resource_type"] == "":
                        results.append(f"{some_prefix}:{some_action['privilege']}")
    else:
        service_prefix_data = get_service_prefix_data(service_prefix)
        for some_action in service_prefix_data["privileges"]:
            if len(some_action["resource_types"]) == 1:
                for resource_type in some_action["resource_types"]:
                    if resource_type["resource_type"] == "":
                        results.append(f"{service_prefix}:{some_action['privilege']}")
    return results


def get_actions_at_access_level_that_support_wildcard_arns_only(
    service_prefix, access_level
):
    """
    Get a list of actions at an access level that do not support restricting the action to resource ARNs.
    Set service to "all" to get a list of actions across all services.

    Arguments:
        service_prefix: A single AWS service prefix, like `s3` or `kms`
        access_level: An access level as it is written in the database, such as 'Read', 'Write', 'List', 'Permisssions management', or 'Tagging'
    Returns:
        List: A list of actions at that access level that do not support resource ARN constraints
    """
    results = []
    if service_prefix == "all":
        for some_prefix in all_service_prefixes:
            service_prefix_data = get_service_prefix_data(some_prefix)
            for some_action in service_prefix_data["privileges"]:
                if len(some_action["resource_types"]) == 1:
                    if (
                        some_action["access_level"] == access_level
                        and some_action["resource_types"][0]["resource_type"] == ""
                    ):
                        results.append(f"{some_prefix}:{some_action['privilege']}")
    else:
        service_prefix_data = get_service_prefix_data(service_prefix)
        for some_action in service_prefix_data["privileges"]:
            if len(some_action["resource_types"]) == 1:
                if (
                    some_action["access_level"] == access_level
                    and some_action["resource_types"][0]["resource_type"] == ""
                ):
                    results.append(f"{service_prefix}:{some_action['privilege']}")
    return results


def get_actions_with_access_level(service_prefix, access_level):
    """
    Get a list of actions in a service under different access levels.

    Arguments:
        service_prefix: A single AWS service prefix, like `s3` or `kms`
        access_level: An access level as it is written in the database, such as 'Read', 'Write', 'List', 'Permisssions management', or 'Tagging'

    Returns:
        List: A list of actions with that access level and service prefix
    """
    results = []
    if service_prefix == "all":
        for some_prefix in all_service_prefixes:
            service_prefix_data = get_service_prefix_data(some_prefix)
            for some_action in service_prefix_data["privileges"]:
                if some_action["access_level"] == access_level:
                    results.append(f"{some_prefix}:{some_action['privilege']}")
    else:
        service_prefix_data = get_service_prefix_data(service_prefix)
        for some_action in service_prefix_data["privileges"]:
            if some_action["access_level"] == access_level:
                results.append(f"{service_prefix}:{some_action['privilege']}")
    return results


def get_actions_with_arn_type_and_access_level(
    service_prefix, resource_type_name, access_level
):
    """
    Get a list of actions in a service under different access levels, specific to an ARN format.

    Arguments:
        service_prefix: A single AWS service prefix, like `s3` or `kms`
        resource_type_name: The ARN type name, like `bucket` or `key`
        access_level: Access level like "Read" or "List" or "Permissions management"
    Return:
        List: A list of actions that have that ARN type and Access level
    """
    service_prefix_data = get_service_prefix_data(service_prefix)
    results = []

    for some_action in service_prefix_data["privileges"]:
        if some_action["access_level"] == access_level:
            for some_resource_type in some_action["resource_types"]:
                this_resource_type = some_resource_type["resource_type"].strip("*")
                if this_resource_type.lower() == resource_type_name.lower():
                    results.append(f"{service_prefix}:{some_action['privilege']}")
                    break
    return results


def get_actions_matching_arn(arn):
    """
    Given a user-supplied ARN, get a list of all actions that correspond to that ARN.

    Arguments:
        arn: A user-supplied arn
    Returns:
        List: A list of all actions that can match it.
    """
    raw_arns = get_matching_raw_arns(arn)
    results = []
    for raw_arn in raw_arns:
        resource_type_name = get_resource_type_name_with_raw_arn(raw_arn)
        service_prefix = get_service_from_arn(raw_arn)
        service_prefix_data = get_service_prefix_data(service_prefix)
        for some_action in service_prefix_data["privileges"]:
            for some_resource_type in some_action["resource_types"]:
                this_resource_type = some_resource_type["resource_type"].strip("*")
                if this_resource_type.lower() == resource_type_name.lower():
                    results.append(f"{service_prefix}:{some_action['privilege']}")
    results = list(dict.fromkeys(results))
    results.sort()
    return results


def get_actions_matching_condition_key(service_prefix, condition_key):
    """
    Get a list of actions under a service that allow the use of a specified condition key

    Arguments:
        service_prefix: A single AWS service prefix
        condition_key: The condition key to look for.
    Returns:
        List: A list of actions
    """
    results = []
    if service_prefix == "all":
        for some_prefix in all_service_prefixes:
            service_prefix_data = get_service_prefix_data(some_prefix)
            for some_action in service_prefix_data["privileges"]:
                for some_resource_type in some_action["resource_types"]:
                    if condition_key in some_resource_type["condition_keys"]:
                        results.append(f"{some_prefix}:{some_action['privilege']}")
    else:
        service_prefix_data = get_service_prefix_data(service_prefix)
        for some_action in service_prefix_data["privileges"]:
            for some_resource_type in some_action["resource_types"]:
                if condition_key in some_resource_type["condition_keys"]:
                    results.append(f"{service_prefix}:{some_action['privilege']}")
    return results


# def get_actions_matching_condition_crud_and_arn(
#     condition_key, access_level, raw_arn
# ):
#     """
#     Get a list of IAM Actions matching a condition key, CRUD level, and raw ARN format.
#
#         condition_key: A condition key, like aws:TagKeys
#         access_level: Access level that matches the database value. "Read", "Write", "List", "Tagging", or "Permissions management"
#         raw_arn: The raw ARN format in the database, like arn:${Partition}:s3:::${BucketName}
#     :return: List of IAM Actions
#     """
#     print()
#     # TODO: This one is non-essential right now.
#


def remove_actions_not_matching_access_level(actions_list, access_level):
    """
    Given a list of actions, return a list of actions that match an access level

    Arguments:
        actions_list: A list of actions
        access_level: 'read', 'write', 'list', 'tagging', or 'permissions-management'
    Returns:
        List: An Updated list of actions, where the actions not matching the requested access level are removed.
    """
    new_actions_list = []

    def is_access_level(some_service_prefix, some_action):
        service_prefix_data = get_service_prefix_data(some_service_prefix.lower())
        this_result = None
        if service_prefix_data:
            if "privileges" in service_prefix_data:
                for action_instance in service_prefix_data["privileges"]:
                    if action_instance.get("access_level") == access_level:
                        # logger.debug(f"remove_actions_not_matching_access_level: Provided access level is {access_level}, "
                        #              f"matches {action_instance.get('access_level')}")
                        if action_instance.get("privilege").lower() == some_action.lower():
                            this_result = f"{some_service_prefix}:{action_instance.get('privilege')}"
                            break
        if not this_result:
            return False
        else:
            return this_result
    if actions_list == ["*"]:
        actions_list.clear()
        for some_prefix in all_service_prefixes:
            service_prefix_data = get_service_prefix_data(some_prefix)
            for some_action in service_prefix_data["privileges"]:
                if some_action["access_level"] == access_level:
                    actions_list.append(f"{some_prefix}:{some_action['privilege']}")
    for action in actions_list:
        try:
            service_prefix, action_name = action.split(":")
        except ValueError as v_e:
            logger.debug(f"{v_e} - for action {action}")
            continue
        result = is_access_level(service_prefix, action_name)
        if result:
            new_actions_list.append(result)
            # new_actions_list.append(f"{service_prefix}:{action_name['privilege']}")
    return new_actions_list


def get_dependent_actions(actions_list):
    """
    Given a list of IAM Actions, query the database to determine if the action has dependent actions in the
    fifth column of the Resources, Actions, and Condition keys tables. If it does, add the dependent actions
    to the list, and return the updated list.

    It includes the original action in there as well. So, if you supply `kms:CreateCustomKeyStore`, it will give you `kms:CreateCustomKeyStore` as well as `cloudhsm:DescribeClusters`

    To get dependent actions for a single given IAM action, just provide the action as a list with one item, like this:
    `get_dependent_actions(db_session, ['kms:CreateCustomKeystore'])`

    Arguments:
        actions_list: A list of actions to use in querying the database for dependent actions
    Returns:
        List: Updated list of actions, including dependent actions if applicable.
    """
    new_actions_list = []
    for action in actions_list:
        service, action_name = action.split(":")
        rows = get_action_data(service, action_name)
        for row in rows[service]:
            if row["dependent_actions"] is not None:
                # new_actions_list.append(action)
                # dependent_actions = [x.lower() for x in row["dependent_actions"]]
                # dependent_actions = [x.lower() for x in row["dependent_actions"]]
                new_actions_list.extend(row["dependent_actions"])

    new_actions_list = list(dict.fromkeys(new_actions_list))
    return new_actions_list


def remove_actions_that_are_not_wildcard_arn_only(actions_list):
    """
    Given a list of actions, remove the ones that CAN be restricted to ARNs, leaving only the ones that cannot.

    Arguments:
        actions_list: A list of actions
    Returns:
        List: An updated list of actions
    """
    # remove duplicates, if there are any
    actions_list_unique = list(dict.fromkeys(actions_list))
    results = []
    for action in actions_list_unique:
        service_prefix, action_name = action.split(":")
        action_data = get_action_data(service_prefix, action_name)
        if len(action_data[service_prefix]) == 1:
            if action_data[service_prefix][0]["resource_arn_format"] == "*":
                # Let's return the CamelCase action name format
                results.append(action_data[service_prefix][0]["action"])
    return results


def get_privilege_info(service, action):
    """
    Given a service, like `s3` and an action name, like `ListBucket`, return info about that action.

    Arguments:
        service: The service prefix, like `s3`
        action: An action name, like `ListBucket`

    Returns:
        List: The info from the docs about that action, along with some of the info from the docs
    """
    for service_info in iam_definition:
        if service_info["prefix"] == service:
            for privilege_info in service_info["privileges"]:
                if privilege_info["privilege"] == action:
                    privilege_info["service_resources"] = service_info["resources"]
                    privilege_info["service_conditions"] = service_info["conditions"]
                    return privilege_info
    raise Exception("Unknown action {}:{}".format(service, action))
