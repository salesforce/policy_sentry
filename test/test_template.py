import unittest
from policy_sentry.shared.template import create_actions_template, create_crud_template


class TemplateTestCase(unittest.TestCase):
    def test_actions_template(self):
        desired_msg = """# Generate my policy when I know the Actions
roles_with_actions:
- name: myrole
  description: '' # Insert a description/justification here for readability
  arn: '' # Insert an ARN here for readability
  actions:
  - ''  # Fill in your IAM actions here"""
        actions_template = create_actions_template("myrole")
        self.assertEquals(desired_msg, actions_template)

    def test_crud_template(self):
        desired_msg = '''# Generate my policy when I know the access levels and ARNs
roles_with_crud_levels:
- name: myrole
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
    - '' # Insert ARNs or comment out'''
        crud_template = create_crud_template("myrole")
        self.assertEquals(desired_msg, crud_template)
