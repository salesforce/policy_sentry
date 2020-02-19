import unittest
import json
from policy_sentry.shared.database import connect_db
from policy_sentry.command.write_policy import write_policy_with_template
from policy_sentry.shared.constants import DATABASE_FILE_PATH

db_session = connect_db(DATABASE_FILE_PATH)


valid_cfg_for_crud = {
    "mode": "crud",
    "name": "RoleNameWithCRUD",
    "read": [
        "arn:aws:s3:::example-org-sbx-vmimport",
        "arn:aws:s3:::example-kinnaird",
        "arn:aws:ssm:us-east-1:123456789012:parameter/test",
        "arn:aws:ssm:us-east-1:123456789012:parameter/test2",
        "arn:aws:kms:us-east-1:123456789012:key/123456",
        "arn:aws:s3:::job/jobid",
        "arn:aws:s3:::example-org-sbx-vmimport/stuff",
    ],
    "write": [
        "arn:aws:s3:::example-org-s3-access-logs",
        "arn:aws:s3:::example-org-sbx-vmimport/stuff",
        "arn:aws:secretsmanager:us-east-1:12345:secret:mysecret",
        "arn:aws:kms:us-east-1:123456789012:key/123456",
    ],
    "list": [
        "arn:aws:s3:::example-org-flow-logs",
        "arn:aws:s3:::example-org-sbx-vmimport/stuff",
    ],
    "tagging": ["arn:aws:ssm:us-east-1:123456789012:parameter/test"],
    "permissions-management": ["arn:aws:s3:::example-org-s3-access-logs"],
}

valid_cfg_for_actions = {
    "mode": "actions",
    "name": "RoleNameWithActions",
    "actions": [
        "kms:CreateGrant",
        "kms:CreateCustomKeyStore",
        "ec2:AuthorizeSecurityGroupEgress",
        "ec2:AuthorizeSecurityGroupIngress",
    ],
}


class YamlValidationOverallTestCase(unittest.TestCase):
    def test_allow_missing_name(self):
        """
        test_actions_missing_name: write-policy when the YAML file is missing a name
        :return:
        """
        cfg_with_missing_name = {
            "mode": "actions",
            "actions": [
                "kms:CreateGrant",
                "kms:CreateCustomKeyStore",
                "ec2:AuthorizeSecurityGroupEgress",
                "ec2:AuthorizeSecurityGroupIngress",
            ],
        }
        #  This should NOT raise an exception so leaving it as-is.
        policy = write_policy_with_template(db_session, cfg_with_missing_name)

    def test_allow_missing_arn(self):
        """
        test_actions_missing_arn: write-policy actions command when YAML file block is missing an ARN
        :return:
        """
        cfg_with_missing_actions = {
            "mode": "actions",
            "name": "RoleNameWithActions",
            "actions": [
                "kms:CreateGrant",
                "kms:CreateCustomKeyStore",
                "ec2:AuthorizeSecurityGroupEgress",
                "ec2:AuthorizeSecurityGroupIngress",
            ],
        }
        #  This should NOT raise an exception so leaving it as-is.
        policy = write_policy_with_template(db_session, cfg_with_missing_actions)


class YamlValidationCrudTestCase(unittest.TestCase):
    def test_allow_missing_access_level_categories_in_cfg(self):
        """
        test_allow_missing_access_level_categories_in_cfg: write-policy when the YAML file is missing access level categories. It should write a policy regardless.
        """

        crud_file_input = {
            "mode": "crud",
            "name": "RoleNameWithCRUD",
            "read": ["arn:aws:ssm:us-east-1:123456789012:parameter/test",],
            "write": ["arn:aws:ssm:us-east-1:123456789012:parameter/test",],
            "list": ["arn:aws:ssm:us-east-1:123456789012:parameter/test",],
        }
        self.maxDiff = None

        result = write_policy_with_template(db_session, crud_file_input)
        print(json.dumps(result, indent=4))

    def test_empty_strings_in_access_level_categories(self):
        """
        test_empty_strings_in_access_level_categories: If the content of a list is an empty string, it should NOT sysexit
        :return:
        """
        crud_file_input = {
            "mode": "crud",
            "name": "RoleNameWithCRUD",
            "read": ["arn:aws:ssm:us-east-1:123456789012:parameter/test",],
            "write": ["arn:aws:ssm:us-east-1:123456789012:parameter/test",],
            "list": ["arn:aws:ssm:us-east-1:123456789012:parameter/test",],
            "tagging": [""],
            "permissions-management": [""],
        }
        desired_output = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "SsmReadParameter",
                    "Effect": "Allow",
                    "Action": [
                        "ssm:GetParameter",
                        "ssm:GetParameterHistory",
                        "ssm:GetParameters",
                        "ssm:GetParametersByPath",
                        "ssm:ListTagsForResource"
                    ],
                    "Resource": [
                        "arn:aws:ssm:us-east-1:123456789012:parameter/test"
                    ]
                },
                {
                    "Sid": "SsmWriteParameter",
                    "Effect": "Allow",
                    "Action": [
                        "ssm:DeleteParameter",
                        "ssm:DeleteParameters",
                        "ssm:LabelParameterVersion",
                        "ssm:PutParameter"
                    ],
                    "Resource": [
                        "arn:aws:ssm:us-east-1:123456789012:parameter/test"
                    ]
                }
            ]
        }
        # with self.assertRaises(Exception):
        result = write_policy_with_template(db_session, crud_file_input)
        self.assertDictEqual(desired_output, result)


class YamlValidationActionsTestCase(unittest.TestCase):
    def test_actions_missing_actions(self):
        """
        test_actions_missing_actions: write-policy actions if the actions block is missing
        :return:
        """
        cfg_with_missing_actions = {
            "mode": "actions",
            "name": "RoleNameWithActions",
        }
        with self.assertRaises(Exception):
            policy = write_policy_with_template(db_session, cfg_with_missing_actions)
