import unittest
from policy_sentry.writing.validate import check_actions_schema, check_crud_schema

valid_cfg_for_crud = {
    "mode": "crud",
    "name": "RoleNameWithCRUD",
    "read": ["arn:aws:s3:::example-org-sbx-vmimport",],
    "write": ["arn:aws:s3:::example-org-s3-access-logs",],
    "list": [
        "arn:aws:s3:::example-org-flow-logs",
        "arn:aws:s3:::example-org-sbx-vmimport/stuff",
    ],
    "tagging": ["arn:aws:ssm:us-east-1:123456789012:parameter/test"],
    "permissions-management": ["arn:aws:s3:::example-org-s3-access-logs"],
    "wildcard-only": {
        "service-read": ["s3"]
    },
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

valid_crud_with_one_item_only = {
    "mode": "crud",
    "name": "RoleNameWithCRUD",
    "read": ["arn:aws:s3:::example-org-sbx-vmimport",],
}

invalid_crud_with_mispelled_category = {
    "mode": "crud",
    "name": "RoleNameWithCRUD",
    "reed": ["arn:aws:s3:::example-org-sbx-vmimport",],
    "right": ["arn:aws:s3:::example-org-sbx-vmimport",],
    "wrist": ["arn:aws:s3:::example-org-sbx-vmimport",],
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
