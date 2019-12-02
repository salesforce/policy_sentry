"""
Functions to support creating the proper resources in the Policy Sentry Config directory - ~/.policy_sentry.
"""
import os
import sys
import shutil
from distutils.dir_util import copy_tree
from policy_sentry.shared.file import create_directory_if_it_doesnt_exist, \
    list_files_in_directory, read_yaml_file
from policy_sentry.shared.constants import HOME, CONFIG_DIRECTORY, AUDIT_DIRECTORY_PATH, DATABASE_FILE_PATH, \
    HTML_DIRECTORY_PATH, HTML_DATA_DIRECTORY_SUBFOLDER


def create_policy_sentry_config_directory():
    """
    Creates a config directory at $HOME/.policy_sentry/
    :return: the path of the database file
    """
    print("Creating the database...")

    print("We will store the new database here: " + DATABASE_FILE_PATH)
    # If the database file already exists
    if os.path.exists(DATABASE_FILE_PATH):
        os.remove(DATABASE_FILE_PATH)
    elif os.path.exists(HOME + CONFIG_DIRECTORY):
        pass
    # If the config directory does not exist
    else:
        os.mkdir(HOME + CONFIG_DIRECTORY)
    return DATABASE_FILE_PATH


def create_html_docs_directory():
    """
    Copies the HTML files from the pip package over to its own folder in the CONFIG_DIRECTORY.
    Also copies over the links.yml file, which is a mapping of services and relevant HTML links in the AWS docs.
    Essentially:
    mkdir -p ~/.policy_sentry/data/docs
    cp -r $MODULE_DIR/policy_sentry/shared/data/docs ~/.policy_sentry/data/docs
    :return:
    """
    create_directory_if_it_doesnt_exist(HTML_DIRECTORY_PATH)
    # Copy from the existing html docs folder - the path ./policy_sentry/shared/data/docs within this repository
    existing_html_docs_folder = os.path.abspath(os.path.dirname(__file__)) + HTML_DATA_DIRECTORY_SUBFOLDER
    copy_tree(existing_html_docs_folder, HTML_DIRECTORY_PATH)
    # Copy the links.yml file from here to the config directory
    existing_links_file = os.path.abspath(os.path.dirname(__file__)) + '/' + 'links.yml'
    target_links_file = HOME + CONFIG_DIRECTORY + 'links.yml'
    shutil.copy(existing_links_file, target_links_file)


def create_audit_directory():
    """
    Creates directory for analyze_iam_policy audit files and places audit files there.

    Essentially:
    mkdir -p ~/.policy_sentry/audit
    cp -r $MODULE_DIR/policy_sentry/shared/data/audit/ ~/.policy_sentry/audit/
    """
    create_directory_if_it_doesnt_exist(AUDIT_DIRECTORY_PATH)
    destination = AUDIT_DIRECTORY_PATH

    existing_audit_files_directory = os.path.abspath(os.path.dirname(__file__)) + '/data/audit/'
    source = existing_audit_files_directory
    file_list = list_files_in_directory(existing_audit_files_directory)

    for file in file_list:
        if file.endswith(".txt"):
            shutil.copy(source + '/' + file, destination)
            print("copying " + file + " to " + destination)


def create_policy_analysis_directory():
    """
    Creates directory for analyze_iam_policy policies.

    Essentially:
    mkdir -p ~/.policy_sentry/analysis
    """
    policy_analysis_directory_path = HOME + CONFIG_DIRECTORY + 'analysis'
    if os.path.exists(policy_analysis_directory_path):
        pass
    else:
        os.mkdir(policy_analysis_directory_path)


def create_default_overrides_file():
    """
    Copies over the overrides file in the config directory

    Essentially:
    cp $MODULE_DIR/policy_sentry/shared/data/access-level-overrides.yml ~/policy_sentry/access-level-overrides.yml
    """
    existing_overrides_file_name = 'access-level-overrides.yml'
    target_overrides_file_path = HOME + CONFIG_DIRECTORY + existing_overrides_file_name
    existing_overrides_file_path = os.path.abspath(os.path.dirname(__file__)) + '/data/' + existing_overrides_file_name
    shutil.copy(existing_overrides_file_path, target_overrides_file_path)
    print(
        f"Copying overrides file {existing_overrides_file_name} to {target_overrides_file_path}")


def create_default_report_config_file():
    """
    Copies over the default report config file to the config directory

    Essentially:
    cp $MODULE_DIR/policy_sentry/shared/data/audit/report-config.yml ~/policy_sentry/audit/report-config.yml
    """
    existing_report_config_file = 'report-config.yml'
    target_report_config_file_path = AUDIT_DIRECTORY_PATH + existing_report_config_file
    existing_overrides_file_path = os.path.abspath(os.path.dirname(
        __file__)) + '/data/' + 'audit/' + existing_report_config_file
    shutil.copy(existing_overrides_file_path, target_report_config_file_path)
    print(
        f"Copying overrides file {existing_report_config_file} to {target_report_config_file_path}")


def get_action_access_level_overrides_from_yml(
        service, access_level_overrides_file_path=None):
    """
    Read the YML overrides file, which is formatted like:
    ['ec2']['permissions-management'][action_name].
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
        # pylint: disable=no-else-break
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
