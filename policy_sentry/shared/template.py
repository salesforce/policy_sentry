"""
Templates for the YML files that policy_sentry expects
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
  # Insert ARNs below
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
  # Provide a list of IAM actions that cannot be restricted to ARNs
  wildcard:
    - ''
'''


def create_crud_template(name):
    template = Template(CRUD_TEMPLATE)
    msg = template.render(name=name)
    return msg


def create_actions_template(name):
    template = Template(ACTIONS_TEMPLATE)
    msg = template.render(name=name)
    return msg
