import unittest

from policy_sentry.analysis.expand import determine_actions_to_expand, expand, get_expanded_policy


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


class ActionCaseInsensitivityTestCase(unittest.TestCase):
    """AWS action/service names are case insensitive; expansion must follow suit."""

    def test_expand_uppercase_service_wildcard_matches_lowercase(self):
        self.assertEqual(expand("S3:*"), expand("s3:*"))
        self.assertTrue(expand("S3:*"))

    def test_expand_uppercase_action_wildcard_matches_lowercase(self):
        self.assertEqual(expand("S3:Get*"), expand("s3:Get*"))
        self.assertTrue(expand("S3:Get*"))

    def test_expand_mixed_case_action_pattern_matches_lowercase(self):
        self.assertEqual(expand("S3:gEt*"), expand("s3:Get*"))

    def test_expand_unknown_wildcard_still_passes_through(self):
        self.assertEqual(expand("nosuchservice:*"), ["nosuchservice:*"])

    def test_expand_non_wildcard_is_unchanged(self):
        self.assertEqual(expand("S3:GetObject"), ["S3:GetObject"])
        self.assertEqual(determine_actions_to_expand(["S3:GetObject"]), ["S3:GetObject"])
