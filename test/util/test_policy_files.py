import os
import unittest
import json
from policy_sentry.util.policy_files import (
    get_actions_from_json_policy_file,
    get_actions_from_policy,
    get_statement_from_policy_using_sid,
    get_sid_names_from_policy,
)


class PolicyFilesTestCase(unittest.TestCase):
    def test_get_actions_from_policy(self):
        """util.policy_files.get_actions_from_policy"""
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "ecr:getauthorizationtoken",
                        "ecr:batchchecklayeravailability",
                        "ecr:getdownloadurlforlayer",
                        "ecr:getrepositorypolicy",
                        "ecr:describerepositories",
                        "ecr:listimages",
                        "ecr:describeimages",
                        "ecr:batchgetimage",
                        "ecr:initiatelayerupload",
                        "ecr:uploadlayerpart",
                        "ecr:completelayerupload",
                        "ecr:putimage",
                    ],
                    "Resource": "*",
                },
                {
                    "Sid": "AllowManageOwnAccessKeys",
                    "Effect": "Allow",
                    "Action": [
                        "iam:CreateAccessKey",
                        "iam:DeleteAccessKey",
                        "iam:ListAccessKeys",
                        "iam:UpdateAccessKey",
                    ],
                    "Resource": "arn:aws:iam::*:user/${aws:username}",
                },
            ],
        }
        actions_list = get_actions_from_policy(policy)
        desired_actions_list = [
            "ecr:BatchCheckLayerAvailability",
            "ecr:BatchGetImage",
            "ecr:CompleteLayerUpload",
            "ecr:DescribeImages",
            "ecr:DescribeRepositories",
            "ecr:GetAuthorizationToken",
            "ecr:GetDownloadUrlForLayer",
            "ecr:GetRepositoryPolicy",
            "ecr:InitiateLayerUpload",
            "ecr:ListImages",
            "ecr:PutImage",
            "ecr:UploadLayerPart",
            "iam:CreateAccessKey",
            "iam:DeleteAccessKey",
            "iam:ListAccessKeys",
            "iam:UpdateAccessKey",
        ]
        self.maxDiff = None
        print(json.dumps(actions_list, indent=4))
        self.assertListEqual(desired_actions_list, actions_list)

    def test_get_actions_from_policy_file_with_explicit_actions(self):
        """util.policy_file.get_actions_from_policy_file_with_explicit_actions: Verify that we can get a list of actions from a
        file when it contains specific actions"""
        policy_file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.path.pardir,
                os.path.pardir,
                "examples",
                "analyze",
                "explicit-actions.json",
            )
        )
        requested_actions = get_actions_from_json_policy_file(policy_file_path)
        # print(requested_actions)
        self.maxDiff = None
        print(json.dumps(requested_actions, indent=4))
        desired_actions = [
            "ecr:BatchCheckLayerAvailability",
            "ecr:BatchGetImage",
            "ecr:CompleteLayerUpload",
            "ecr:DescribeImages",
            "ecr:DescribeRepositories",
            "ecr:GetAuthorizationToken",
            "ecr:GetDownloadUrlForLayer",
            "ecr:GetRepositoryPolicy",
            "ecr:InitiateLayerUpload",
            "ecr:ListImages",
            "ecr:PutImage",
            "ecr:UploadLayerPart",
            "iam:CreateAccessKey",
            "iam:DeleteAccessKey",
            "iam:ListAccessKeys",
            "iam:UpdateAccessKey",
        ]
        self.assertListEqual(requested_actions, desired_actions)

    def test_get_sid_names_from_policy(self):
        """util.policy_files.get_sid_names_from_policy"""
        policy_json = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "MultMultNone",
                    "Effect": "Allow",
                    "Action": [
                        "ram:EnableSharingWithAwsOrganization",
                        "ram:GetResourcePolicies",
                        "ecr:GetAuthorizationToken",
                        "s3:GetAccessPoint",
                        "s3:GetAccountPublicAccessBlock",
                        "s3:ListAccessPoints",
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
        expected_result = ["MultMultNone", "S3PermissionsmanagementBucket"]
        result = get_sid_names_from_policy(policy_json)
        self.assertListEqual(result, expected_result)

    def test_get_statement_from_policy_using_sid(self):
        """util.policy_files.get_statement_from_policy_using_sid"""
        policy_json = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "MultMultNone",
                    "Effect": "Allow",
                    "Action": [
                        "ram:EnableSharingWithAwsOrganization",
                        "ram:GetResourcePolicies",
                        "ecr:GetAuthorizationToken",
                        "s3:GetAccessPoint",
                        "s3:GetAccountPublicAccessBlock",
                        "s3:ListAccessPoints",
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

        expected_result = {
            "Sid": "MultMultNone",
            "Effect": "Allow",
            "Action": [
                "ram:EnableSharingWithAwsOrganization",
                "ram:GetResourcePolicies",
                "ecr:GetAuthorizationToken",
                "s3:GetAccessPoint",
                "s3:GetAccountPublicAccessBlock",
                "s3:ListAccessPoints",
            ],
            "Resource": ["*"],
        }

        result = get_statement_from_policy_using_sid(policy_json, "MultMultNone")
        self.assertDictEqual(result, expected_result)
