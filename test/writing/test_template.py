import unittest
from policy_sentry.writing.template import create_actions_template, create_crud_template


class TemplateTestCase(unittest.TestCase):
    def test_actions_template(self):
        desired_msg = """mode: actions
name: ''
actions:
- ''
"""
        actions_template = create_actions_template()
        self.assertEqual(desired_msg, actions_template)

    def test_crud_template(self):
        desired_msg = """mode: crud
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
        crud_template = create_crud_template()
        self.maxDiff = None
        self.assertEqual(desired_msg, crud_template)
