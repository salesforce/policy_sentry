import unittest
import json

from policy_sentry.command.write_policy import write_policy
from policy_sentry.writing.sid_group import SidGroup
from policy_sentry.writing.template import (
    get_crud_template_dict,
    get_actions_template_dict,
)

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
            "Sid": "SsmTaggingParameter",
            "Effect": "Allow",
            "Action": [
                "ssm:AddTagsToResource",
                "ssm:RemoveTagsFromResource"
            ],
            "Resource": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/test"
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
        self.assertDictEqual(policy, desired_actions_policy)

    def test_write_crud_policy_with_library_only(self):
        """test_write_crud_policy_with_library_only: Write a policy in CRUD mode without using the command line at all (library only)"""
        crud_template = get_crud_template_dict()
        wildcard_actions_to_add = [
            "kms:CreateCustomKeyStore",
            # "cloudhsm:describeclusters",
        ]
        crud_template["mode"] = "crud"
        crud_template["read"].append(
            "arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"
        )
        crud_template["write"].append(
            "arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"
        )
        crud_template["list"].append("arn:aws:s3:::example-org-sbx-vmimport/stuff")
        crud_template["permissions-management"].append(
            "arn:aws:kms:us-east-1:123456789012:key/123456"
        )
        crud_template["tagging"].append(
            "arn:aws:ssm:us-east-1:123456789012:parameter/test"
        )
        crud_template["wildcard-only"]["single-actions"].extend(wildcard_actions_to_add)
        # Modify it
        sid_group = SidGroup()
        minimize = None
        policy = sid_group.process_template(
            crud_template, minimize=minimize
        )
        # print("desired_crud_policy")
        # print(json.dumps(desired_crud_policy, indent=4))
        # print("policy")
        print(json.dumps(policy, indent=4))
        self.maxDiff = None
        self.assertDictEqual(desired_crud_policy, policy)
