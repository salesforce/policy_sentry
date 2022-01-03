import os
import logging
import json
import re
import requests
from policy_sentry.shared.constants import (
    IAM_DATASET_URL,
    SERVICE_AUTHORIZATION_URL_PREFIX,
    BUNDLED_ACCESS_OVERRIDES_FILE,
    INFER_ACTION_ACCESS_LEVEL
)
from policy_sentry.util.access_levels import determine_access_level_override
from policy_sentry.util.file import read_yaml_file

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

def get_iam_dataset(dataset_url):
    """
    Fetch the iam-defintions.json file from our Github repo URL
    """
    resp = requests.get(dataset_url)

    try:
        return resp.json()
    except Exception as e:
        logger.error(f'Could not download IAM Dataset {e}')
        exit(1)

def get_action_access_level_overrides_from_yml(
    service, access_level_overrides_file_path=None
):
    """
    Read the YML overrides file, which is formatted like:
        ['ec2']['permissions-management'][action_name].

    Since the AWS Documentation is sometimes outdated, we can use this YML file to     override whatever they provide in their documentation.
    """
    if not access_level_overrides_file_path:
        access_level_overrides_file_path = BUNDLED_ACCESS_OVERRIDES_FILE
    cfg = read_yaml_file(access_level_overrides_file_path)
    if service in cfg:
        return cfg[service]
    else:
        return False

def infer_action_access_level(action, privileges):
    """
    Given an action and a dictionary of all actions for that service, find the actions that begin with similar prefix and try to infer the access level

    IAM dataset we download includes some undocumented actions that have access level of "Unknown" We can either handle it by using the
    overrides file or using the infer_action_access_level function which will look at actions with similar names and try to infer the correct
    access level based on the majority access level with similar names.
    """

    # Find all distinguished words in a camel case string (CreateBlueprint -> ['Create', 'Blueprint'])
    words = re.findall('([A-Z][a-z]+)', action)

    matching_privileges_access_levels = []
    if words:
        # The first word is usually a good indicator or access level (Describe, List, Create, etc.)
        action_descriptor = words[0]

        # Find actions with similar starting words, add all the access levels to a list
        for privilege in privileges:
            if re.match(f'^{action_descriptor}', privilege["privilege"]):
                matching_privileges_access_levels.append(privilege["access_level"])

        # If we found some access levels, find the one that occurs most often
        if matching_privileges_access_levels:
            mode = max(set(matching_privileges_access_levels), key = matching_privileges_access_levels.count)
            return mode

    return 'Unknown'

def create_database(destination_directory, access_level_overrides_file):
    """
    Create the JSON Data source that holds the IAM data.

    :param destination_directory:
    :param access_level_overrides_file: The path to the file that we use for overriding access levels that are incorrect in the AWS documentation
    :return:
    """
    iam_definition_file = os.path.join(destination_directory, "iam-definition.json")
    schema = get_iam_dataset(IAM_DATASET_URL)

    for s_idx, service in enumerate(schema):
        service_prefix = service.get("prefix")
        
        access_level_overrides_cfg = get_action_access_level_overrides_from_yml(
                service_prefix, access_level_overrides_file
            )

        filename = 'list_{0}'.format(service.get("service_name").replace(' ', '')).lower()+'.html'
        schema[s_idx]['service_authorization_url'] = SERVICE_AUTHORIZATION_URL_PREFIX+'/'+filename

        for a_idx, action in enumerate(service.get("privileges")):
            action_name = action.get("privilege", "")
            access_level = action.get("access_level", "")
            schema[s_idx]["privileges"][a_idx]["api_documentation_link"] = f"https://docs.aws.amazon.com/{service_prefix}/latest/APIReference/API_{action_name}.html"

            if access_level.lower() == 'unknown' and INFER_ACTION_ACCESS_LEVEL:
                access_level = infer_action_access_level(action_name, service.get("privileges"))
                schema[s_idx]["privileges"][a_idx]["access_level"] = access_level

            if access_level_overrides_cfg:
                override_result = determine_access_level_override(
                    service_prefix,
                    action_name,
                    access_level,
                    access_level_overrides_cfg,
                )
                if override_result:
                    
                    access_level = override_result
                    logger.debug(
                        "Override: Setting access level for %s:%s to %s",
                        service_prefix,
                        action_name,
                        access_level,
                    )
                    schema[s_idx]["privileges"][a_idx]["access_level"] = access_level

    with open(iam_definition_file, "w") as file:
        json.dump(schema, file, indent=4)
    logger.info("Wrote IAM definition file to path: ", iam_definition_file)
