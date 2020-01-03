import unittest
import json
from policy_sentry.shared.database import connect_db
from policy_sentry.command.write_policy import write_policy_with_access_levels, write_policy_with_actions
from policy_sentry.shared.constants import DATABASE_FILE_PATH

db_session = connect_db(DATABASE_FILE_PATH)


valid_cfg_for_crud = {
    "policy_with_crud_levels": [
        {
            "name": "RoleNameWithCRUD",
            "description": "Why I need these privs",
            "arn": "arn:aws:iam::123456789012:role/RiskyEC2",
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
    "policy_with_actions": [
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
    #         "policy_with_actions": [
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
    #     with self.assertRaises(SystemExit):
    #         policy = write_policy_with_actions(cfg_multiple_roles_in_file, db_session)
    #
    #
    # def test_both_roles_in_file(self):
    #     """
    #     test_both_roles_in_file: write-policy when the YAML file contains both policy_with_crud_levels and policy_with_actions in the file (should only contain one)
    #     :return:
    #     """
    #     cfg_both_roles_in_file = {
    #         "policy_with_actions": [
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
    #         "policy_with_crud_levels": [
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
    #     with self.assertRaises(SystemExit):
    #         policy = write_policy_with_actions(cfg_both_roles_in_file, db_session)
    #

    # def test_missing_category_as_dict(self):
    #     """
    #     Test case: write-policy when the YAML file does not contain policy_with_crud_levels or
    #     policy_with_actions, and the input is as a dict instead of a list
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
        test_actions_missing_name: write-policy when the YAML file is missing a name
        :return:
        """
        cfg_with_missing_name = {
            "policy_with_actions": [
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
            "policy_with_actions": [
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
            "policy_with_actions": [
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

    def test_allow_missing_access_level_categories_in_cfg(self):
        """
        test_allow_missing_access_level_categories_in_cfg: write-policy --crud when the YAML file
        is missing access level categories
        It should write a policy regardless.
        :return:
        """

        crud_file_input = {
            "policy_with_crud_levels": [
                {
                    "name": "RoleNameWithCRUD",
                    "description": "Why I need these privs",
                    "arn": "arn:aws:iam::123456789012:role/RiskyEC2",
                    "read": [
                        "arn:aws:ssm:us-east-1:123456789012:parameter/test",
                    ],
                    "write": [
                        "arn:aws:ssm:us-east-1:123456789012:parameter/test",

                    ],
                    "list": [
                        "arn:aws:ssm:us-east-1:123456789012:parameter/test",
                    ],
                }
            ]
        }
        self.maxDiff = None

        result = write_policy_with_access_levels(crud_file_input, db_session)
        print(json.dumps(result, indent=4))

    def test_empty_strings_in_access_level_categories(self):
        """
        test_allow_empty_access_level_categories_in_cfg: If the content of a list is an empty string, it should sysexit
        :return:
        """
        crud_file_input = {
            "policy_with_crud_levels": [
                {
                    "name": "RoleNameWithCRUD",
                    "description": "Why I need these privs",
                    "arn": "arn:aws:iam::123456789012:role/RiskyEC2",
                    "read": [
                        "arn:aws:ssm:us-east-1:123456789012:parameter/test",
                    ],
                    "write": [
                        "arn:aws:ssm:us-east-1:123456789012:parameter/test",

                    ],
                    "list": [
                        "arn:aws:ssm:us-east-1:123456789012:parameter/test",
                    ],
                    "tag": [
                        ""
                    ],
                    "permissions-management": [
                        ""
                    ]
                }
            ]
        }
        with self.assertRaises(SystemExit):
            result = write_policy_with_access_levels(crud_file_input, db_session)
            print(json.dumps(result, indent=4))


class YamlValidationActionsTestCase(unittest.TestCase):

    def test_actions_missing_actions(self):
        """
        test_actions_missing_actions: write-policy actions if the actions block is missing
        :return:
        """
        cfg_with_missing_actions = {
            "policy_with_actions": [
                {
                    "name": "RoleNameWithActions",
                    "description": "Why I need these privs",
                    "arn": "arn:aws:iam::123456789102:role/RiskyEC2",
                }
            ]
        }
        with self.assertRaises(SystemExit):
            policy = write_policy_with_actions(cfg_with_missing_actions, db_session)

