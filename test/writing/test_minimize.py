import unittest

from policy_sentry.writing.minimize import minimize_statement_actions
from policy_sentry.querying.all import get_all_actions


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
            sorted(
                minimize_statement_actions(actions_to_minimize, all_actions, minchars)
            ),
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
            sorted(
                minimize_statement_actions(actions_to_minimize, all_actions, minchars)
            ),
            sorted(desired_result),
        )

    def test_minimize_rw_same(self):
        cfg = {
            "mode": "crud",
            "name": "",
            "read": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter",
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter2"
            ],
            "write": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter",
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter2"
            ]
        }
        sid_grp = SidGroup()
        write_format = sid_grp.process_template(cfg,minimize=1)
        write_format.pop('Version')
        self.assertEqual(len(write_format['Statement']), 1, "More than one statement returned, expected 1")
        expected_action = ['ssm:getpar*','ssm:deletepar*','ssm:la*','ssm:putp*']
        self.assertEqual(write_format['Statement'][0]['Action'], expected_action, "extra actions are returned")
        self.assertEqual(write_format['Statement'][0]['Resource'], cfg['read'], "Wrong resources were returned")

    def test_minimize_rw_different(self):
        cfg = {
            "mode": "crud",
            "name": "",
            "read": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter",
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter2"
            ],
            "write": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter",
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter10"
            ]
        }
        sid_grp = SidGroup()
        write_format = sid_grp.process_template(cfg,minimize=1)
        write_format.pop('Version')
        self.assertEqual(len(write_format['Statement']), 2, "More than one statement returned, expected 1")
        self.assertEqual(write_format['Statement'][0]['Action'], ['ssm:getpar*'], "extra actions are returned")
        self.assertEqual(write_format['Statement'][0]['Resource'], cfg['read'], "Wrong resources were returned")
        self.assertEqual(write_format['Statement'][1]['Action'], ['ssm:deletepar*', 'ssm:la*', 'ssm:putp*'],
                         "extra actions are returned")
        self.assertEqual(write_format['Statement'][1]['Resource'], cfg['write'], "Wrong resources were returned")

