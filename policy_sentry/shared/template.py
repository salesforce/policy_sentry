"""
Templates for the YML files that policy_sentry expects
"""
from jinja2 import Template

actions_template = '''# Generate my policy when I know the Actions
roles_with_actions:
- name: {{ name }}
  description: '' # Insert a description/justification here for readability
  arn: '' # Insert an ARN here for readability
  actions:
  - ''  # Fill in your IAM actions here
'''

crud_template = '''# Generate my policy when I know the access levels and ARNs
roles_with_crud_levels:
- name: {{ name }}
  description: '' # Insert a description/justification here for readability
  arn: '' # Insert an ARN here for readability
  read:
    - '' # Insert ARNs or comment out
  write:
    - '' # Insert ARNs or comment out
  list:
    - '' # Insert ARNs or comment out
  tag:
    - '' # Insert ARNs or comment out
  permissions-management:
    - '' # Insert ARNs or comment out
'''


def create_crud_template(name):
    tm = Template(crud_template)
    msg = tm.render(name=name)
    return msg


def create_actions_template(name):
    tm = Template(actions_template)
    msg = tm.render(name=name)
    return msg
