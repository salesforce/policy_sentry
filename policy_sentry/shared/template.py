"""Templates for the policy_sentry YML files.
These can be used for generating policies
"""
from jinja2 import Template

ACTIONS_TEMPLATE = '''# Generate my policy when I know the Actions
roles_with_actions:
- name: {{ name }}
  description: ''
  arn: ''
  actions:
  - ''
'''

CRUD_TEMPLATE = '''# Generate my policy when I know the access levels and ARNs
roles_with_crud_levels:
- name: {{ name }}
  description: ''
  arn: ''
  # Insert ARNs under each access level below
  # If you do not need to use certain access levels, delete them.
  read:
    - ''
  write:
    - ''
  list:
    - ''
  tag:
    - ''
  permissions-management:
    - ''
  # If the policy needs to use IAM actions that cannot be restricted to ARNs,
  # like ssm:DescribeParameters, specify those actions here.
  wildcard:
    - ''
'''


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
