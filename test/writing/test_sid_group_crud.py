import unittest
import json
import os
import yaml
from policy_sentry.writing.sid_group import SidGroup


crud_with_override_template = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        os.path.pardir,
        os.path.pardir,
        "examples",
        "yml",
        "crud-with-override.yml",
    )
)

with open(crud_with_override_template, "r") as yaml_file:
    crud_with_override_template_cfg = yaml.safe_load(yaml_file)


class SidGroupCrudTestCase(unittest.TestCase):
    def test_sid_group_multiple(self):
        sid_group = SidGroup()
        arn_list_from_user = [
            "arn:aws:s3:::example-org-s3-access-logs",
            "arn:aws:kms:us-east-1:123456789012:key/123456",
        ]
        access_level = "Permissions management"
        sid_group.add_by_arn_and_access_level(
            arn_list_from_user, access_level
        )
        output = sid_group.get_sid_group()
        # print(json.dumps(output, indent=4))
        desired_output = {
            "S3PermissionsmanagementBucket": {
                "arn": ["arn:aws:s3:::example-org-s3-access-logs"],
                "service": "s3",
                "access_level": "Permissions management",
                "arn_format": "arn:${Partition}:s3:::${BucketName}",
                "actions": [
                    "s3:DeleteBucketPolicy",
                    "s3:PutBucketAcl",
                    "s3:PutBucketPolicy",
                    "s3:PutBucketPublicAccessBlock",
                ],
                "conditions": [],
            },
            "KmsPermissionsmanagementKey": {
                "arn": ["arn:aws:kms:us-east-1:123456789012:key/123456"],
                "service": "kms",
                "access_level": "Permissions management",
                "arn_format": "arn:${Partition}:kms:${Region}:${Account}:key/${KeyId}",
                "actions": [
                    "kms:CreateGrant",
                    "kms:PutKeyPolicy",
                    "kms:RetireGrant",
                    "kms:RevokeGrant",
                ],
                "conditions": [],
            },
        }
        self.maxDiff = None
        self.assertDictEqual(desired_output, output)
        desired_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "S3PermissionsmanagementBucket",
                    "Effect": "Allow",
                    "Action": [
                        "s3:DeleteBucketPolicy",
                        "s3:PutBucketAcl",
                        "s3:PutBucketPolicy",
                        "s3:PutBucketPublicAccessBlock",
                    ],
                    "Resource": ["arn:aws:s3:::example-org-s3-access-logs"],
                },
                {
                    "Sid": "KmsPermissionsmanagementKey",
                    "Effect": "Allow",
                    "Action": [
                        "kms:CreateGrant",
                        "kms:PutKeyPolicy",
                        "kms:RetireGrant",
                        "kms:RevokeGrant",
                    ],
                    "Resource": ["arn:aws:kms:us-east-1:123456789012:key/123456"],
                },
            ],
        }
        rendered_policy = sid_group.get_rendered_policy()
        self.assertDictEqual(desired_policy, rendered_policy)
        # print(json.dumps(rendered_policy, indent=4))

    def test_sid_group(self):
        desired_output = {
            "S3PermissionsmanagementBucket": {
                "arn": ["arn:aws:s3:::example-org-s3-access-logs"],
                "service": "s3",
                "access_level": "Permissions management",
                "arn_format": "arn:${Partition}:s3:::${BucketName}",
                "actions": [
                    "s3:DeleteBucketPolicy",
                    "s3:PutBucketAcl",
                    "s3:PutBucketPolicy",
                    "s3:PutBucketPublicAccessBlock",
                ],
                "conditions": [],
            }
        }
        sid_group = SidGroup()
        arn_list_from_user = ["arn:aws:s3:::example-org-s3-access-logs"]
        access_level = "Permissions management"
        sid_group.add_by_arn_and_access_level(
            arn_list_from_user, access_level
        )
        status = sid_group.get_sid_group()
        self.maxDiff = None
        # print(json.dumps(status, indent=4))
        self.assertEqual(status, desired_output)
        rendered_policy = sid_group.get_rendered_policy()
        desired_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "S3PermissionsmanagementBucket",
                    "Effect": "Allow",
                    "Action": [
                        "s3:DeleteBucketPolicy",
                        "s3:PutBucketAcl",
                        "s3:PutBucketPolicy",
                        "s3:PutBucketPublicAccessBlock",
                    ],
                    "Resource": ["arn:aws:s3:::example-org-s3-access-logs"],
                }
            ],
        }
        # print(json.dumps(rendered_policy, indent=4))
        self.maxDiff = None
        self.assertDictEqual(desired_policy, rendered_policy)

    # def test_get_actions_data_service_wide(self):
    #     data = get_action_data("s3", "*")
    #     # print(data)

    def test_refactored_crud_policy(self):
        """test_refactored_crud_policy"""
        sid_group = SidGroup()
        sid_group.add_by_arn_and_access_level(
            ["arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"],
            "Read",
        )
        sid_group.add_by_arn_and_access_level(
            ["arn:aws:s3:::example-org-sbx-vmimport/stuff"], "Tagging"
        )
        sid_group.add_by_arn_and_access_level(
            ["arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"],
            "Write",
        )
        sid_group.add_by_arn_and_access_level(
            ["arn:aws:secretsmanager:us-east-1:123456789012:secret:anothersecret"],
            "Write",
        )
        sid_group.add_by_arn_and_access_level(
            ["arn:aws:kms:us-east-1:123456789012:key/123456"],
            "Permissions management",
        )
        sid_group.add_by_arn_and_access_level(
            ["arn:aws:ssm:us-east-1:123456789012:parameter/test"], "List"
        )

        output = sid_group.get_rendered_policy()
        desired_output = {
            "Version": "2012-10-17",
            "Statement": [
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
                    "Sid": "S3TaggingObject",
                    "Effect": "Allow",
                    "Action": [
                        "s3:DeleteObjectTagging",
                        "s3:DeleteObjectVersionTagging",
                        "s3:PutObjectTagging",
                        "s3:PutObjectVersionTagging",
                        "s3:ReplicateTags"
                    ],
                    "Resource": [
                        "arn:aws:s3:::example-org-sbx-vmimport/stuff"
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
                        "arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret",
                        "arn:aws:secretsmanager:us-east-1:123456789012:secret:anothersecret"
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
                    "Sid": "SsmListParameter",
                    "Effect": "Allow",
                    "Action": [
                        "ssm:ListTagsForResource"
                    ],
                    "Resource": [
                        "arn:aws:ssm:us-east-1:123456789012:parameter/test"
                    ]
                }
            ]
        }
        # print(json.dumps(output, indent=4))
        self.maxDiff = None
        self.assertEqual(output, desired_output)

    def test_write_with_template(self):
        cfg = {
            "mode": "crud",
            "name": "RoleNameWithCRUD",
            "permissions-management": ["arn:aws:s3:::example-org-s3-access-logs"],
            "list": [
                "arn:aws:secretsmanager:us-east-1:123456789012:secret:anothersecret"
            ],
        }
        sid_group = SidGroup()
        rendered_policy = sid_group.process_template(cfg)
        desired_output = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "S3PermissionsmanagementBucket",
                    "Effect": "Allow",
                    "Action": [
                        "s3:DeleteBucketPolicy",
                        "s3:PutBucketAcl",
                        "s3:PutBucketPolicy",
                        "s3:PutBucketPublicAccessBlock",
                    ],
                    "Resource": ["arn:aws:s3:::example-org-s3-access-logs"],
                }
            ],
        }
        # print(json.dumps(rendered_policy, indent=4))
        self.assertEqual(rendered_policy, desired_output)

    def test_resource_restriction_plus_dependent_action(self):
        """
        test_resource_restriction_plus_dependent_action
        """
        # Given iam:generateorganizationsaccessreport with resource constraint, make sure these are added:
        #  organizations:DescribePolicy,organizations:ListChildren,organizations:ListParents,
        #  organizations:ListPoliciesForTarget,organizations:ListRoots,organizations:ListTargetsForPolicy
        actions_test_data_1 = ["iam:generateorganizationsaccessreport"]
        sid_group = SidGroup()
        sid_group.add_by_list_of_actions(actions_test_data_1)
        output = sid_group.get_rendered_policy()
        # print(json.dumps(rendered_policy, indent=4))
        desired_output = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "organizations:DescribePolicy",
                        "organizations:ListChildren",
                        "organizations:ListParents",
                        "organizations:ListPoliciesForTarget",
                        "organizations:ListRoots",
                        "organizations:ListTargetsForPolicy",
                    ],
                    "Resource": ["*"],
                    "Sid": "MultMultNone",
                },
                {
                    "Sid": "IamReadAccessreport",
                    "Effect": "Allow",
                    "Action": ["iam:GenerateOrganizationsAccessReport"],
                    "Resource": [
                        "arn:${Partition}:iam::${Account}:access-report/${EntityPath}"
                    ],
                },
            ],
        }
        self.maxDiff = None
        # print(json.dumps(output, indent=4))
        self.assertDictEqual(output, desired_output)

    def test_resource_restriction_plus_dependent_action_simple_2(self):
        """
        test_resource_restriction_plus_dependent_action_simple_2
        """
        # Given iam:generateorganizationsaccessreport with resource constraint, make sure these are added:
        #  organizations:DescribePolicy,organizations:ListChildren,organizations:ListParents,
        #  organizations:ListPoliciesForTarget,organizations:ListRoots,organizations:ListTargetsForPolicy

        sid_group = SidGroup()
        sid_group.add_by_arn_and_access_level(
            ["arn:aws:iam::000000000000:access-report/somepath"], "Read"
        )
        output = sid_group.get_rendered_policy()
        desired_output = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "MultMultNone",
                    "Effect": "Allow",
                    "Action": [
                        "organizations:DescribePolicy",
                        "organizations:ListChildren",
                        "organizations:ListParents",
                        "organizations:ListPoliciesForTarget",
                        "organizations:ListRoots",
                        "organizations:ListTargetsForPolicy",
                    ],
                    "Resource": ["*"],
                },
                {
                    "Sid": "IamReadAccessreport",
                    "Effect": "Allow",
                    "Action": ["iam:GenerateOrganizationsAccessReport"],
                    "Resource": ["arn:aws:iam::000000000000:access-report/somepath"],
                },
            ],
        }
        # print(json.dumps(output, indent=4))
        self.assertDictEqual(output, desired_output)

    def test_add_by_list_of_actions(self):
        actions_test_data_1 = ["kms:CreateCustomKeyStore", "kms:CreateGrant"]
        sid_group = SidGroup()
        sid_group.add_by_list_of_actions(actions_test_data_1)
        output = sid_group.get_rendered_policy()
        desired_output = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "KmsPermissionsmanagementKey",
                    "Effect": "Allow",
                    "Action": ["kms:CreateGrant"],
                    "Resource": [
                        "arn:${Partition}:kms:${Region}:${Account}:key/${KeyId}"
                    ],
                },
                {
                    "Sid": "MultMultNone",
                    "Effect": "Allow",
                    "Action": [
                        "cloudhsm:DescribeClusters",
                        "kms:CreateCustomKeyStore",
                    ],
                    "Resource": ["*"],
                },
            ],
        }
        # print(json.dumps(output, indent=4))
        self.maxDiff = None
        self.assertDictEqual(output, desired_output)

    def test_add_crud_with_wildcard(self):
        cfg = {
            "mode": "crud",
            "name": "RoleNameWithCRUD",
            "permissions-management": ["arn:aws:s3:::example-org-s3-access-logs"],
            "wildcard-only": {
                "single-actions": [
                    # The first three are legitimately wildcard only.
                    # Verify with `policy_sentry query action-table --service secretsmanager --wildcard-only`
                    "ram:enablesharingwithawsorganization",
                    "ram:getresourcepolicies",
                    "secretsmanager:createsecret",
                    # This last one can be "secret" ARN type OR wildcard. We want to prevent people from
                    # bypassing this mechanism, while allowing them to explicitly
                    # request specific privs that require wildcard mode. This next value -
                    # secretsmanager:putsecretvalue - is an example of someone trying to beat the tool.
                    "secretsmanager:putsecretvalue",
                ],
            }
        }
        sid_group = SidGroup()
        output = sid_group.process_template(cfg)
        desired_output = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "MultMultNone",
                    "Effect": "Allow",
                    "Action": [
                        "ram:EnableSharingWithAwsOrganization",
                        "ram:GetResourcePolicies",
                    ],
                    "Resource": ["*"],
                },
                {
                    "Sid": "S3PermissionsmanagementBucket",
                    "Effect": "Allow",
                    "Action": [
                        "s3:DeleteBucketPolicy",
                        "s3:PutBucketAcl",
                        "s3:PutBucketPolicy",
                        "s3:PutBucketPublicAccessBlock",
                    ],
                    "Resource": ["arn:aws:s3:::example-org-s3-access-logs"],
                },
            ],
        }
        self.maxDiff = None
        # print(json.dumps(output, indent=4))
        self.assertDictEqual(output, desired_output)

    def test_sid_group_override(self):
        sid_group = SidGroup()
        output = sid_group.process_template(crud_with_override_template_cfg)
        self.maxDiff = None
        desired_output = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "MultMultNone",
                    "Effect": "Allow",
                    "Action": [
                        "ram:GetResourcePolicies"
                    ],
                    "Resource": [
                        "*"
                    ]
                },
                {
                    "Sid": "S3PermissionsmanagementBucket",
                    "Effect": "Allow",
                    "Action": [
                        "s3:DeleteBucketPolicy",
                        "s3:PutBucketAcl",
                        "s3:PutBucketPolicy",
                        "s3:PutBucketPublicAccessBlock"
                    ],
                    "Resource": [
                        "arn:aws:s3:::example-org-s3-access-logs"
                    ]
                },
                {
                    "Sid": "SkipResourceConstraints",
                    "Effect": "Allow",
                    "Action": [
                        "ssm:GetParameter",
                        "ssm:GetParameters",
                        "ssm:GetParametersByPath"
                    ],
                    "Resource": [
                        "*"
                    ]
                }
            ]
        }
        # print(json.dumps(output, indent=4))
        self.assertDictEqual(output, desired_output)

    def test_exclude_actions_from_crud_output(self):
        sid_group = SidGroup()
        crud_with_exclude_actions = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.path.pardir,
                os.path.pardir,
                "examples",
                "yml",
                "crud-with-exclude-actions.yml",
            )
        )

        with open(crud_with_exclude_actions, "r") as this_yaml_file:
            crud_with_exclude_actions_cfg = yaml.safe_load(this_yaml_file)
        # crud_with_exclude_actions_cfg = {
        #     "mode": "crud",
        #     "write": [
        #         "arn:aws:kms:us-east-1:123456789012:key/aaaa-bbbb-cccc"
        #     ],
        #     "exclude-actions": [
        #         "kms:Delete*"
        #     ]
        # }

        # print(json.dumps(crud_with_exclude_actions_cfg, indent=4))
        sid_group.process_template(crud_with_exclude_actions_cfg)
        result = sid_group.get_rendered_policy(crud_with_exclude_actions_cfg)
        # print(json.dumps(result, indent=4))
        expected_result = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "KmsWriteKey",
                    "Effect": "Allow",
                    "Action": [
                        "kms:CancelKeyDeletion",
                        "kms:CreateAlias",
                        "kms:Decrypt",
                        "kms:EnableKey",
                        "kms:EnableKeyRotation",
                        "kms:Encrypt",
                        "kms:GenerateDataKey",
                        "kms:GenerateDataKeyPair",
                        "kms:GenerateDataKeyPairWithoutPlaintext",
                        "kms:GenerateDataKeyWithoutPlaintext",
                        "kms:ImportKeyMaterial",
                        "kms:ReEncryptFrom",
                        "kms:ReEncryptTo",
                        "kms:Sign",
                        "kms:UpdateAlias",
                        "kms:UpdateKeyDescription",
                        "kms:Verify"
                    ],
                    "Resource": [
                        "arn:aws:kms:us-east-1:123456789012:key/aaaa-bbbb-cccc"
                    ]
                }
            ]
        }
        self.assertDictEqual(result, expected_result)

        crud_with_exclude_actions_cfg = {
            "mode": "crud",
            "write": [
                "arn:aws:kms:us-east-1:123456789012:key/aaaa-bbbb-cccc"
            ],
            # This is really only because KMS is a special case.
            "exclude-actions": [
                "kms:Delete*",
                "kms:Disable*",
                "kms:Enable*",
                "kms:Generate*",
                "kms:Cancel*",
                "kms:Create*",
                "kms:Import*",
                "kms:ReEncrypt*",
                "kms:Sign*",
                "kms:Schedule*",
                "kms:Update*",
                "kms:Verify*"
            ]
        }
        sid_group.process_template(crud_with_exclude_actions_cfg)
        results = sid_group.get_rendered_policy()
        # print(json.dumps(results, indent=4))
        expected_result = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "KmsWriteKey",
                    "Effect": "Allow",
                    "Action": [
                        "kms:Decrypt",
                        "kms:Encrypt"
                    ],
                    "Resource": [
                        "arn:aws:kms:us-east-1:123456789012:key/aaaa-bbbb-cccc"
                    ]
                }
            ]
        }
        self.assertDictEqual(results, expected_result)
