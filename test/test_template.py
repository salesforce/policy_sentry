import unittest
from policy_sentry.shared.template import create_actions_template, create_crud_template


class TemplateTestCase(unittest.TestCase):
    def test_actions_template(self):
        desired_msg = """# Generate my policy when I know the Actions
roles_with_actions:
- name: myrole
  description: ''
  arn: ''
  actions:
  - ''"""
        actions_template = create_actions_template("myrole")
        self.assertEquals(desired_msg, actions_template)

    def test_crud_template(self):
        desired_msg = """# Generate my policy when I know the access levels and ARNs
roles_with_crud_levels:
- name: myrole
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
    - ''"""
        crud_template = create_crud_template("myrole")
        self.assertEquals(desired_msg, crud_template)
