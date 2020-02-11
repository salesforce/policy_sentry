from policy_sentry.analysis.analyze import (
    determine_actions_to_expand,
    analyze_by_access_level,
    determine_risky_actions_from_list,
    analyze_statement_by_access_level,
)
from policy_sentry.shared.database import connect_db
from policy_sentry.shared.constants import DATABASE_FILE_PATH
import unittest

db_session = connect_db(DATABASE_FILE_PATH)


class AnalysisExpandWildcardActionsTestCase(unittest.TestCase):
    # TODO: Write a wEiRd nOtCaMeLCaSe version of this
    def test_determine_actions_to_expand(self):
        """
        test_determine_actions_to_expand: provide expanded list of actions, like ecr:*
        :return:
        """
        action_list = ["ecr:*"]
        self.maxDiff = None
        desired_result = [
            "ecr:BatchCheckLayerAvailability",
            "ecr:BatchDeleteImage",
            "ecr:BatchGetImage",
            "ecr:CompleteLayerUpload",
            "ecr:CreateRepository",
            "ecr:DeleteLifecyclePolicy",
            "ecr:DeleteRepository",
            "ecr:DeleteRepositoryPolicy",
            "ecr:DescribeImageScanFindings",
            "ecr:DescribeImages",
            "ecr:DescribeRepositories",
            "ecr:GetAuthorizationToken",
            "ecr:GetDownloadUrlForLayer",
            "ecr:GetLifecyclePolicy",
            "ecr:GetLifecyclePolicyPreview",
            "ecr:GetRepositoryPolicy",
            "ecr:InitiateLayerUpload",
            "ecr:ListImages",
            "ecr:ListTagsForResource",
            "ecr:PutImage",
            "ecr:PutImageScanningConfiguration",
            "ecr:PutImageTagMutability",
            "ecr:PutLifecyclePolicy",
            "ecr:SetRepositoryPolicy",
            "ecr:StartImageScan",
            "ecr:StartLifecyclePolicyPreview",
            "ecr:TagResource",
            "ecr:UntagResource",
            "ecr:UploadLayerPart"
        ]
        # print(determine_actions_to_expand(db_session, action_list))
        self.maxDiff = None
        self.assertListEqual(
            sorted(determine_actions_to_expand(db_session, action_list)),
            sorted(desired_result),
        )

    def test_analyze_by_access_level(self):
        """test_analyze_by_access_level: Test out calling this as a library"""
        permissions_management_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        # This one is Permissions management
                        "ecr:SetRepositoryPolicy",
                        "secretsmanager:DeleteResourcePolicy",
                        # These ones are not permissions management
                        "ecr:getrepositorypolicy",
                        "ecr:describerepositories",
                        "ecr:listimages",
                        "ecr:DescribeImages",
                    ],
                    "Resource": "*",
                },
                {
                    "Sid": "AllowManageOwnAccessKeys",
                    "Effect": "Allow",
                    "Action": [
                        # These ones are permissions management
                        "iam:CreateAccessKey",
                        "iam:DeleteAccessKey",
                        "iam:UpdateAccessKey",
                        # This one is not
                        "iam:ListAccessKeys",
                    ],
                    "Resource": "arn:aws:iam::*:user/${aws:username}",
                },
            ],
        }
        permissions_management_actions = analyze_by_access_level(
            db_session, permissions_management_policy, "permissions-management"
        )
        # print(permissions_management_actions)
        desired_actions_list = [
            "ecr:SetRepositoryPolicy",
            "iam:CreateAccessKey",
            "iam:DeleteAccessKey",
            "iam:UpdateAccessKey",
            "secretsmanager:DeleteResourcePolicy",
        ]
        self.maxDiff = None
        self.assertListEqual(permissions_management_actions, desired_actions_list)

    def test_analyze_statement_by_access_level(self):
        """test_analyze_statement_by_access_level: Test out calling this as a library"""
        permissions_management_statement = {
            "Effect": "Allow",
            "Action": [
                # This one is Permissions management
                "ecr:SetRepositoryPolicy",
                "secretsmanager:DeleteResourcePolicy",
                # These ones are not permissions management
                "ecr:GetRepositoryPolicy",
                "ecr:DescribeRepositories",
                "ecr:ListImages",
                "ecr:DescribeImages",
            ],
            "Resource": "*",
        }
        permissions_management_actions = analyze_statement_by_access_level(
            db_session, permissions_management_statement, "permissions-management"
        )
        # print(permissions_management_actions)
        desired_actions_list = [
            "ecr:SetRepositoryPolicy",
            "secretsmanager:DeleteResourcePolicy",
        ]
        self.maxDiff = None
        self.assertListEqual(permissions_management_actions, desired_actions_list)

    def test_determine_risky_actions_from_list(self):
        """test_determine_risky_actions_from_list: Test comparing requested actions to a list of risky actions"""
        requested_actions = [
            "ecr:putimage",
            "ecr:uploadlayerpart",
            "iam:createaccesskey",
            "iam:deleteaccesskey",
        ]
        risky_actions = [
            "iam:createaccesskey",
            "iam:deleteaccesskey",
            "iam:listaccesskeys",
            "iam:updateaccesskey",
        ]
        actions_to_triage = determine_risky_actions_from_list(
            requested_actions, risky_actions
        )
        expected = ["iam:createaccesskey", "iam:deleteaccesskey"]
        self.maxDiff = None
        self.assertListEqual(actions_to_triage, expected)
