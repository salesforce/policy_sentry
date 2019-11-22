from policy_sentry.shared.file import read_this_file
# from policyuniverse import all_permissions
import fnmatch
import pprint
from policy_sentry.shared.actions import get_actions_by_access_level, get_actions_from_json_policy_file, \
    get_all_actions
from policy_sentry.shared.database import connect_db
from pathlib import Path
from policy_sentry.shared.file import list_files_in_directory

HOME = str(Path.home())
CONFIG_DIRECTORY = '/.policy_sentry/'
DATABASE_FILE_NAME = 'aws.sqlite3'
database_file_path = HOME + CONFIG_DIRECTORY + DATABASE_FILE_NAME


def read_risky_iam_permissions_text_file(audit_file):
    """
    read in the audit file of high risk actions
    """

    risky_actions = read_this_file(audit_file)
    return risky_actions


def determine_risky_actions(requested_actions, audit_file):
    """
    compare the actions in the policy against the audit file of high risk actions
    """

    risky_actions = read_risky_iam_permissions_text_file(audit_file)
    print("Auditing for risky actions...")
    print("Please justify why you need permissions to the following actions:")
    for action in requested_actions:
        if action in risky_actions:
            print("{}".format(action))
    print("Auditing for risky actions complete!")


def expand(action):  # FIXME [MJ] change the name to be more descriptive
    """
    expand the action wildcards into a full action
    """

    db_session = connect_db(database_file_path)

    all_actions = get_all_actions(db_session)

    if isinstance(action, list):
        expanded_actions = []
        for item in action:
            expanded_actions.extend(expand(item))
        return expanded_actions

    if "*" in action:
        expanded = [
            expanded_action.lower()
            # for expanded_action in all_permissions
            for expanded_action in all_actions
            if fnmatch.fnmatchcase(expanded_action.lower(), action.lower())
        ]

        # if we get a wildcard for a tech we've never heard of, just return the
        # wildcard
        if not expanded:
            print(
                "ERROR: The action {} references a wildcard for an unknown resource.".format(action))
            return [action.lower()]

        return expanded
    return [action.lower()]


def determine_actions_to_expand(action_list):
    """
    check to see if an action needs to get expanded
    """

    # FIXME why is this new, what is the change? Set a more descriptive variable name, this is a temp/local var
    # TODO Consider using enumerate instead of iterating with range and len
    new_action_list = []
    for action in range(len(action_list)):
        if "*" in action_list[action]:
            expanded_action = expand(action_list[action])
            new_action_list.extend(expanded_action)
        else:
            # If there is no wildcard, copy that action name over to the new_action_list
            # TODO do we check for dupes here to make sure we are staying DRY?
            # [MJ] create issue for this
            new_action_list.append(action_list[action])
    return new_action_list


def analyze(policy_file, db_session, from_access_level, from_audit_file):

    requested_actions = get_actions_from_json_policy_file(policy_file)
    expanded_actions = determine_actions_to_expand(requested_actions)

    if from_access_level:
        levels = get_actions_by_access_level(
            db_session, expanded_actions, from_access_level)
        if not levels:
            pass
        else:
            policy_path_elements = policy_file.split('/')
            policy_name = policy_path_elements[-1]
            print("\nPolicy: " + policy_name)
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(levels)
    else:
        print("These are the expanded actions")
        print(expanded_actions)
        determine_risky_actions(expanded_actions, from_audit_file)


def analyze_policy_directory(policy, db_session, from_access_level, from_audit_file):
    file_list = list_files_in_directory(policy)
    print("Access level: " + from_access_level)
    for file in file_list:
        this_file = policy + '/' + file
        analyze(this_file, db_session, from_access_level, from_audit_file)
