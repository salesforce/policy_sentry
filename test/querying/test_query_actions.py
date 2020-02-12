import unittest
import json
from policy_sentry.shared.constants import DATABASE_FILE_PATH
from policy_sentry.shared.database import connect_db
from policy_sentry.querying.actions import (
    get_actions_for_service,
    get_action_data,
    get_actions_with_access_level,
    get_actions_with_arn_type_and_access_level,
    get_actions_matching_condition_key,
    get_actions_that_support_wildcard_arns_only,
    get_actions_matching_condition_crud_and_arn,
    get_actions_at_access_level_that_support_wildcard_arns_only,
    remove_actions_that_are_not_wildcard_arn_only,
    get_dependent_actions,
    remove_actions_not_matching_access_level,
)

db_session = connect_db(DATABASE_FILE_PATH)


class QueryActionsTestCase(unittest.TestCase):
    def test_get_actions_for_service(self):
        """querying.actions.get_actions_for_service"""
        desired_output = [
            "ram:AcceptResourceShareInvitation",
            "ram:AssociateResourceShare",
            "ram:AssociateResourceSharePermission",
            "ram:CreateResourceShare",
            "ram:DeleteResourceShare",
            "ram:DisassociateResourceShare",
            "ram:DisassociateResourceSharePermission",
            "ram:EnableSharingWithAwsOrganization",
            "ram:GetPermission",
            "ram:GetResourcePolicies",
            "ram:GetResourceShareAssociations",
            "ram:GetResourceShareInvitations",
            "ram:GetResourceShares",
            "ram:ListPendingInvitationResources",
            "ram:ListPermissions",
            "ram:ListPrincipals",
            "ram:ListResourceSharePermissions",
            "ram:ListResources",
            "ram:RejectResourceShareInvitation",
            "ram:TagResource",
            "ram:UntagResource",
            "ram:UpdateResourceShare",
        ]
        output = get_actions_for_service(db_session, "ram")
        print(output)
        self.maxDiff = None
        self.assertListEqual(desired_output, output)

    def test_get_action_data(self):
        """querying.actions.test_get_action_data"""
        desired_output = {
            "ram": [
                {
                    "action": "ram:CreateResourceShare",
                    "description": "Create resource share with provided resource(s) and/or principal(s)",
                    "access_level": "Permissions management",
                    "resource_arn_format": "*",
                    "condition_keys": [
                        "aws:RequestTag/${TagKey}",
                        "aws:TagKeys",
                        "ram:RequestedResourceType",
                        "ram:ResourceArn",
                        "ram:RequestedAllowsExternalPrincipals",
                        "ram:Principal",
                    ],
                    "dependent_actions": None,
                }
            ]
        }
        output = get_action_data(db_session, "ram", "createresourceshare")
        print(json.dumps(output, indent=4))
        self.maxDiff = None
        self.assertDictEqual(desired_output, output)

    def test_get_actions_that_support_wildcard_arns_only(self):
        """querying.actions.get_actions_that_support_wildcard_arns_only"""
        desired_output = [
            "secretsmanager:CreateSecret",
            "secretsmanager:GetRandomPassword",
            "secretsmanager:ListSecrets",
        ]
        output = get_actions_that_support_wildcard_arns_only(
            db_session, "secretsmanager"
        )
        self.maxDiff = None
        print(output)
        self.assertListEqual(desired_output, output)

    def test_get_actions_at_access_level_that_support_wildcard_arns_only(self):
        """querying.actions.get_actions_at_access_level_that_support_wildcard_arns_only"""
        permissions_output = get_actions_at_access_level_that_support_wildcard_arns_only(
            db_session, "s3", "Permissions management"
        )
        list_output = get_actions_at_access_level_that_support_wildcard_arns_only(
            db_session, "s3", "List"
        )
        read_output = get_actions_at_access_level_that_support_wildcard_arns_only(
            db_session, "s3", "Read"
        )
        self.assertListEqual(permissions_output, ["s3:PutAccountPublicAccessBlock"])
        self.assertListEqual(list_output, ["s3:ListAllMyBuckets"])
        self.assertListEqual(
            read_output,
            [
                "s3:GetAccessPoint",
                "s3:GetAccountPublicAccessBlock",
                "s3:ListAccessPoints",
            ],
        )

    def test_get_actions_with_access_level(self):
        """querying.actions.get_actions_with_access_level"""
        desired_output = [
            "ram:AcceptResourceShareInvitation",
            "ram:AssociateResourceShare",
            "ram:CreateResourceShare",
            "ram:DeleteResourceShare",
            "ram:DisassociateResourceShare",
            "ram:EnableSharingWithAwsOrganization",
            "ram:RejectResourceShareInvitation",
            "ram:UpdateResourceShare",
        ]
        output = get_actions_with_access_level(
            db_session, "ram", "Permissions management"
        )
        # print(output)
        self.maxDiff = None
        print(output)
        self.assertListEqual(desired_output, output)

    def test_get_actions_with_arn_type_and_access_level(self):
        """querying.actions.get_actions_with_arn_type_and_access_level"""
        desired_output = [
            "ram:AssociateResourceShare",
            # 'ram:createresourceshare',
            "ram:DeleteResourceShare",
            "ram:DisassociateResourceShare",
            "ram:UpdateResourceShare",
        ]
        output = get_actions_with_arn_type_and_access_level(
            db_session, "ram", "resource-share", "Permissions management"
        )
        print(output)
        self.maxDiff = None
        self.assertListEqual(desired_output, output)

    def test_get_actions_matching_condition_key(self):
        """querying.actions.get_actions_matching_condition_key"""
        desired_output = [
            'ses:SendEmail',
            'ses:SendBulkTemplatedEmail',
            'ses:SendCustomVerificationEmail',
            'ses:SendEmail',
            'ses:SendRawEmail',
            'ses:SendTemplatedEmail'
        ]

        output = get_actions_matching_condition_key(
            db_session, "ses", "ses:FeedbackAddress"
        )
        # print(output)
        self.maxDiff = None
        print(output)
        self.assertListEqual(desired_output, output)

    def test_get_actions_matching_condition_crud_and_arn(self):
        """querying.actions.get_actions_matching_condition_crud_and_arn"""
        results = get_actions_matching_condition_crud_and_arn(
            db_session,
            "elasticbeanstalk:InApplication",
            "List",
            "arn:${Partition}:elasticbeanstalk:${Region}:${Account}:environment/${ApplicationName}/${EnvironmentName}",
        )
        desired_results = [
            "elasticbeanstalk:DescribeEnvironments",
        ]
        print(results)
        self.assertListEqual(desired_results, results)

    def test_get_actions_matching_condition_crud_and_wildcard_arn(self):
        """querying.actions.get_actions_matching_condition_crud_and_wildcard_arn"""
        desired_results = [
            "swf:PollForActivityTask",
            "swf:PollForDecisionTask",
            "swf:RespondActivityTaskCompleted",
            "swf:StartWorkflowExecution",
        ]
        results = get_actions_matching_condition_crud_and_arn(
            db_session, "swf:taskList.name", "Write", "*"
        )
        print(results)
        self.assertListEqual(desired_results, results)

        # This one leverages a condition key that is partway through a string in the database
        # - luckily, SQLAlchemy's ilike function allows us to find it anyway because it's a substring
        # kms:CallerAccount,kms:EncryptionAlgorithm,kms:EncryptionContextKeys,kms:ViaService
        desired_results = [
            "kms:Decrypt",
            "kms:Encrypt",
            "kms:GenerateDataKey",
            "kms:GenerateDataKeyPair",
            "kms:GenerateDataKeyPairWithoutPlaintext",
            "kms:GenerateDataKeyWithoutPlaintext",
            "kms:ReEncryptFrom",
            "kms:ReEncryptTo",
        ]
        print(results)
        results = get_actions_matching_condition_crud_and_arn(
            db_session, "kms:EncryptionAlgorithm", "Write", "*"
        )
        self.assertListEqual(desired_results, results)

    def test_remove_actions_not_matching_access_level(self):
        """querying.actions.remove_actions_not_matching_access_level"""
        actions_list = [
            "ecr:batchgetimage",  # read
            "ecr:createrepository",  # write
            "ecr:describerepositories",  # list
            "ecr:tagresource",  # tagging
            "ecr:setrepositorypolicy",  # permissions management
        ]
        # print("Read ")
        self.maxDiff = None
        # Read
        read_result = remove_actions_not_matching_access_level(
            db_session, actions_list, "read"
        )
        self.assertListEqual(read_result, ["ecr:BatchGetImage"])
        # Write
        write_result = remove_actions_not_matching_access_level(
            db_session, actions_list, "write"
        )
        self.assertListEqual(write_result, ["ecr:CreateRepository"])
        # List
        list_result = remove_actions_not_matching_access_level(
            db_session, actions_list, "list"
        )
        self.assertListEqual(list_result, ["ecr:DescribeRepositories"])
        # Tagging
        tagging_result = remove_actions_not_matching_access_level(
            db_session, actions_list, "tagging"
        )
        self.assertListEqual(tagging_result, ["ecr:TagResource"])
        # Permissions management
        permissions_result = remove_actions_not_matching_access_level(
            db_session, actions_list, "permissions-management"
        )
        self.assertListEqual(permissions_result, ["ecr:SetRepositoryPolicy"])

    def test_get_dependent_actions(self):
        """querying.actions.get_dependent_actions"""
        dependent_actions_single = ["ec2:associateiaminstanceprofile"]
        dependent_actions_double = ["shield:associatedrtlogbucket"]
        dependent_actions_several = ["chime:getcdrbucket"]
        self.assertEqual(
            get_dependent_actions(db_session, dependent_actions_single),
            ["iam:PassRole"],
        )
        self.assertEqual(
            get_dependent_actions(db_session, dependent_actions_double),
            ["s3:GetBucketPolicy", "s3:PutBucketPolicy"],
        )
        self.assertEqual(
            get_dependent_actions(db_session, dependent_actions_several),
            [
                "s3:GetBucketAcl",
                "s3:GetBucketLocation",
                "s3:GetBucketLogging",
                "s3:GetBucketVersioning",
                "s3:GetBucketWebsite",
            ],
        )

    def test_remove_actions_that_are_not_wildcard_arn_only(self):
        """querying.actions.remove_actions_that_are_not_wildcard_arn_only"""
        provided_actions_list = [
            # 3 wildcard only actions
            "secretsmanager:createsecret",
            "secretsmanager:getrandompassword",
            "secretsmanager:listsecrets",
            # This one is wildcard OR "secret"
            "secretsmanager:putsecretvalue",
        ]
        desired_output = [
            # 3 wildcard only actions
            "secretsmanager:CreateSecret",
            "secretsmanager:GetRandomPassword",
            "secretsmanager:ListSecrets",
        ]
        output = remove_actions_that_are_not_wildcard_arn_only(
            db_session, provided_actions_list
        )
        self.maxDiff = None
        self.assertListEqual(desired_output, output)

# TODO: Test it when we give actions with wEiRd cases, and it should feed us back the cleaned up version.
# # TODO: Because above, it actually would fail when they were lowercase, and it would pass when they were UpperCamelCase
