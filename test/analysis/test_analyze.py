from policy_sentry.analysis.analyze import (
    determine_actions_to_expand,
    analyze_by_access_level,
    analyze_statement_by_access_level,
)
import unittest
import json


class AnalysisExpandWildcardActionsTestCase(unittest.TestCase):
    def test_a_determine_actions_to_expand_not_upper_camelcase(self):
        """test_determine_actions_to_expand_not_upper_camelcase: The nOtCaMeLcAsE version of the same test"""
        action_list = ["ecr:pUt*"]
        self.maxDiff = None
        expected_results = [
            "ecr:PutImage",
            "ecr:PutImageScanningConfiguration",
            "ecr:PutImageTagMutability",
            "ecr:PutLifecyclePolicy",
        ]
        result = determine_actions_to_expand(action_list)
        print(result)
        self.maxDiff = None
        results = determine_actions_to_expand(action_list)
        for expected_result in expected_results:
            self.assertTrue(expected_result in results)

    def test_determine_actions_to_expand(self):
        """
        test_determine_actions_to_expand: provide expanded list of actions, like ecr:*
        :return:
        """
        action_list = ["ecr:*"]
        self.maxDiff = None
        expected_results = [
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
        # print(determine_actions_to_expand(action_list))
        self.maxDiff = None
        results = determine_actions_to_expand(action_list)
        for expected_result in expected_results:
            self.assertTrue(expected_result in results)

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
            permissions_management_policy, "Permissions management"
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
        result = analyze_statement_by_access_level(
            permissions_management_statement, "Permissions management"
        )
        # print(permissions_management_actions)
        desired_result = [
            "ecr:SetRepositoryPolicy",
            "secretsmanager:DeleteResourcePolicy",
        ]
        self.maxDiff = None
        self.assertListEqual(result, desired_result)

    def test_gh_162(self):
        """test_gh_162: Addressing the concern in the Github issue
        https://github.com/salesforce/policy_sentry/issues/162"""
        permissions_management_policy = {
            "Statement": [
                {
                    "Action": [
                        "s3:GetObject*",
                        "s3:PutObject*"
                    ],
                    "Effect": "Allow",
                    "Resource": [
                        "*"
                    ]
                }
            ],
            "Version": "2012-10-17"
        }
        print('********* READ ***********')
        results = analyze_by_access_level(permissions_management_policy, "Read")
        print(json.dumps(results, indent=4))
        # Rather than maintaining a large list as AWS keeps adding new actions,
        # just verify that an expanded action exists in the list
        self.assertTrue("s3:GetObjectAcl" in results)
        print('********* LIST ***********')
        results = analyze_by_access_level(permissions_management_policy, "List")
        print(json.dumps(results, indent=4))
        self.assertListEqual(results, [])
        print('********* WRITE ***********')
        results = analyze_by_access_level(permissions_management_policy, "Write")
        print(json.dumps(results, indent=4))
        self.assertTrue("s3:PutObjectLegalHold" in results)
        print('********* TAGGING ***********')
        results = analyze_by_access_level(permissions_management_policy, "Tagging")
        print(json.dumps(results, indent=4))
        self.assertTrue("s3:PutObjectTagging" in results)
        print('********* PERMISSIONS-MANAGEMENT ***********')
        results = analyze_by_access_level(permissions_management_policy, "Permissions management")
        print(json.dumps(results, indent=4))
        self.assertTrue("s3:PutObjectAcl" in results)

