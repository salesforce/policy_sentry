"""Templates for the policy_sentry YML files.
These can be used for generating policies
"""
from jinja2 import Template

ACTIONS_TEMPLATE = """mode: actions
name: {{ name }}
actions:
- ''
"""

CRUD_TEMPLATE = """mode: crud
name: {{ name }}
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
}

ACTIONS_TEMPLATE_DICT = {
    "mode": "actions",
    "name": "",
    "actions": [],
}


def create_crud_template(name):
    """Generate the CRUD YML Template with Jinja2"""
    template = Template(CRUD_TEMPLATE)
    msg = template.render(name=name)
    return msg


def create_actions_template(name):
    """Generate the Actions YML template with Jinja2"""
    template = Template(ACTIONS_TEMPLATE)
    msg = template.render(name=name)
    return msg


def get_crud_template_dict():
    """Generate the CRUD template in dict format"""
    return CRUD_TEMPLATE_DICT


def get_actions_template_dict():
    """Get the Actions template in dict format."""
    return ACTIONS_TEMPLATE_DICT
