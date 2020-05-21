"""Templates for the policy_sentry YML files.
These can be used for generating policies
"""

ACTIONS_TEMPLATE = """mode: actions
name: ''
actions:
- ''
"""

CRUD_TEMPLATE = """mode: crud
name: ''
# Specify resource ARNs
read:
- ''
write:
- ''
list:
- ''
tagging:
- ''
permissions-management:
- ''
# Actions that do not support resource constraints
wildcard-only:
  single-actions: # standalone actions
  - ''
  # Service-wide - like 's3' or 'ec2'
  service-read:
  - ''
  service-write:
  - ''
  service-list:
  - ''
  service-tagging:
  - ''
  service-permissions-management:
  - ''
# Skip resource constraint requirements by listing actions here.
skip-resource-constraints:
- ''
# Exclude actions from the output by specifying them here. Accepts wildcards, like kms:Delete*
exclude-actions:
- ''
"""

CRUD_TEMPLATE_DICT = {
    "mode": "crud",
    "name": "",
    "read": [],
    "write": [],
    "list": [],
    "tagging": [],
    "permissions-management": [],
    "wildcard-only": {
        "single-actions": [],
        "service-read": [],
        "service-write": [],
        "service-list": [],
        "service-tagging": [],
        "service-permissions-management": [],
    },
    "skip-resource-constraints": [],
    "exclude-actions": []
}

ACTIONS_TEMPLATE_DICT = {"mode": "actions", "name": "", "actions": []}


def create_crud_template():
    """Generate the CRUD YML Template """
    return CRUD_TEMPLATE


def create_actions_template():
    """Generate the Actions YML template"""
    return ACTIONS_TEMPLATE


def get_crud_template_dict():
    """Generate the CRUD template in dict format"""
    return CRUD_TEMPLATE_DICT


def get_actions_template_dict():
    """Get the Actions template in dict format."""
    return ACTIONS_TEMPLATE_DICT
