import unittest
import json
from pathlib import Path
from policy_sentry.shared.database import connect_db
from policy_sentry.command.write_policy import write_policy_with_access_levels, write_policy_with_actions
from policy_sentry.shared.policy import ArnActionGroup

home = str(Path.home())
config_directory = '/.policy_sentry/'
database_file_name = 'aws.sqlite3'
database_path = home + config_directory + database_file_name
db_session = connect_db(database_path)


valid_cfg_for_crud = {
    "roles_with_crud_levels": [
        {
            "name": "RoleNameWithCRUD",
            "description": "Why I need these privs",
            "arn": "arn:aws:iam::559410426617:role/RiskyEC2",
            "read": [
                "arn:aws:s3:::example-org-sbx-vmimport",
                "arn:aws:s3:::example-kinnaird",
                "arn:aws:ssm:us-east-1:123456789012:parameter/test",
                "arn:aws:ssm:us-east-1:123456789012:parameter/test2",
                "arn:aws:kms:us-east-1:123456789012:key/123456",
                "arn:aws:s3:::job/jobid",
                "arn:aws:s3:::example-org-sbx-vmimport/stuff"
            ],
            "write": [
                "arn:aws:s3:::example-org-s3-access-logs",
                "arn:aws:s3:::example-org-sbx-vmimport/stuff",
                "arn:aws:secretsmanager:us-east-1:12345:secret:mysecret",
                "arn:aws:kms:us-east-1:123456789012:key/123456"
            ],
            "list": [
                "arn:aws:s3:::example-org-flow-logs",
                "arn:aws:s3:::example-org-sbx-vmimport/stuff"
            ],
            "tag": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/test"
            ],
            "permissions-management": [
                "arn:aws:s3:::example-org-s3-access-logs"
            ]
        }
    ]
}

valid_cfg_for_actions = {
    "roles_with_actions": [
        {
            "name": "RoleNameWithActions",
            "description": "Why I need these privs",
            "arn": "arn:aws:iam::123456789102:role/RiskyEC2",
            "actions": [
                "kms:CreateGrant",
                "kms:CreateCustomKeyStore",
                "ec2:AuthorizeSecurityGroupEgress",
                "ec2:AuthorizeSecurityGroupIngress"
            ]
        }
    ]
}


