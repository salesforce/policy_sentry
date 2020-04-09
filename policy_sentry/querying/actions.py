from policy_sentry.shared.iam_data import iam_definition, get_service_prefix_data


def get_actions_for_service(service_prefix):
    """Similar to get_privilege_info"""
    service_prefix_data = get_service_prefix_data(service_prefix)
    results = []
    for item in service_prefix_data["privileges"]:
        results.append(f"{service_prefix}:{item['privilege']}")
    return results


def get_action_data(service, action_name):
    """Similar to get_privilege info but for backwards compatibility"""
    results = []
    action_data_results = {}
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
    # if results:
    return action_data_results
    # else:
    #     return False
    # raise Exception("Unknown action {}:{}".format(service, action_name))


def get_actions_that_support_wildcard_arns_only(service_prefix):
    service_prefix_data = get_service_prefix_data(service_prefix)
    results = []

    for some_action in service_prefix_data["privileges"]:
        if len(some_action["resource_types"]) == 1:
            if some_action["resource_types"][0]["resource_type"] == "":
                results.append(f"{service_prefix}:{some_action['privilege']}")
    return results


def get_actions_at_access_level_that_support_wildcard_arns_only(
    service_prefix, access_level
):
    service_prefix_data = get_service_prefix_data(service_prefix)
    results = []

    for some_action in service_prefix_data["privileges"]:
        if len(some_action["resource_types"]) == 1:
            if (
                some_action["access_level"] == access_level
                and some_action["resource_types"][0]["resource_type"] == ""
            ):
                results.append(f"{service_prefix}:{some_action['privilege']}")
    return results


def get_actions_with_access_level(service_prefix, access_level):
    service_prefix_data = get_service_prefix_data(service_prefix)
    results = []

    for some_action in service_prefix_data["privileges"]:
        if some_action["access_level"] == access_level:
            results.append(f"{service_prefix}:{some_action['privilege']}")
    return results


def get_actions_with_arn_type_and_access_level(
    service_prefix, resource_type_name, access_level
):
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


def get_actions_matching_condition_key(service, condition_key):
    print()
    # TODO: This one is non-essential right now.


# def get_actions_matching_condition_crud_and_arn(
#     condition_key, access_level, raw_arn
# ):
#     print()
#     # TODO: This one is non-essential right now.
#


def remove_actions_not_matching_access_level(actions_list, access_level):
    # TODO: This method normalized the access level unnecessarily. Make sure to change that in the final iteration
    new_actions_list = []

    def is_access_level(some_service_prefix, some_action):
        service_prefix_data = get_service_prefix_data(some_service_prefix.lower())
        result = None
        for action_instance in service_prefix_data["privileges"]:
            if action_instance.get("access_level") == access_level:
                if action_instance.get("privilege").lower() == some_action.lower():
                    result = f"{some_service_prefix}:{action_instance.get('privilege')}"
                    break
        if not result:
            return False
        else:
            return result

    for action in actions_list:
        service_prefix, action_name = action.split(":")
        result = is_access_level(service_prefix, action_name)
        if result:
            new_actions_list.append(result)
            # new_actions_list.append(f"{service_prefix}:{action_name['privilege']}")
    return new_actions_list


def get_dependent_actions(actions_list):
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
    Given a service, like "s3"
    and an action, like "ListBucket"
    return the info from the docs about that action, along with some of the info from the docs
    """
    for service_info in iam_definition:
        if service_info["prefix"] == service:
            for privilege_info in service_info["privileges"]:
                if privilege_info["privilege"] == action:
                    privilege_info["service_resources"] = service_info["resources"]
                    privilege_info["service_conditions"] = service_info["conditions"]
                    return privilege_info
    raise Exception("Unknown action {}:{}".format(service, action))
