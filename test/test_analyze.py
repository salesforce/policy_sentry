import os
import unittest
from policy_sentry.shared.database import connect_db
from policy_sentry.shared.constants import DATABASE_FILE_PATH
from policy_sentry.analysis.analyze import analyze_by_access_level, analyze_statement_by_access_level, determine_risky_actions_from_list
from policy_sentry.util.policy_files import get_actions_from_json_policy_file, get_actions_from_policy
from policy_sentry.querying.actions import remove_actions_not_matching_access_level
from policy_sentry.util.policy_files import get_actions_from_json_policy_file, get_actions_from_policy

db_session = connect_db(DATABASE_FILE_PATH)


class AnalyzeActionsTestCase(unittest.TestCase):

    def test_remove_actions_not_matching_access_level(self):
        """test_remove_actions_not_matching_access_level: Verify remove_actions_not_matching_access_level is working as expected"""
        actions_list = [
            "ecr:BatchGetImage",  # Read
            "ecr:CreateRepository",  # Write
            "ecr:DescribeRepositories",  # List
            "ecr:TagResource",  # Tagging
            "ecr:SetRepositoryPolicy",  # Permissions management
        ]
        # print("Read ")
        self.maxDiff = None
        # Read
        self.assertListEqual(remove_actions_not_matching_access_level(db_session, actions_list, "read"), ["ecr:batchgetimage"])
        # Write
        self.assertListEqual(remove_actions_not_matching_access_level(db_session, actions_list, "write"), ["ecr:createrepository"])
        # List
        self.assertListEqual(remove_actions_not_matching_access_level(db_session, actions_list, "list"), ["ecr:describerepositories"])
        # Tagging
        self.assertListEqual(remove_actions_not_matching_access_level(db_session, actions_list, "tagging"), ["ecr:tagresource"])
        # Permissions management
        self.assertListEqual(remove_actions_not_matching_access_level(db_session, actions_list, "permissions-management"), ["ecr:setrepositorypolicy"])

    def test_get_actions_from_policy(self):
        """test_get_actions_from_policy: Verify that the get_actions_from_policy function is grabbing the actions
        from a dict properly"""
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
                        "ecr:PutImage"
                    ],
                    "Resource": "*"
                },
              {
                    "Sid": "AllowManageOwnAccessKeys",
                    "Effect": "Allow",
                    "Action": [
                        "iam:CreateAccessKey",
                        "iam:DeleteAccessKey",
                        "iam:ListAccessKeys",
                        "iam:UpdateAccessKey"
                    ],
                    "Resource": "arn:aws:iam::*:user/${aws:username}"
                }
            ]
        }
        actions_list = get_actions_from_policy(policy)
        desired_actions_list = [
            'ecr:batchchecklayeravailability',
            'ecr:batchgetimage',
            'ecr:completelayerupload',
            'ecr:describeimages',
            'ecr:describerepositories',
            'ecr:getauthorizationtoken',
            'ecr:getdownloadurlforlayer',
            'ecr:getrepositorypolicy',
            'ecr:initiatelayerupload',
            'ecr:listimages',
            'ecr:putimage',
            'ecr:uploadlayerpart',
            'iam:createaccesskey',
            'iam:deleteaccesskey',
            'iam:listaccesskeys',
            'iam:updateaccesskey'
        ]
        self.maxDiff = None
        self.assertListEqual(desired_actions_list, actions_list)

    def test_get_actions_from_policy_file_with_wildcards(self):
        """test_get_actions_from_policy_file_with_wildcards: Verify that we can read the actions from a file,
        even if it contains wildcards"""
        policy_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir +
                                                        '/examples/analyze/wildcards.json'))
        requested_actions = get_actions_from_json_policy_file(policy_file_path)
        # print(requested_actions)
        desired_actions_list = ['ecr:*', 's3:*']
        self.maxDiff = None
        self.assertListEqual(requested_actions, desired_actions_list)

    def test_get_actions_from_policy_file_with_explicit_actions(self):
        """test_get_actions_from_policy_file_with_explicit_actions: Verify that we can get a list of actions from a
        file when it contains specific actions"""
        policy_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir +
                                                        '/examples/analyze/explicit-actions.json'))
        requested_actions = get_actions_from_json_policy_file(policy_file_path)
        # print(requested_actions)
        desired_actions_list = [
            'ecr:batchchecklayeravailability',
            'ecr:batchgetimage',
            'ecr:completelayerupload',
            'ecr:describeimages',
            'ecr:describerepositories',
            'ecr:getauthorizationtoken',
            'ecr:getdownloadurlforlayer',
            'ecr:getrepositorypolicy',
            'ecr:initiatelayerupload',
            'ecr:listimages',
            'ecr:putimage',
            'ecr:uploadlayerpart',
            'iam:createaccesskey',
            'iam:deleteaccesskey',
            'iam:listaccesskeys',
            'iam:updateaccesskey'
        ]
        self.maxDiff = None
        self.assertListEqual(requested_actions, desired_actions_list)

    def test_analyze_by_access_level(self):
        """test_analyze_by_access_level: Test out calling this as a library"""
        permissions_management_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        # This one is Permissions management
                        "ecr:setrepositorypolicy",
                        "secretsmanager:DeleteResourcePolicy",
                        # These ones are not permissions management
                        "ecr:GetRepositoryPolicy",
                        "ecr:DescribeRepositories",
                        "ecr:ListImages",
                        "ecr:DescribeImages",
                    ],
                    "Resource": "*"
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
                    "Resource": "arn:aws:iam::*:user/${aws:username}"
                }
            ]
        }
        permissions_management_actions = analyze_by_access_level(db_session, permissions_management_policy, "permissions-management")
        # print(permissions_management_actions)
        desired_actions_list = [
            'ecr:setrepositorypolicy',
            'iam:createaccesskey',
            'iam:deleteaccesskey',
            'iam:updateaccesskey',
            'secretsmanager:deleteresourcepolicy'
        ]
        self.maxDiff = None
        self.assertListEqual(permissions_management_actions, desired_actions_list)

    def test_analyze_statement_by_access_level(self):
        """test_analyze_statement_by_access_level: Test out calling this as a library"""
        permissions_management_statement = {
            "Effect": "Allow",
            "Action": [
                # This one is Permissions management
                "ecr:setrepositorypolicy",
                "secretsmanager:DeleteResourcePolicy",
                # These ones are not permissions management
                "ecr:GetRepositoryPolicy",
                "ecr:DescribeRepositories",
                "ecr:ListImages",
                "ecr:DescribeImages",
            ],
            "Resource": "*"
        }
        permissions_management_actions = analyze_statement_by_access_level(db_session, permissions_management_statement, "permissions-management")
        # print(permissions_management_actions)
        desired_actions_list = [
            'ecr:setrepositorypolicy',
            'secretsmanager:deleteresourcepolicy'
        ]
        self.maxDiff = None
        self.assertListEqual(permissions_management_actions, desired_actions_list)

    def test_determine_risky_actions_from_list(self):
        """test_determine_risky_actions_from_list: Test comparing requested actions to a list of risky actions"""
        requested_actions = [
            'ecr:putimage',
            'ecr:uploadlayerpart',
            'iam:createaccesskey',
            'iam:deleteaccesskey'
        ]
        risky_actions = [
            'iam:createaccesskey',
            'iam:deleteaccesskey',
            'iam:listaccesskeys',
            'iam:updateaccesskey'
        ]
        actions_to_triage = determine_risky_actions_from_list(requested_actions, risky_actions)
        expected = [
            'iam:createaccesskey',
            'iam:deleteaccesskey'
        ]
        self.maxDiff = None
        self.assertListEqual(actions_to_triage, expected)
