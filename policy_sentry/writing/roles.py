"""
Roles is a data holder for sublists. It supports the write-policy actions mode.
In the future, this data structure should probably go away, or it should at least be renamed.
"""
import sys
import logging

logger = logging.getLogger(__name__)


class Roles:
    """
    This is just a data holder for list of lists - used for running the YAML option.
    The sublists should all contain these:
    Indexes:
    0 - Name
    1 - Description
    2 - ARN (string ARN of the role)
    3 - Actions (list of AWS API Actions)
    """
    roles = None

    def __init__(self):
        """Create the data holder for action_lists"""
        self.roles = []

    def add_role(self, role):
        """Chain write-policy action mode files together"""
        self.roles.append(role)

    def get_roles(self):
        """Get the full data structure of action_list holder."""
        return self.roles

    def process_actions_config(self, cfg):
        """Given the YAML file used for the list of actions config, process it."""
        try:
            for template in cfg:
                if template == 'policy_with_actions':
                    # for principal in cfg[category]:
                    self.add_role(
                        [
                            cfg['policy_with_actions']['name'],
                            cfg['policy_with_actions']['description'],
                            cfg['policy_with_actions']['role_arn'],
                            cfg['policy_with_actions']['actions'],
                        ]
                    )
        except KeyError as k_e:
            logger.critical("Yaml file is missing this block: %s", k_e.args[0])
            sys.exit()
        # except TypeError:
        #     logger.critical("Yaml file is not formatted properly. Please see the documentation for the proper format.")
        #     # logger.critical("Error: " + te.args[0])
        #     sys.exit()