class YamlValidationOverallTestCase(unittest.TestCase):
    # def test_multiple_roles_in_file(self):
    #     """
    #     test_multiple_roles_in_file: write-policy when the YAML file includes multiple role blocks in the file (should only be 1)
    #     :return:
    #     """
    #     cfg_multiple_roles_in_file = {
    #         "roles_with_actions": [
    #             {
    #                 "name": "RoleNameWithActions",
    #                 "description": "Why I need these privs",
    #                 "arn": "arn:aws:iam::123456789102:role/RiskyEC2",
    #                 "actions": [
    #                     "kms:CreateGrant",
    #                     "kms:CreateCustomKeyStore",
    #                     "ec2:AuthorizeSecurityGroupEgress",
    #                     "ec2:AuthorizeSecurityGroupIngress"
    #                 ]
    #             },
    #             {
    #                 "name": "DuplicateRoleNameWithActions",
    #                 "description": "Why I need these privs",
    #                 "arn": "arn:aws:iam::123456789102:role/RiskyEC2",
    #                 "actions": [
    #                     "kms:CreateGrant",
    #                     "kms:CreateCustomKeyStore",
    #                     "ec2:AuthorizeSecurityGroupEgress",
    #                     "ec2:AuthorizeSecurityGroupIngress"
    #                 ]
    #             }
    #         ]
    #     }
    #     # TODO: Have some error handling to let the user know if there are multiple blocks
    #     with self.assertRaises(SystemExit):
    #         policy = write_policy_with_actions(cfg_multiple_roles_in_file, db_session)
    #
    #
    # def test_both_roles_in_file(self):
    #     """
    #     test_both_roles_in_file: write-policy when the YAML file contains both roles_with_crud_levels and roles_with_actions in the file (should only contain one)
    #     :return:
    #     """
    #     cfg_both_roles_in_file = {
    #         "roles_with_actions": [
    #             {
    #                 "name": "RoleNameWithActions",
    #                 "description": "Why I need these privs",
    #                 "arn": "arn:aws:iam::123456789102:role/RiskyEC2",
    #                 "actions": [
    #                     "kms:CreateGrant",
    #                     "kms:CreateCustomKeyStore",
    #                     "ec2:AuthorizeSecurityGroupEgress",
    #                     "ec2:AuthorizeSecurityGroupIngress"
    #                 ]
    #             },
    #         ],
    #         "roles_with_crud_levels": [
    #             {
    #                 "name": "DuplicateRoleNameWithActions",
    #                 "description": "Why I need these privs",
    #                 "arn": "arn:aws:iam::123456789102:role/RiskyEC2",
    #                 "actions": [
    #                     "kms:CreateGrant",
    #                     "kms:CreateCustomKeyStore",
    #                     "ec2:AuthorizeSecurityGroupEgress",
    #                     "ec2:AuthorizeSecurityGroupIngress"
    #                 ],
    #                 "read": [
    #                     "arn:aws:s3:::example-org-sbx-vmimport",
    #                     "arn:aws:s3:::example-kinnaird",
    #                     "arn:aws:ssm:us-east-1:123456789012:parameter/test",
    #                     "arn:aws:ssm:us-east-1:123456789012:parameter/test2",
    #                     "arn:aws:kms:us-east-1:123456789012:key/123456",
    #                     "arn:aws:s3:::job/jobid",
    #                     "arn:aws:s3:::example-org-sbx-vmimport/stuff"
    #                 ],
    #                 "write": [
    #                     "arn:aws:s3:::example-org-s3-access-logs",
    #                     "arn:aws:s3:::example-org-sbx-vmimport/stuff",
    #                     "arn:aws:secretsmanager:us-east-1:12345:secret:mysecret",
    #                     "arn:aws:kms:us-east-1:123456789012:key/123456"
    #                 ],
    #                 "list": [
    #                     "arn:aws:s3:::example-org-flow-logs",
    #                     "arn:aws:s3:::example-org-sbx-vmimport/stuff"
    #                 ],
    #                 "tag": [
    #                     "arn:aws:ssm:us-east-1:123456789012:parameter/test"
    #                 ],
    #                 "permissions-management": [
    #                     "arn:aws:s3:::example-org-s3-access-logs"
    #                 ]
    #             }
    #         ]
    #     }
    #     # TODO: Have some error handling to let the user know if there are multiple blocks
    #     with self.assertRaises(SystemExit):
    #         policy = write_policy_with_actions(cfg_both_roles_in_file, db_session)
    #

    # def test_missing_category_as_dict(self):
    #     """
    #     Test case: write-policy when the YAML file does not contain roles_with_crud_levels or roles_with_actions, and the input is as a dict instead of a list
    #     :return:
    #     """
    #     cfg_with_missing_category = {
    #         {
    #             "name": "RoleNameWithActions",
    #             "description": "Why I need these privs",
    #             "actions": [
    #                 "kms:CreateGrant",
    #                 "kms:CreateCustomKeyStore",
    #                 "ec2:AuthorizeSecurityGroupEgress",
    #                 "ec2:AuthorizeSecurityGroupIngress",
    #             ]
    #         }
    #     }
    #     with self.assertRaises(SystemExit):
    #         policy = write_policy_with_actions(cfg_with_missing_category, db_session)

    def test_actions_missing_name(self):
        """
        test_actions_missing_name: write-policy when the YAML file is missing a name?
        :return:
        """
        cfg_with_missing_name = {
            "roles_with_actions": [
                {
                    "description": "Why I need these privs",
                    "arn": "arn:aws:iam::123456789102:role/RiskyEC2",
                    "actions": [
                        "kms:CreateGrant",
                        "kms:CreateCustomKeyStore",
                        "ec2:AuthorizeSecurityGroupEgress",
                        "ec2:AuthorizeSecurityGroupIngress"
                    ]
                }
            ]
        }
        with self.assertRaises(SystemExit):
            policy = write_policy_with_actions(cfg_with_missing_name, db_session)


    def test_actions_missing_description(self):
        """
        test_actions_missing_description: write-policy when the YAML file is missing a description
        :return:
        """
        cfg_with_missing_description = {
            "roles_with_actions": [
                {
                    "name": "RoleNameWithActions",
                    "arn": "arn:aws:iam::123456789102:role/RiskyEC2",
                    "actions": [
                        "kms:CreateGrant",
                        "kms:CreateCustomKeyStore",
                        "ec2:AuthorizeSecurityGroupEgress",
                        "ec2:AuthorizeSecurityGroupIngress"
                    ]
                }
            ]
        }
        with self.assertRaises(SystemExit):
            policy = write_policy_with_actions(cfg_with_missing_description, db_session)


    def test_actions_missing_arn(self):
        """
        test_actions_missing_arn: write-policy actions command when YAML file block is missing an ARN
        :return:
        """
        cfg_with_missing_actions = {
            "roles_with_actions": [
                {
                    "name": "RoleNameWithActions",
                    "description": "Why I need these privs",
                    "actions": [
                        "kms:CreateGrant",
                        "kms:CreateCustomKeyStore",
                        "ec2:AuthorizeSecurityGroupEgress",
                        "ec2:AuthorizeSecurityGroupIngress"
                    ]
                }
            ]
        }
        with self.assertRaises(SystemExit):
            policy = write_policy_with_actions(cfg_with_missing_actions, db_session)


class YamlValidationCrudTestCase(unittest.TestCase):

    def test_missing_access_levels(self):
        """
        test_missing_access_levels: write-policy --crud command when YAML File is missing access levels
        :return:
        """
        cfg_with_missing_access_levels = {
            "roles_with_crud_levels": [
                {
                    "name": "RoleNameWithCRUD",
                    "description": "Why I need these privs",
                    "arn": "arn:aws:iam::559410426617:role/RiskyEC2",
                    "list": [
                        "arn:aws:s3:::example-org-flow-logs",
                        "arn:aws:s3:::example-org-sbx-vmimport/stuff"
                    ],
                    "tag": [
                        "arn:aws:ssm:us-east-1:123456789012:parameter/test"
                    ],
                    "permissions-management": [
                        "arn:aws:s3:::example-org-s3-access-logs"
                    ]
                }
            ]
        }

        with self.assertRaises(SystemExit):
            arn_action_group = ArnActionGroup()
            arn_dict = arn_action_group.process_resource_specific_acls(cfg_with_missing_access_levels, db_session)


class YamlValidationActionsTestCase(unittest.TestCase):

    def test_actions_missing_actions(self):
        """
        test_actions_missing_actions: write-policy actions if the actions block is missing
        :return:
        """
        cfg_with_missing_actions = {
            "roles_with_actions": [
                {
                    "name": "RoleNameWithActions",
                    "description": "Why I need these privs",
                    "arn": "arn:aws:iam::123456789102:role/RiskyEC2",
                }
            ]
        }
        with self.assertRaises(SystemExit):
            policy = write_policy_with_actions(cfg_with_missing_actions, db_session)

