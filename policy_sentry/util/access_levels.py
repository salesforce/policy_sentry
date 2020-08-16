"""
Util methods for handling operations relating to access levels.
All of these access_levels methods are specific to policy sentry internals."""
import sys
import logging

logger = logging.getLogger(__name__)


def override_access_level(service_override_config, action_name, provided_access_level):
    """
    Given the service-specific override config, determine whether or not the
    override config tells us to override the access level in the documentation.

    Arguments:
        service_override_config: Given that the name
        action_name: The name of the action
        provided_access_level: Read, Write, List, Tagging, or 'Permissions management'.
    """
    real_access_level = []  # This will hold the real access level in index 0
    try:
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
    except AttributeError as a_e:
        logger.debug(
            "AttributeError: %s\nService overrides config is %s\nKeys are %s",
            a_e,
            service_override_config,
            service_override_config.keys(),
        )
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


def transform_access_level_text(access_level):
    """This takes the Click choices for access levels, like permissions-management, and
    returns the text format matching that access level, but in the format that the database expects"""
    if access_level == "read":
        level = "Read"
    elif access_level == "write":
        level = "Write"
    elif access_level == "list":
        level = "List"
    elif access_level == "tagging":
        level = "Tagging"
    elif access_level == "permissions-management":
        level = "Permissions management"
    else:
        logger.debug("Error: Please specify the correct access level.")
        sys.exit(0)
    return level


def determine_access_level_override(
    service, action_name, provided_access_level, service_override_config
):
    """
    Arguments:
        service: service, like iam
        action_name: action name, like ListUsers
        provided_access_level: The access level provided in the scraping process
        service_override_config: Specific to each service. returned by get_action_overrides_from_yml
    """
    # overrides = get_action_overrides_from_yml(service)
    # To reduce memory, this should be used in the table building,
    # and then run the rest of this for if else statement eval later.
    # Using str.lower to make sure we don't get failing cases if there are
    # minor capitalization differences
    if str.lower(provided_access_level) == str.lower("Read"):
        override_decision = override_access_level(
            service_override_config, str.lower(action_name), "Read"
        )
    elif str.lower(provided_access_level) == str.lower("Write"):
        override_decision = override_access_level(
            service_override_config, str.lower(action_name), "Write"
        )
    elif str.lower(provided_access_level) == str.lower("List"):
        override_decision = override_access_level(
            service_override_config, str.lower(action_name), "List"
        )
    elif str.lower(provided_access_level) == str.lower("Permissions management"):
        override_decision = override_access_level(
            service_override_config, str.lower(action_name), "Permissions management"
        )
    elif str.lower(provided_access_level) == str.lower("Tagging"):
        override_decision = override_access_level(
            service_override_config, str.lower(action_name), "Tagging"
        )
    else:
        logger.debug(
            "Unknown error - determine_override_status() can't determine the access level of %s:%s during "
            "the scraping process. The provided access level was %s. Exiting...",
            service,
            str.lower(action_name),
            provided_access_level,
        )
        sys.exit()
    return override_decision
