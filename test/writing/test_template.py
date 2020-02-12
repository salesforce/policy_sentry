import unittest
from policy_sentry.writing.template import create_actions_template, create_crud_template


class TemplateTestCase(unittest.TestCase):
    def test_actions_template(self):
        desired_msg = """mode: actions
name: myrole
actions:
- ''"""
        actions_template = create_actions_template("myrole")
        self.assertEqual(desired_msg, actions_template)

    def test_crud_template(self):
        desired_msg = """mode: crud
name: myrole
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
  - ''"""
        crud_template = create_crud_template("myrole")
        self.assertEqual(desired_msg, crud_template)
