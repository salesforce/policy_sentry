import os
import unittest
from policy_sentry.util.policy_files import (
    get_actions_from_json_policy_file,
    get_actions_from_policy,
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
                        "ecr:GetAuthorizationToken",
                        "ecr:BatchCheckLayerAvailability",
                        "ecr:GetDownloadUrlForLayer",
                        "ecr:GetRepositoryPolicy",
                        "ecr:DescribeRepositories",
                        "ecr:ListImages",
                        "ecr:DescribeImages",
                        "ecr:BatchGetImage",
                        "ecr:InitiateLayerUpload",
                        "ecr:UploadLayerPart",
                        "ecr:CompleteLayerUpload",
                        "ecr:PutImage",
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
            "ecr:batchchecklayeravailability",
            "ecr:batchgetimage",
            "ecr:completelayerupload",
            "ecr:describeimages",
            "ecr:describerepositories",
            "ecr:getauthorizationtoken",
            "ecr:getdownloadurlforlayer",
            "ecr:getrepositorypolicy",
            "ecr:initiatelayerupload",
            "ecr:listimages",
            "ecr:putimage",
            "ecr:uploadlayerpart",
            "iam:createaccesskey",
            "iam:deleteaccesskey",
            "iam:listaccesskeys",
            "iam:updateaccesskey",
        ]
        self.maxDiff = None
        self.assertListEqual(desired_actions_list, actions_list)

    def test_get_actions_from_policy_file_with_wildcards(self):
        """util.policy_files.get_actions_from_policy_file_with_wildcards: Verify that we can read the actions from a file,
        even if it contains wildcards"""
        policy_file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.path.pardir
                + "/"
                + os.path.pardir
                + "/examples/analyze/wildcards.json",
            )
        )
        requested_actions = get_actions_from_json_policy_file(policy_file_path)
        # print(requested_actions)
        desired_actions_list = ["ecr:*", "s3:*"]
        self.maxDiff = None
        self.assertListEqual(requested_actions, desired_actions_list)

    def test_get_actions_from_policy_file_with_explicit_actions(self):
        """util.policy_file.get_actions_from_policy_file_with_explicit_actions: Verify that we can get a list of actions from a
        file when it contains specific actions"""
        policy_file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.path.pardir
                + "/"
                + os.path.pardir
                + "/examples/analyze/explicit-actions.json",
            )
        )
        requested_actions = get_actions_from_json_policy_file(policy_file_path)
        # print(requested_actions)
        desired_actions_list = [
            "ecr:batchchecklayeravailability",
            "ecr:batchgetimage",
            "ecr:completelayerupload",
            "ecr:describeimages",
            "ecr:describerepositories",
            "ecr:getauthorizationtoken",
            "ecr:getdownloadurlforlayer",
            "ecr:getrepositorypolicy",
            "ecr:initiatelayerupload",
            "ecr:listimages",
            "ecr:putimage",
            "ecr:uploadlayerpart",
            "iam:createaccesskey",
            "iam:deleteaccesskey",
            "iam:listaccesskeys",
            "iam:updateaccesskey",
        ]
        self.maxDiff = None
        self.assertListEqual(requested_actions, desired_actions_list)
