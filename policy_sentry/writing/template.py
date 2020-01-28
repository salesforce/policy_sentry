"""Templates for the policy_sentry YML files.
These can be used for generating policies
"""
from jinja2 import Template

ACTIONS_TEMPLATE = '''# Generate my policy when I know the Actions
policy_with_actions:
- name: {{ name }}
  description: '' # For human auditability
  role_arn: '' # For human auditability
  actions:
  - ''
'''

CRUD_TEMPLATE = '''# Generate my policy when I know the access levels and ARNs
policy_with_crud_levels:
- name: {{ name }}
  description: '' # For human auditability
  role_arn: '' # For human auditability
  # Insert ARNs under each access level below
  # If you do not need to use certain access levels, delete them.
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
  # If the policy needs to use IAM actions that cannot be restricted to ARNs,
  # like ssm:DescribeParameters, specify those actions here.
  wildcard:
    - ''
'''

CRUD_TEMPLATE_DICT = {
    'policy_with_crud_levels': [
        {
            'name': '',
            'description': '',
            'role_arn': '',
            'read': [],
            'write': [],
            'list': [],
            'tagging': [],
            'permissions-management': [],
            'wildcard': [],
        }
    ]
}

ACTIONS_TEMPLATE_DICT = {
    'policy_with_actions': [
        {
            'name': '',
            'description': '',
            'role_arn': '',
            'actions': [],
        }
    ]
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
