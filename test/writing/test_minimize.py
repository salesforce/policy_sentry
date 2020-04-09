import unittest

from policy_sentry.writing.minimize import minimize_statement_actions
from policy_sentry.querying.all import get_all_actions
from policy_sentry.shared.constants import DATABASE_FILE_PATH



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
