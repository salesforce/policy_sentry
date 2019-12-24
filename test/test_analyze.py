import os
import unittest
import logging
from policy_sentry.shared.database import connect_db
from policy_sentry.shared.constants import DATABASE_FILE_PATH
from policy_sentry.shared.analyze import analyze_by_access_level
from policy_sentry.shared.finding import Findings
from policy_sentry.shared.actions import get_actions_by_access_level, get_actions_from_policy, \
    get_actions_from_json_policy_file

db_session = connect_db(DATABASE_FILE_PATH)
logging.basicConfig()
logger = logging.getLogger('policy_sentry')

resource_exposure_finding = {
    "some-risky-policy": {
        "account_id": "0123456789012",
        "resource_exposure": [
            "iam:createaccesskey",
            "iam:deleteaccesskey"
        ]
    }
}
privilege_escalation_finding = {
    "some-risky-policy": {
        "account_id": "0123456789012",
        "privilege_escalation": [
            "iam:createaccesskey"
        ]
    }
}
privilege_escalation_finding_account_2 = {
    "some-risky-policy": {
        "account_id": "9876543210123",
        "privilege_escalation": [
            "iam:createaccesskey"
        ]
    }
}
privilege_escalation_yolo_policy = {
    "yolo-policy": {
        "account_id": "9876543210123",
        "privilege_escalation": [
            "iam:createaccesskey"
        ]
    }
}


class FindingsTestCase(unittest.TestCase):
    def test_get_findings(self):
        """test_get_findings: Ensure that finding.get_findings() combines two risk findings for one policy properly."""
        findings = Findings()
        desired_result = {
            "some-risky-policy": {
                "account_id": "0123456789012",
                "resource_exposure": [
                    "iam:createaccesskey",
                    "iam:deleteaccesskey"
                ],
                "privilege_escalation": [
                    "iam:createaccesskey"
                ]
            }
        }
        findings.add(resource_exposure_finding)
        findings.add(privilege_escalation_finding)
        occurrences = findings.get_findings()
        self.assertDictEqual(occurrences, desired_result)

    def test_get_findings_by_policy_name(self):
        """test_get_findings_by_policy_name: Testing out the 'Findings' object"""
        findings = Findings()
        # Policy name: some-risky-policy
        findings.add(privilege_escalation_finding)
        logger.debug(privilege_escalation_finding)
        # Policy name: yolo-policy
        findings.add(privilege_escalation_yolo_policy)
        logger.debug(privilege_escalation_yolo_policy)
        findings_for_second_policy_name = findings.get_findings_by_policy_name('yolo-policy')
        logger.debug(findings_for_second_policy_name)
        self.assertDictEqual(findings_for_second_policy_name, privilege_escalation_yolo_policy['yolo-policy'])

    # def test_get_findings_by_account_id(self):
    #     findings = Findings()
    #     # account ID = 0123456789012
    #     findings.add('privilege_escalation', privilege_escalation_finding)
    #     # account ID = 9876543210123
    #     findings.add('privilege_escalation', privilege_escalation_finding_account_2)
    #     findings_for_second_account = findings.get_findings_by_account_id('9876543210123')
    #     self.assertDictEqual(findings_for_second_account, privilege_escalation_finding_account_2)


class AnalyzeActionsTestCase(unittest.TestCase):

    def test_get_actions_by_access_level(self):
        """test_get_actions_by_access_level: Verify get_actions_by_access_level is working as expected"""
        actions_list = [
            "ecr:BatchGetImage",  # Read
            "ecr:CreateRepository",  # Write
            "ecr:DescribeRepositories",  # List
            "ecr:TagResource",  # Tagging
            "ecr:SetRepositoryPolicy",  # Permissions management
        ]
        logger.debug("Read")
        # Read
        self.assertListEqual(get_actions_by_access_level(db_session, actions_list, "read"), ["ecr:batchgetimage"])
        # Write
        self.assertListEqual(get_actions_by_access_level(db_session, actions_list, "write"), ["ecr:createrepository"])
        # List
        self.assertListEqual(get_actions_by_access_level(db_session, actions_list, "list"), ["ecr:describerepositories"])
        # Tagging
        self.assertListEqual(get_actions_by_access_level(db_session, actions_list, "tagging"), ["ecr:tagresource"])
        # Permissions management
        self.assertListEqual(get_actions_by_access_level(db_session, actions_list, "permissions-management"), ["ecr:setrepositorypolicy"])

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
        logger.debug(requested_actions)
        desired_actions_list = ['ecr:*', 's3:*']
        self.maxDiff = None
        self.assertListEqual(requested_actions, desired_actions_list)

    def test_get_actions_from_policy_file_with_explicit_actions(self):
        """test_get_actions_from_policy_file_with_explicit_actions: Verify that we can get a list of actions from a
        file when it contains specific actions"""
        policy_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir +
                                                        '/examples/analyze/explicit-actions.json'))
        requested_actions = get_actions_from_json_policy_file(policy_file_path)
        logger.debug(requested_actions)
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
                        "iam:UpdateAccessKey"
                        # This one is not
                        "iam:ListAccessKeys",
                    ],
                    "Resource": "arn:aws:iam::*:user/${aws:username}"
                }
            ]
        }
        permissions_management_actions = analyze_by_access_level(permissions_management_policy, db_session, "permissions-management")
        logger.debug(permissions_management_actions)
        desired_actions_list = [
            'ecr:setrepositorypolicy',
            'iam:createaccesskey',
            'iam:deleteaccesskey',
            'secretsmanager:deleteresourcepolicy'
        ]
        self.assertListEqual(permissions_management_actions, desired_actions_list)

