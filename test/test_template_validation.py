import unittest
from policy_sentry.writing.validate import check_actions_schema, check_crud_schema

valid_cfg_for_crud = {
    "policy_with_crud_levels": [
        {
            "name": "RoleNameWithCRUD",
            "description": "Why I need these privs",
            "role_arn": "arn:aws:iam::123456789012:role/MyRole",
            "read": [
                "arn:aws:s3:::example-org-sbx-vmimport",
            ],
            "write": [
                "arn:aws:s3:::example-org-s3-access-logs",
            ],
            "list": [
                "arn:aws:s3:::example-org-flow-logs",
                "arn:aws:s3:::example-org-sbx-vmimport/stuff"
            ],
            "tagging": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/test"
            ],
            "permissions-management": [
                "arn:aws:s3:::example-org-s3-access-logs"
            ],
            "wildcard": [
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
            "role_arn": "arn:aws:iam::123456789102:role/MyRole",
            "actions": [
                "kms:CreateGrant",
                "kms:CreateCustomKeyStore",
                "ec2:AuthorizeSecurityGroupEgress",
                "ec2:AuthorizeSecurityGroupIngress"
            ]
        }
    ]
}

valid_crud_with_one_item_only = {
    "policy_with_crud_levels": [
        {
            "name": "RoleNameWithCRUD",
            "description": "Why I need these privs",
            "role_arn": "arn:aws:iam::123456789012:role/MyRole",
            "read": [
                "arn:aws:s3:::example-org-sbx-vmimport",
            ],
        }
    ]
}

invalid_crud_with_mispelled_category = {
    "policy_with_crud_levels": [
        {
            "name": "RoleNameWithCRUD",
            "description": "Why I need these privs",
            "role_arn": "arn:aws:iam::123456789012:role/MyRole",
            "reed": [
                "arn:aws:s3:::example-org-sbx-vmimport",
            ],
            "right": [
                "arn:aws:s3:::example-org-sbx-vmimport",
            ],
            "wrist": [
                "arn:aws:s3:::example-org-sbx-vmimport",
            ],
        }
    ]
}


class YMLSchemaTestCase(unittest.TestCase):
    def test_actions_schema(self):
        """test_actions_schema: Validates that the user-supplied YAML is working for CRUD mode"""
        result = check_actions_schema(valid_cfg_for_actions)
        self.assertTrue(result)

    def test_crud_schema(self):
        """test_actions_schema: Validates that the user-supplied YAML is working for CRUD mode"""
        result = check_crud_schema(valid_cfg_for_crud)
        self.assertTrue(result)
        self.assertTrue(check_crud_schema(valid_crud_with_one_item_only))
        with self.assertRaises(Exception):
            check_crud_schema(invalid_crud_with_mispelled_category)

