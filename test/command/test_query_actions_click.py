import json
import unittest
from click.testing import CliRunner
from policy_sentry.command.query import query


class QueryClickUnitTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_query_action_table_basic_with_click(self):
        """command.query.query_action_table: should return exit code 0"""
        result = self.runner.invoke(query, ["action-table", "--service", "ram"])
        self.assertTrue(result.exit_code == 0)

    def test_click_query_action_table(self):
        """command.query.query_action_table: click testing"""
        cases = [
            [
                "action-table",
                "--service",
                "all",
                "--access-level",
                "permissions-management",
            ],
            ["action-table", "--service", "all", "--resource-type", "*"],
            ["action-table", "--service", "all"],
            [
                "action-table",
                "--service",
                "ram",
                "--access-level",
                "permissions-management",
            ],
            [
                "action-table",
                "--service",
                "ram",
                "--access-level",
                "permissions-management",
                "--resource-type",
                "resource-share",
            ],
            ["action-table", "--service", "ses", "--condition", "ses:FeedbackAddress"],
            ["action-table", "--service", "ssm", "--resource-type", "*"],
            ["action-table", "--service", "ram", "--name", "tagresource"],
            ["action-table", "--service", "ssm", "--resource-type", "parameter"],
            ["action-table", "--service", "ram"],
        ]
        for case in cases:
            result = self.runner.invoke(query, case)
            print(result.output)
            self.assertTrue(result.exit_code == 0)

    def test_click_query_arn_table(self):
        """command.query.query_arn_table: click testing"""
        cases = [
            ["arn-table", "--service", "ssm"],
            ["arn-table", "--service", "cloud9", "--list-arn-types"],
            ["arn-table", "--service", "cloud9", "--name", "environment"],
        ]
        for case in cases:
            result = self.runner.invoke(query, case)
            print(result.output)
            self.assertTrue(result.exit_code == 0)

    def test_click_query_condition_table(self):
        """command.query.query_condition_table: click testing"""
        cases = [
            ["condition-table", "--service", "cloud9"],
            ["condition-table", "--service", "cloud9", "--name", "cloud9:Permissions"],
        ]
        for case in cases:
            result = self.runner.invoke(query, case)
            print(result.output)
            self.assertTrue(result.exit_code == 0)
