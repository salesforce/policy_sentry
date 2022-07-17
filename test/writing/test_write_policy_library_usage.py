import unittest
import json
import os
from policy_sentry.command.write_policy import write_policy_with_template
from policy_sentry.writing.sid_group import SidGroup
from policy_sentry.writing.template import (
    get_crud_template_dict,
    get_actions_template_dict,
)
from policy_sentry.util.arns import ARN

desired_crud_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "MultMultNone",
            "Effect": "Allow",
            "Action": [
                "cloudhsm:DescribeClusters",
                "kms:CreateCustomKeyStore"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Sid": "SecretsmanagerReadSecret",
            "Effect": "Allow",
            "Action": [
                "secretsmanager:DescribeSecret",
                "secretsmanager:GetResourcePolicy",
                "secretsmanager:GetSecretValue",
                "secretsmanager:ListSecretVersionIds"
            ],
            "Resource": [
                "arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"
            ]
        },
        {
            "Sid": "SecretsmanagerWriteSecret",
            "Effect": "Allow",
            "Action": [
                "secretsmanager:CancelRotateSecret",
                "secretsmanager:CreateSecret",
                "secretsmanager:DeleteSecret",
                "secretsmanager:PutSecretValue",
                "secretsmanager:RestoreSecret",
                "secretsmanager:RotateSecret",
                "secretsmanager:UpdateSecret",
                "secretsmanager:UpdateSecretVersionStage"
            ],
            "Resource": [
                "arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"
            ]
        },
        {
            "Sid": "S3ListObject",
            "Effect": "Allow",
            "Action": [
                "s3:ListMultipartUploadParts"
            ],
            "Resource": [
                "arn:aws:s3:::example-org-sbx-vmimport/stuff"
            ]
        },
        {
            "Sid": "SsmTaggingParameter",
            "Effect": "Allow",
            "Action": [
                "ssm:AddTagsToResource",
                "ssm:RemoveTagsFromResource"
            ],
            "Resource": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/test"
            ]
        },
        {
            "Sid": "KmsPermissionsmanagementKey",
            "Effect": "Allow",
            "Action": [
                "kms:CreateGrant",
                "kms:PutKeyPolicy",
                "kms:RetireGrant",
                "kms:RevokeGrant"
            ],
            "Resource": [
                "arn:aws:kms:us-east-1:123456789012:key/123456"
            ]
        },
        {
            "Sid": "AssumeRole",
            "Effect": "Allow",
            "Action": [
                "sts:AssumeRole"
            ],
            "Resource": [
                "arn:aws:iam::123456789012:role/demo"
            ]
        }
    ]
}

desired_actions_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "KmsPermissionsmanagementKey",
            "Effect": "Allow",
            "Action": [
                "kms:CreateGrant"
            ],
            "Resource": [
                "arn:${Partition}:kms:${Region}:${Account}:key/${KeyId}"
            ]
        },
        {
            "Sid": "MultMultNone",
            "Effect": "Allow",
            "Action": [
                "cloudhsm:DescribeClusters",
                "kms:CreateCustomKeyStore"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Sid": "Ec2WriteSecuritygroup",
            "Effect": "Allow",
            "Action": [
                "ec2:AuthorizeSecurityGroupEgress",
                "ec2:AuthorizeSecurityGroupIngress"
            ],
            "Resource": [
                "arn:${Partition}:ec2:${Region}:${Account}:security-group/${SecurityGroupId}"
            ]
        }
    ]
}


