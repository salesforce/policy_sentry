import unittest
import json
from policy_sentry.shared.database import connect_db
from policy_sentry.writing.sid_group import SidGroup
from policy_sentry.querying.actions import get_action_data
from policy_sentry.shared.constants import DATABASE_FILE_PATH

db_session = connect_db(DATABASE_FILE_PATH)


class SidGroupActionsTestCase(unittest.TestCase):
    def test_actions_test_case(self):
        cfg = {
            "mode": "actions",
            "name": "RoleNameWithCRUD",
            "description": "Why I need these privs",
            "role_arn": "arn:aws:iam::123456789012:role/RiskyEC2",
            "actions": [
                "kms:CreateGrant",
                "kms:CreateCustomKeyStore",
                "ec2:AuthorizeSecurityGroupEgress",
                "ec2:AuthorizeSecurityGroupIngress",
            ],
        }
        sid_group = SidGroup()
        output = sid_group.process_template(db_session, cfg)
        print(json.dumps(output, indent=4))
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
                    "Sid": "Ec2WriteSecuritygroup",
                    "Effect": "Allow",
                    "Action": [
                        "ec2:AuthorizeSecurityGroupEgress",
                        "ec2:AuthorizeSecurityGroupIngress",
                    ],
                    "Resource": [
                        "arn:${Partition}:ec2:${Region}:${Account}:security-group/${SecurityGroupId}"
                    ],
                },
                {
                    "Sid": "MultMultNone",
                    "Effect": "Allow",
                    "Action": ["cloudhsm:DescribeClusters", "kms:CreateCustomKeyStore"],
                    "Resource": ["*"],
                },
            ],
        }
        self.maxDiff = None
        print(output)
        self.assertDictEqual(output, desired_output)


class SidGroupCrudTestCase(unittest.TestCase):
    def test_sid_group_multiple(self):
        sid_group = SidGroup()
        arn_list_from_user = [
            "arn:aws:s3:::example-org-s3-access-logs",
            "arn:aws:kms:us-east-1:123456789012:key/123456",
        ]
        access_level = "Permissions management"
        sid_group.add_by_arn_and_access_level(
            db_session, arn_list_from_user, access_level
        )
        output = sid_group.get_sid_group()
        print(json.dumps(output, indent=4))
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
        rendered_policy = sid_group.get_rendered_policy(db_session)
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
            db_session, arn_list_from_user, access_level
        )
        status = sid_group.get_sid_group()
        self.maxDiff = None
        # print(json.dumps(status, indent=4))
        self.assertEqual(status, desired_output)
        rendered_policy = sid_group.get_rendered_policy(db_session)
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
    #     data = get_action_data(db_session, "s3", "*")
    #     # print(data)

    def test_refactored_crud_policy(self):
        """test_refactored_crud_policy"""
        sid_group = SidGroup()
        sid_group.add_by_arn_and_access_level(
            db_session,
            ["arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"],
            "Read",
        )
        sid_group.add_by_arn_and_access_level(
            db_session, ["arn:aws:s3:::example-org-sbx-vmimport/stuff"], "Tagging"
        )
        sid_group.add_by_arn_and_access_level(
            db_session,
            ["arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"],
            "Write",
        )
        sid_group.add_by_arn_and_access_level(
            db_session,
            ["arn:aws:secretsmanager:us-east-1:123456789012:secret:anothersecret"],
            "Write",
        )
        sid_group.add_by_arn_and_access_level(
            db_session,
            ["arn:aws:kms:us-east-1:123456789012:key/123456"],
            "Permissions management",
        )
        sid_group.add_by_arn_and_access_level(
            db_session, ["arn:aws:ssm:us-east-1:123456789012:parameter/test"], "List"
        )

        output = sid_group.get_rendered_policy(db_session)
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
                        "secretsmanager:ListSecretVersionIds",
                    ],
                    "Resource": [
                        "arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"
                    ],
                },
                {
                    "Sid": "S3TaggingObject",
                    "Effect": "Allow",
                    "Action": [
                        "s3:DeleteObjectTagging",
                        "s3:DeleteObjectVersionTagging",
                        "s3:PutObjectTagging",
                        "s3:PutObjectVersionTagging",
                        "s3:ReplicateTags",
                    ],
                    "Resource": ["arn:aws:s3:::example-org-sbx-vmimport/stuff"],
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
                        "secretsmanager:UpdateSecretVersionStage",
                    ],
                    "Resource": [
                        "arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret",
                        "arn:aws:secretsmanager:us-east-1:123456789012:secret:anothersecret",
                    ],
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
        print(json.dumps(output, indent=4))
        self.maxDiff = None
        self.assertEqual(output, desired_output)

    def test_write_with_template(self):
        cfg = {
            "mode": "crud",
            "name": "RoleNameWithCRUD",
            "description": "Why I need these privs",
            "role_arn": "arn:aws:iam::123456789012:role/RiskyEC2",
            "permissions-management": ["arn:aws:s3:::example-org-s3-access-logs"],
            "list": [
                "arn:aws:secretsmanager:us-east-1:123456789012:secret:anothersecret"
            ],
        }
        sid_group = SidGroup()
        rendered_policy = sid_group.process_template(db_session, cfg)
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
        sid_group.add_by_list_of_actions(db_session, actions_test_data_1)
        output = sid_group.get_rendered_policy(db_session)
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
        print(json.dumps(output, indent=4))
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
            db_session, ["arn:aws:iam::000000000000:access-report/somepath"], "Read"
        )
        output = sid_group.get_rendered_policy(db_session)
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
        print(json.dumps(output, indent=4))
        self.assertDictEqual(output, desired_output)

    def test_add_by_list_of_actions(self):
        actions_test_data_1 = ["kms:CreateCustomKeyStore", "kms:CreateGrant"]
        sid_group = SidGroup()
        sid_group.add_by_list_of_actions(db_session, actions_test_data_1)
        output = sid_group.get_rendered_policy(db_session)
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
        print(json.dumps(output, indent=4))
        self.maxDiff = None
        self.assertDictEqual(output, desired_output)

    def test_add_crud_with_wildcard(self):
        cfg = {
            "mode": "crud",
            "name": "RoleNameWithCRUD",
            "description": "Why I need these privs",
            "role_arn": "arn:aws:iam::123456789012:role/RiskyEC2",
            "permissions-management": ["arn:aws:s3:::example-org-s3-access-logs"],
            "wildcard": [
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
        sid_group = SidGroup()
        output = sid_group.process_template(db_session, cfg)
        desired_output = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "MultMultNone",
                    "Effect": "Allow",
                    "Action": [
                        "ram:EnableSharingWithAwsOrganization",
                        "ram:GetResourcePolicies",
                        "secretsmanager:CreateSecret",
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
        print("Yolo")
        print(json.dumps(output, indent=4))
        self.assertDictEqual(output, desired_output)
