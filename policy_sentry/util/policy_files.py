"""A few methods for parsing policies."""
import json


# pylint: disable=too-many-branches,too-many-statements
def get_actions_from_policy(data):
    """Given a policy dictionary, create a list of the actions"""
    actions_list = []
    # Multiple statements are in the 'Statement' list
    # pylint: disable=too-many-nested-blocks
    for i in range(len(data['Statement'])):
        try:
            # Statement must be a dict if it's a single statement. Otherwise it will be a list of statements
            if isinstance(data['Statement'], dict):
                # We only want to evaluate policies that have Effect = "Allow"
                # pylint: disable=no-else-continue, literal-comparison
                if data['Statement']['Effect'] is 'Deny':
                    continue
                else:
                    try:
                        # Action = "s3:GetObject"
                        if isinstance(data['Statement']['Action'], str):
                            actions_list.append(
                                data['Statement']['Action'])
                        # Action = ["s3:GetObject", "s3:ListBuckets"]
                        elif isinstance(data['Statement']['Action'], list):
                            actions_list.extend(
                                data['Statement']['Action'])
                        elif 'Action' not in data['Statement']:
                            print('Action is not a key in the statement')
                        else:
                            print(
                                "Unknown error: The 'Action' is neither a list nor a string")
                    except KeyError as k_e:
                        print(
                            f"KeyError at get_actions_from_policy {k_e}")
                        exit()

            # Otherwise it will be a list of Sids
            elif isinstance(data['Statement'], list):
                # We only want to evaluate policies that have Effect = "Allow"
                try:
                    if data['Statement'][i]['Effect'] == 'Deny':
                        continue
                    else:
                        if 'Action' in data['Statement'][i]:
                            if isinstance(data['Statement'][i]['Action'], str):
                                actions_list.append(
                                    data['Statement'][i]['Action'])
                            elif isinstance(data['Statement'][i]['Action'], list):
                                actions_list.extend(
                                    data['Statement'][i]['Action'])
                            elif data['Statement'][i]['NotAction'] and not data['Statement'][i]['Action']:
                                print('Skipping due to NotAction')
                            else:
                                print(
                                    "Unknown error: The 'Action' is neither a list nor a string")
                                exit()
                        else:
                            continue
                except KeyError as k_e:
                    print(
                        f"KeyError at get_actions_from_policy {k_e}")
                    exit()
            else:
                print(
                    "Unknown error: The 'Action' is neither a list nor a string")
                # exit()
        except TypeError as t_e:
            print(
                f"TypeError at get_actions_from_policy {t_e}")
            exit()
    try:
        actions_list = [x.lower() for x in actions_list]
    except AttributeError as a_e:
        print(actions_list)
        print(f"AttributeError: {a_e}")
    actions_list.sort()
    return actions_list


# pylint: disable=too-many-branches,too-many-statements
def get_actions_from_json_policy_file(file):
    """
    read the json policy file and return a list of actions
    """

    # FIXME use a try/expect here to validate the json file. I would create a generic json
    try:
        with open(file) as json_file:
            # validation function/parser as there is a lot of json floating around
            # in this tool. [MJ]
            data = json.load(json_file)
            actions_list = get_actions_from_policy(data)

    except:  # pylint: disable=bare-except
        print("General Error at get_actions_from_json_policy_file.")
        actions_list = []
    return actions_list
