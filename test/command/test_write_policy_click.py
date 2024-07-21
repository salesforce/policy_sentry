import os
import json
import unittest
from click.testing import CliRunner
from policy_sentry.command.write_policy import write_policy
from policy_sentry.util.policy_files import get_sid_names_from_policy

test_file_directory = os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir, "examples", "yml")


class PolicySentryClickUnitTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_write_policy_basic_with_click(self):
        """command.write_policy: using crud.yml should return exit code 0"""
        template_file = os.path.join(test_file_directory, "crud.yml")
        result = self.runner.invoke(write_policy, ["--input-file", template_file])
        self.assertTrue(result.exit_code == 0)

    def test_click_crud_case_1(self):
        """write_policy: using 1-ssm-read.yml"""
        template_file = os.path.join(test_file_directory, "crud-cases", "1-ssm-read.yml")
        result = self.runner.invoke(write_policy, ["--input-file", template_file])
        result_json = json.loads(result.output)
        self.assertListEqual(get_sid_names_from_policy(result_json), ["SsmReadParameter"])
        self.assertTrue(result.exit_code == 0)

    def test_click_crud_case_2(self):
        """write_policy: using 2-skip-resource-constraints.yml"""
        template_file = os.path.join(test_file_directory, "crud-cases", "2-skip-resource-constraints.yml")
        result = self.runner.invoke(write_policy, ["--input-file", template_file])
        result_json = json.loads(result.output)
        self.assertListEqual(get_sid_names_from_policy(result_json), ["SkipResourceConstraints"])
        self.assertTrue(result.exit_code == 0)

    def test_click_crud_case_3(self):
        """write_policy: using 3-wildcard-only-single-actions.yml"""
        template_file = os.path.join(test_file_directory, "crud-cases", "3-wildcard-only-single-actions.yml")
        result = self.runner.invoke(write_policy, ["--input-file", template_file])
        result_json = json.loads(result.output)
        self.assertListEqual(get_sid_names_from_policy(result_json), ["MultMultNone"])
        self.assertTrue(result.exit_code == 0)

    def test_click_crud_case_4(self):
        """write_policy: using 4-wildcard-only-bulk-selection.yml"""
        template_file = os.path.join(test_file_directory, "crud-cases", "4-wildcard-only-bulk-selection.yml")
        result = self.runner.invoke(write_policy, ["--input-file", template_file])
        result_json = json.loads(result.output)
        self.assertListEqual(get_sid_names_from_policy(result_json), ["MultMultNone"])
        self.assertTrue(result.exit_code == 0)
