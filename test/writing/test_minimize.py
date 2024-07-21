import unittest
import json
from policy_sentry.writing.sid_group import SidGroup
from policy_sentry.writing.minimize import minimize_statement_actions
from policy_sentry.querying.all import get_all_actions
from policy_sentry.util.policy_files import get_sid_names_from_policy


class MinimizeWildcardActionsTestCase(unittest.TestCase):
    def test_minimize_statement_actions(self):
        actions_to_minimize = [
            "kms:CreateGrant",
            "kms:CreateCustomKeyStore",
            "ec2:AuthorizeSecurityGroupEgress",
            "ec2:AuthorizeSecurityGroupIngress",
        ]
        desired_result = ["ec2:authorizes*", "kms:createc*", "kms:createg*"]
        all_actions = get_all_actions(lowercase=True)
        minchars = None
        self.maxDiff = None
        # minimized_actions_list = minimize_statement_actions(desired_actions, all_actions, minchars)
        self.assertListEqual(
            sorted(minimize_statement_actions(actions_to_minimize, all_actions, minchars)),
            sorted(desired_result),
        )

    def test_minimize_statement_actions_funky_case(self):
        actions_to_minimize = [
            "kms:creategrant",
            "kms:createcustomkeystore",
            "ec2:authorizesecuritygroupegress",
            "ec2:authorizesecuritygroupingress",
        ]
        desired_result = ["ec2:authorizes*", "kms:createc*", "kms:createg*"]
        all_actions = get_all_actions(lowercase=True)
        minchars = None
        self.maxDiff = None
        # minimized_actions_list = minimize_statement_actions(desired_actions, all_actions, minchars)
        self.assertListEqual(
            sorted(minimize_statement_actions(actions_to_minimize, all_actions, minchars)),
            sorted(desired_result),
        )

    def test_minimize_statement_actions_with_min_chars(self):
        actions_to_minimize = [
            "ec2:AuthorizeSecurityGroupEgress",
            "ec2:AuthorizeSecurityGroupIngress",
        ]
        desired_result = ["ec2:authorizesecurity*"]
        all_actions = get_all_actions(lowercase=True)
        minchars = 17
        self.maxDiff = None
        self.assertListEqual(
            sorted(minimize_statement_actions(actions_to_minimize, all_actions, minchars)),
            sorted(desired_result),
        )

    def test_minimize_statement_actions_with_wildcard(self):
        actions_to_minimize = ["ec2:*"]
        desired_result = ["ec2:*"]
        all_actions = get_all_actions(lowercase=True)
        minchars = None
        self.maxDiff = None
        self.assertListEqual(
            sorted(minimize_statement_actions(actions_to_minimize, all_actions, minchars)),
            sorted(desired_result),
        )

    def test_minimize_rw_same_one(self):
        cfg = {
            "mode": "crud",
            "name": "",
            "read": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter",
            ],
            "write": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter",
            ],
        }
        sid_grp = SidGroup()
        write_format = sid_grp.process_template(cfg, minimize=0)

        """
        Expected result:
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "SsmMultParametermyparameter",
                    "Effect": "Allow",
                    "Action": [
                        "ssm:getpar*",
                        "ssm:deletepar*",
                        "ssm:la*",
                        "ssm:putp*"
                    ],
                    "Resource": [
                        "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter"
                    ]
                }
            ]
        }
        """
        # To future-proof this unit test...
        # (1) check that there is only one SID so it was combined during minimization
        sid_names = get_sid_names_from_policy(write_format)
        self.assertEqual(len(sid_names), 1, "More than one statement returned, expected 1")

    def test_minimize_rw_same(self):
        cfg = {
            "mode": "crud",
            "name": "",
            "read": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter",
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter2",
            ],
            "write": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter",
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter2",
            ],
        }
        sid_grp = SidGroup()
        write_format = sid_grp.process_template(cfg, minimize=1)
        # print(json.dumps(write_format, indent=4))
        """
        the output will look like:

        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "SsmParameterMyparameter",
                    "Effect": "Allow",
                    "Action": [
                        "ssm:getpar*",
                        "ssm:deletepar*",
                        "ssm:la*",
                        "ssm:putp*"
                    ],
                    "Resource": [
                        "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter",
                        "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter2"
                    ]
                }
            ]
        }
        """
        # To future-proof this unit test...
        # (1) check that there is only one SID so it was combined during minimization
        sid_names = get_sid_names_from_policy(write_format)
        self.assertEqual(len(sid_names), 1, "More than one statement returned, expected 1")

        # (2) Check for the presence of certain actions that we know will be there
        self.assertEqual(
            write_format["Statement"][0]["Action"],
            ["ssm:deletepar*", "ssm:getpar*", "ssm:la*", "ssm:putp*", "ssm:un*"],
            "extra actions are returned",
        )
        self.assertEqual(
            write_format["Statement"][0]["Resource"],
            cfg["read"],
            "Wrong resources were returned",
        )

    def test_minimize_rw_different(self):
        cfg = {
            "mode": "crud",
            "name": "",
            "read": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter",
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter2",
            ],
            "write": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter",
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter10",
            ],
        }
        sid_grp = SidGroup()
        write_format = sid_grp.process_template(cfg, minimize=1)
        """
        Expected result:

        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "SsmReadParameter",
                    "Effect": "Allow",
                    "Action": [
                        "ssm:getpar*"
                    ],
                    "Resource": [
                        "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter",
                        "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter2"
                    ]
                },
                {
                    "Sid": "SsmWriteParameter",
                    "Effect": "Allow",
                    "Action": [
                        "ssm:deletepar*",
                        "ssm:la*",
                        "ssm:putp*"
                    ],
                    "Resource": [
                        "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter",
                        "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter10"
                    ]
                }
            ]
        }
        """
        self.assertEqual(
            len(write_format["Statement"]),
            2,
            "More than two statements returned, expected 2",
        )
        self.assertEqual(
            write_format["Statement"][0]["Action"],
            ["ssm:getpar*"],
            "extra actions are returned",
        )
        self.assertEqual(
            write_format["Statement"][0]["Resource"],
            cfg["read"],
            "Wrong resources were returned",
        )
        self.assertEqual(
            write_format["Statement"][1]["Action"],
            ["ssm:deletepar*", "ssm:la*", "ssm:putp*", "ssm:un*"],
            "extra actions are returned",
        )
        self.assertEqual(
            write_format["Statement"][1]["Resource"],
            cfg["write"],
            "Wrong resources were returned",
        )

    def test_minimize_arn_case_bucket(self):
        cfg = {
            "mode": "crud",
            "read": ["arn:aws:s3:::bucket_name"],
            "write": ["arn:aws:s3:::bucket_name"],
        }
        sid_group = SidGroup()
        results = sid_group.process_template(cfg, minimize=0)

        # print(json.dumps(results, indent=4))
        # To future-proof this unit test...
        # (1) check that there is only one SID so it was combined during minimization
        sid_names = get_sid_names_from_policy(results)
        # For S3, it does require iam:PassRole lol because of s3:PutReplicationConfiguration requiring it as an action
        self.assertEqual(len(sid_names), 2, "More than 2 statements returned, expected 2")

    def test_minimize_arn_case_1(self):
        """minimization test with ARN types from test_does_arn_match_case_1"""
        cfg = {
            "mode": "crud",
            "read": ["arn:aws:codecommit:us-east-1:123456789012:MyDemoRepo"],
            "write": ["arn:aws:codecommit:us-east-1:123456789012:MyDemoRepo"],
        }
        sid_group = SidGroup()
        results = sid_group.process_template(cfg, minimize=0)
        sid_names = get_sid_names_from_policy(results)
        self.assertEqual(len(sid_names), 1, "More than one statement returned, expected 1")

    def test_minimize_arn_case_3(self):
        """minimization test with ARN types from test_does_arn_match_case_3"""
        cfg = {
            "mode": "crud",
            "read": [
                "arn:aws:kinesis:us-east-1:account-id:firehose/myfirehose/consumer/someconsumer:${ConsumerCreationTimpstamp}"
            ],
            "write": [
                "arn:aws:kinesis:us-east-1:account-id:firehose/myfirehose/consumer/someconsumer:${ConsumerCreationTimpstamp}"
            ],
        }
        sid_group = SidGroup()
        results = sid_group.process_template(cfg, minimize=0)
        sid_names = get_sid_names_from_policy(results)
        self.assertEqual(len(sid_names), 1, "More than one statement returned, expected 1")

    def test_minimize_arn_case_4(self):
        """minimization test with ARN types from test_does_arn_match_case_4"""
        cfg = {
            "mode": "crud",
            "read": ["arn:aws:batch:region:account-id:job-definition/job-name:revision"],
            "write": ["arn:aws:batch:region:account-id:job-definition/job-name:revision"],
        }
        sid_group = SidGroup()
        results = sid_group.process_template(cfg, minimize=0)
        sid_names = get_sid_names_from_policy(results)
        self.assertEqual(len(sid_names), 1, "More than one statement returned, expected 1")

    def test_minimize_arn_case_5(self):
        """minimization test with ARN types from test_does_arn_match_case_5"""
        cfg = {
            "mode": "crud",
            "read": ["arn:aws:states:region:account-id:stateMachine:stateMachineName"],
            "write": ["arn:aws:states:region:account-id:stateMachine:stateMachineName"],
        }
        sid_group = SidGroup()
        results = sid_group.process_template(cfg, minimize=0)
        sid_names = get_sid_names_from_policy(results)
        self.assertEqual(len(sid_names), 2, "More than two statements returned, expected 2")

    def test_minimize_arn_case_6(self):
        """minimization test with ARN types from test_does_arn_match_case_6"""
        cfg = {
            "mode": "crud",
            "read": ["arn:aws:states:region:account-id:execution:stateMachineName:executionName"],
            "write": ["arn:aws:states:region:account-id:execution:stateMachineName:executionName"],
        }
        sid_group = SidGroup()
        results = sid_group.process_template(cfg, minimize=0)
        sid_names = get_sid_names_from_policy(results)
        self.assertEqual(len(sid_names), 1, "More than one statement returned, expected 1")

    # TODO: Greengrass now has two documentation pages. Need to fix that. Perhaps look to #226 for guidance? idk.
    # def test_minimize_arn_case_7(self):
    #     """minimization test with ARN types from test_does_arn_match_case_7"""
    #     cfg = {
    #         "mode": "crud",
    #         "read": ["arn:aws:greengrass:${Region}:${Account}:/greengrass/definition/devices/1234567/versions/1"],
    #         "write": ["arn:aws:greengrass:${Region}:${Account}:/greengrass/definition/devices/1234567/versions/1"]
    #     }
    #     sid_group = SidGroup()
    #     results = sid_group.process_template(cfg, minimize=0)
    #     sid_names = get_sid_names_from_policy(results)
    #     self.assertEqual(len(sid_names), 1, "More than one statement returned, expected 1")

    def test_GH_364_remove_duplicates_from_minimize(self):
        cfg = {
            "mode": "crud",
            "read": ["arn:aws:rds:*:*:*:test-*"],
            "write": ["arn:aws:rds:*:*:*:test-*"],
            "list": ["arn:aws:rds:*:*:*:test-*"],
            "tagging": ["arn:aws:rds:*:*:*:test-*"],
            "permissions-management": ["arn:aws:rds:*:*:*:test-*"],
        }
        # Bug introduced in https://github.com/salesforce/policy_sentry/pull/252
        sid_group = SidGroup()
        results = sid_group.process_template(cfg, minimize=0)
        print(json.dumps(results, indent=4))
        actions = results["Statement"][0]["Action"]
        actions_set = set(actions)
        self.assertEqual(
            len(actions_set),
            len(actions),
            "There should be no duplicate strings in the actions.",
        )
