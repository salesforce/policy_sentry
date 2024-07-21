import unittest
from policy_sentry.analysis.expand import get_expanded_policy


class PolicyExpansionTestCase(unittest.TestCase):
    def test_policy_expansion(self):
        """command.expand_policy.get_expanded_policy: Test the expansion of the cloud9 service"""
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "TestSID",
                    "Effect": "Allow",
                    "Action": ["cloud9:*"],
                    "Resource": "*",
                }
            ],
        }
        output = get_expanded_policy(policy)
        # print(json.dumps(output, indent=4))
        desired_output = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "TestSID",
                    "Effect": "Allow",
                    "Action": [
                        "cloud9:CreateEnvironmentEC2",
                        "cloud9:CreateEnvironmentMembership",
                        "cloud9:DeleteEnvironment",
                        "cloud9:DeleteEnvironmentMembership",
                        "cloud9:DescribeEnvironmentMemberships",
                        "cloud9:DescribeEnvironmentStatus",
                        "cloud9:DescribeEnvironments",
                        "cloud9:GetUserSettings",
                        "cloud9:ListEnvironments",
                        "cloud9:ListTagsForResource",
                        "cloud9:TagResource",
                        "cloud9:UntagResource",
                        "cloud9:UpdateEnvironment",
                        "cloud9:UpdateEnvironmentMembership",
                        "cloud9:UpdateUserSettings",
                    ],
                    "Resource": "*",
                }
            ],
        }
        expected_statement_ids = ["TestSID"]
        for statement in output.get("Statement"):
            self.assertTrue(statement.get("Sid") in expected_statement_ids)
        expected_actions = [
            "cloud9:CreateEnvironmentEC2",
            "cloud9:CreateEnvironmentMembership",
            "cloud9:DeleteEnvironment",
            "cloud9:DeleteEnvironmentMembership",
            "cloud9:DescribeEnvironmentMemberships",
            "cloud9:DescribeEnvironmentStatus",
            "cloud9:DescribeEnvironments",
            "cloud9:GetUserSettings",
            "cloud9:ListEnvironments",
            "cloud9:ListTagsForResource",
            "cloud9:TagResource",
            "cloud9:UntagResource",
            "cloud9:UpdateEnvironment",
            "cloud9:UpdateEnvironmentMembership",
            "cloud9:UpdateUserSettings",
        ]
        for action in expected_actions:
            self.assertTrue(action in output["Statement"][0]["Action"])
