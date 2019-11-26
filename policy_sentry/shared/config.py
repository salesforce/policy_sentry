# Manages the policy_sentry config directory and files
# Default location is $HOME/.policy_sentry
from pathlib import Path
import os
from policy_sentry.shared.file import read_this_file, create_directory_if_it_doesnt_exist, \
    list_files_in_directory, read_yaml_file
import shutil
import sys
from policy_sentry.shared.constants import HOME, CONFIG_DIRECTORY, DATABASE_FILE_NAME, AUDIT_DIRECTORY_FOLDER


def create_policy_sentry_config_directory():
    """
    Creates a config directory at $HOME/.policy_sentry/
    :return: the path of the database file
    """
    print("Creating the database...")

    database_path = HOME + CONFIG_DIRECTORY + DATABASE_FILE_NAME
    print("We will store the new database here: " + database_path)
    # If the database file already exists
    if os.path.exists(database_path):
        os.remove(database_path)
    elif os.path.exists(HOME + CONFIG_DIRECTORY):
        pass
    # If the config directory does not exist
    else:
        os.mkdir(HOME + CONFIG_DIRECTORY)
    return database_path


def create_audit_directory():
    """
    Creates directory for analyze_iam_policy audit files and places audit files there.
    """
    audit_directory_path = HOME + CONFIG_DIRECTORY + AUDIT_DIRECTORY_FOLDER
    create_directory_if_it_doesnt_exist(audit_directory_path)
    destination = audit_directory_path

    existing_audit_files_directory = os.path.abspath(
        os.path.dirname(__file__)) + '/data/audit/'
    source = existing_audit_files_directory
    file_list = list_files_in_directory(existing_audit_files_directory)

    for file in file_list:
        if file.endswith(".txt"):
            shutil.copy(source + '/' + file, destination)
            print("copying " + file + " to " + destination)


def create_policy_analysis_directory():
    """
    Creates directory for analyze_iam_policy policies.
    """
    policy_analysis_directory_path = HOME + CONFIG_DIRECTORY + 'policy-analysis'
    if os.path.exists(policy_analysis_directory_path):
        pass
    else:
        os.mkdir(policy_analysis_directory_path)


def create_default_overrides_file():
    """
    Copies over the overrides file in the config directory
    """
    existing_overrides_file_name = 'access-level-overrides.yml'
    target_overrides_file_path = HOME + CONFIG_DIRECTORY + existing_overrides_file_name
    existing_overrides_file_path = os.path.abspath(
        os.path.dirname(__file__)) + '/data/' + existing_overrides_file_name
    shutil.copy(existing_overrides_file_path, target_overrides_file_path)
    print(
        f"Copying overrides file {existing_overrides_file_name} to {target_overrides_file_path}")


def create_default_report_config_file():
    """
    Copies over the default report config file to the config directory
    """
    existing_report_config_file = 'report-config.yml'
    target_report_config_file_path = HOME + CONFIG_DIRECTORY + existing_report_config_file
    existing_overrides_file_path = os.path.abspath(
        os.path.dirname(__file__)) + '/data/' + existing_report_config_file
    shutil.copy(existing_overrides_file_path, target_report_config_file_path)
    print(
        f"Copying overrides file {existing_report_config_file} to {target_report_config_file_path}")


def get_action_access_level_overrides_from_yml(
        service, access_level_overrides_file_path=None):
    """
    Read the YML overrides file, which is formatted like: ['ec2']['permissions-management'][action_name].
    Since the AWS Documentation is sometimes outdated, we can use this YML file to
    override whatever they provide in their documentation.
    """
    if not access_level_overrides_file_path:
        access_level_overrides_file_path = os.path.abspath(
            os.path.dirname(__file__)) + '/data/access-level-overrides.yml'
    cfg = read_yaml_file(access_level_overrides_file_path)
    if service in cfg:
        return cfg[service]
    else:
        return False


def determine_access_level_override(
        service,
        action_name,
        provided_access_level,
        service_override_config):
    """
    override_config
    :param service: service, like iam
    :param action_name: action name, like ListUsers
    :param provided_access_level: The access level provided in the scraping process
    :param service_override_config: Specific to each service. returned by get_action_overrides_from_yml
    :return:
    """
    # overrides = get_action_overrides_from_yml(service)
    # To reduce memory, this should be used in the table building,
    # and then run the rest of this for if else statement eval later.
    # Using str.lower to make sure we don't get failing cases if there are
    # minor capitalization differences
    if str.lower(provided_access_level) == str.lower("Read"):
        override_decision = override_access_level(
            service_override_config, action_name, "Read")
    elif str.lower(provided_access_level) == str.lower("Write"):
        override_decision = override_access_level(
            service_override_config, action_name, "Write")
    elif str.lower(provided_access_level) == str.lower("List"):
        override_decision = override_access_level(
            service_override_config, action_name, "List")
    elif str.lower(provided_access_level) == str.lower("Permissions management"):
        override_decision = override_access_level(
            service_override_config, action_name, "Permissions management")
    elif str.lower(provided_access_level) == str.lower("Tagging"):
        override_decision = override_access_level(
            service_override_config, action_name, "Tagging")
    else:
        print(
            f"Unknown error - determine_override_status() can't determine the access level of"
            f" {service}:{action_name} during the scraping process. The provided access level "
            f"was {provided_access_level}. Exiting...")
        sys.exit()
    return override_decision


def override_access_level(
        service_override_config,
        action_name,
        provided_access_level):
    """
    Given the service-specific override config, determine whether or not the
    override config tells us to override the access level in the documentation.
    :param service_override_config: Given that the name
    :param action_name: The name of the action
    :param provided_access_level: Read, Write, List, Tagging, or 'Permissions management'.
    :return:
    """
    real_access_level = []  # This will hold the real access level in index 0
    for i in range(len(service_override_config.keys())):
        keys = list(service_override_config.keys())
        actions_list = service_override_config[keys[i]]
        # If it exists in the list, then set the real_access_level to the key (key is read, write, list, etc.)
        # Once we meet this condition, break the loop so we can return the
        # value
        if str.lower(action_name) in actions_list:
            real_access_level.append(keys[i])
            break
        else:
            continue
    # first index will contain the access level given in the override config for that action.
    # since we break the loop, we know it only contains one value.
    if len(real_access_level) > 0:
        # If AWS hasn't fixed their documentation yet, then our YAML override cfg will not match their documentation.
        # Therefore, accept our override instead.
        if real_access_level[0] != provided_access_level:
            return real_access_level[0]
        # Otherwise, they have fixed their documentation because our override file matches their documentation.
        # Therefore, return false because we don't need to override
        else:
            return False
    else:
        return False
