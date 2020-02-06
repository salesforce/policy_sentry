import unittest
from policy_sentry.writing.template import create_actions_template, create_crud_template


class TemplateTestCase(unittest.TestCase):
    def test_actions_template(self):
        desired_msg = """# Generate my policy when I know the Actions
policy_with_actions:
  name: myrole
  description: '' # For human auditability
  role_arn: '' # For human auditability
  actions:
  - ''"""
        actions_template = create_actions_template("myrole")
        self.assertEqual(desired_msg, actions_template)

    def test_crud_template(self):
        desired_msg = """# Generate my policy when I know the access levels and ARNs
policy_with_crud_levels:
  name: myrole
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
    - ''"""
        crud_template = create_crud_template("myrole")
        self.assertEqual(desired_msg, crud_template)