class WritePolicyWithLibraryOnly(unittest.TestCase):
    def test_write_actions_policy_with_library_only(self):
        """test_write_actions_policy_with_library_only: Write an actions mode policy without using the command line at all (library only)"""
        actions_template = get_actions_template_dict()
        # print(actions_template)
        actions_to_add = [
            "kms:CreateGrant",
            "kms:CreateCustomKeyStore",
            "ec2:AuthorizeSecurityGroupEgress",
            "ec2:AuthorizeSecurityGroupIngress",
        ]
        actions_template["mode"] = "actions"
        actions_template["actions"].extend(actions_to_add)
        # Modify it
        sid_group = SidGroup()
        minimize = None
        policy = sid_group.process_template(
            actions_template, minimize=minimize
        )
        self.maxDiff = None
        print(json.dumps(policy, indent=4))
        expected_statement_ids = [
            "KmsPermissionsmanagementKey",
            "MultMultNone",
            "Ec2WriteSecuritygroup",
            "Ec2WriteSecuritygrouprule"
        ]
        # self.assertDictEqual(policy, desired_actions_policy)
        for statement in policy.get("Statement"):
            self.assertTrue(statement.get("Sid") in expected_statement_ids)

    def test_write_crud_policy_with_library_only(self):
        """test_write_crud_policy_with_library_only: Write a policy in CRUD mode without using the command line at all (library only)"""
        another_crud_template = get_crud_template_dict()
        wildcard_actions_to_add = [
            "kms:CreateCustomKeyStore",
            # "cloudhsm:describeclusters",
        ]
        another_crud_template["mode"] = "crud"
        another_crud_template["read"].append(
            "arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"
        )
        another_crud_template["write"].append(
            "arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"
        )
        another_crud_template["list"].append("arn:aws:s3:::example-org-sbx-vmimport/stuff")
        another_crud_template["permissions-management"].append(
            "arn:aws:kms:us-east-1:123456789012:key/123456"
        )
        another_crud_template["tagging"].append(
            "arn:aws:ssm:us-east-1:123456789012:parameter/test"
        )
        another_crud_template["wildcard-only"]["single-actions"].extend(wildcard_actions_to_add)
        another_crud_template["sts"]["assume-role"].append("arn:aws:iam::123456789012:role/demo")
        # Modify it
        sid_group = SidGroup()
        # minimize = None
        result = sid_group.process_template(
            another_crud_template
        )
        expected_statement_ids = [
            "MultMultNone",
            "SecretsmanagerReadSecret",
            "SecretsmanagerWriteSecret",
            "S3ListObject",
            "SsmTaggingParameter",
            "KmsPermissionsmanagementKey",
            "AssumeRole"
        ]
        self.maxDiff = None
        print(json.dumps(result, indent=4))
        for statement in result.get("Statement"):
            self.assertTrue(statement.get("Sid") in expected_statement_ids)

    def test_gh_211_write_with_empty_access_level_lists(self):
        crud_template = get_crud_template_dict()
        crud_template['read'].append("arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret")
        crud_template['write'].append("arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret")
        # crud_template['list'].append("arn:aws:s3:::mybucket/stuff")
        # by commenting out the line below, you should not get an IndexError
        # crud_template['permissions-management'].append("arn:aws:kms:us-east-1:123456789012:key/123456")
        # crud_template['tagging'].append("arn:aws:ssm:us-east-1:123456789012:parameter/test")
        wildcard_actions_to_add = ["kms:createcustomkeystore", "cloudhsm:describeclusters"]
        crud_template['wildcard-only']['single-actions'].extend(wildcard_actions_to_add)
        result = write_policy_with_template(crud_template)
        # print(json.dumps(result, indent=4))
        expected_statement_ids = [
            "MultMultNone",
            "SecretsmanagerReadSecret",
            "SecretsmanagerWriteSecret",
        ]
        for statement in result.get("Statement"):
            self.assertTrue(statement.get("Sid") in expected_statement_ids)

    def test_gh_204_multiple_resource_types_wildcards(self):
        """test_gh_204_multiple_resource_types_wildcards: Address github issue #204 not having unit tests"""
        crud_template = {
            "mode": "crud",
            'read': ["arn:aws:rds:us-east-1:123456789012:*:*"],
            'write': ["arn:aws:rds:us-east-1:123456789012:*:*"],
            'list': ["arn:aws:rds:us-east-1:123456789012:*:*"]
        }

        # Let's only check the read level ones, or that will get exhausting.
        expected_statement_ids = [
            "RdsReadDb",
            "RdsReadEs",
            "RdsReadOg",
            "RdsReadPg",
            "RdsReadProxy",
            "RdsReadRi",
            "RdsReadSecgrp",
            "RdsReadSnapshot",
            "RdsReadSubgrp",
            "RdsReadTargetgroup",
            "MultMultNone",
        ]
        # In the real world, we would want to minimize, but that would just result in two different Sids:
        #   RdsMult
        #   MultMultNone
        # And in this test, we are trying to verify them individually to make sure they are not excluded.
        # So we will skip --minimize just for this test.
        policy = write_policy_with_template(crud_template)
        statement_ids = []
        for statement in policy.get("Statement"):
            statement_ids.append(statement.get("Sid"))
        for expected_sid in expected_statement_ids:
            self.assertTrue(expected_sid in statement_ids)

    def test_gh_237_ssm_arns_with_paths(self):
        """test_gh_237_ssm_arns_with_paths: Test GitHub issue #204 with resource ARN paths"""
        crud_template = {
            "mode": "crud",
            'read': ["arn:aws:ssm:::parameter/dev/foo/bar*"]
        }
        # result = write_policy_with_template(crud_template)
        # print(json.dumps(result, indent=4))
        arn = ARN("arn:aws:ssm:::parameter/dev/foo/bar*")
        self.assertTrue(arn.same_resource_type("arn:aws:ssm:::parameter/dev"))
