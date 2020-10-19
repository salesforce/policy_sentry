import unittest
import os
import json
from schema import Optional, Schema, And, Use, SchemaError
from policy_sentry.shared.iam_data import get_service_prefix_data
from policy_sentry.querying.actions import (
    get_actions_for_service,
    get_privilege_info,
    get_action_data,
    get_actions_that_support_wildcard_arns_only,
    get_actions_at_access_level_that_support_wildcard_arns_only,
    get_actions_with_access_level,
    get_actions_with_arn_type_and_access_level,
    remove_actions_not_matching_access_level,
    get_dependent_actions,
    remove_actions_that_are_not_wildcard_arn_only,
    get_actions_matching_condition_key,
    get_actions_matching_arn,
    get_actions_matching_arn_type
    # get_actions_matching_condition_crud_and_arn
)
from policy_sentry.writing.validate import check


class QueryActionsTestCase(unittest.TestCase):
    def test_get_service_prefix_data(self):
        result = get_service_prefix_data("cloud9")
        desired_output_schema = Schema(
            {
                "service_name": "AWS Cloud9",
                "prefix": "cloud9",
                "privileges": dict,
                "resources": dict,
                "conditions": dict
            }
        )
        valid_output = check(desired_output_schema, result)
        # print(json.dumps(result, indent=4))
        self.assertTrue(valid_output)

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
            "ram:UpdateResourceShare"
        ]
        output = get_actions_for_service("ram")
        # print(json.dumps(output, indent=4))
        self.maxDiff = None
        self.assertListEqual(desired_output, output)

        # performance notes
        # old: 0.021s
        # this one: 0.005s

    def test_get_actions_for_invalid_service(self):
        """querying.actions.get_actions_for_service
           for invalid service
        """
        output = get_actions_for_service("invalid_service")
        self.assertListEqual([], output)

    def test_get_privilege_info(self):
        expected_results_file = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "get_privilege_info_cloud9.json",
            )
        )
        # print(expected_results_file)
        with open(expected_results_file) as json_file:
            expected_results = json.load(json_file)
        results = get_privilege_info("cloud9", "CreateEnvironmentEC2")
        print(json.dumps(results, indent=4))
        self.assertDictEqual(results, expected_results)

    # def test_get_privilege_info_2(self):
    #     results = get_privilege_info("ram", "CreateResourceShare")
    #     # results = get_privilege_info("ram", "createresourceshare")
    #     print(json.dumps(results, indent=4))

    def test_get_action_data(self):
        """querying.actions.test_get_action_data"""
        desired_output = {
            "ram": [
                {
                    "action": "ram:TagResource",
                    "description": "Tag the specified resources share",
                    "access_level": "Tagging",
                    "resource_arn_format": "arn:${Partition}:ram:${Region}:${Account}:resource-share/${ResourcePath}",
                    "condition_keys": [
                        "aws:ResourceTag/${TagKey}",
                        "ram:AllowsExternalPrincipals",
                        "ram:ResourceShareName"
                    ],
                    "dependent_actions": []
                },
                {
                    "action": "ram:TagResource",
                    "description": "Tag the specified resources share",
                    "access_level": "Tagging",
                    "resource_arn_format": "*",
                    "condition_keys": [
                        "aws:ResourceTag/${TagKey}",
                        "ram:AllowsExternalPrincipals",
                        "ram:ResourceShareName"
                    ],
                    "dependent_actions": []
                }
            ]
        }
        output = get_action_data("ram", "TagResource")
        # print(json.dumps(output, indent=4))
        self.maxDiff = None
        self.assertDictEqual(desired_output, output)

    def test_get_actions_that_support_wildcard_arns_only(self):
        """querying.actions.get_actions_that_support_wildcard_arns_only"""
        desired_output = [
            "secretsmanager:GetRandomPassword",
            "secretsmanager:ListSecrets",
        ]
        output = get_actions_that_support_wildcard_arns_only("secretsmanager")
        self.maxDiff = None
        self.assertListEqual(desired_output, output)

        output = get_actions_that_support_wildcard_arns_only("ecr")
        self.assertEqual(output, ["ecr:GetAuthorizationToken"])
        # print(json.dumps(output, indent=4))
        output = get_actions_that_support_wildcard_arns_only("all")
        # print(len(output))

    def test_get_actions_at_access_level_that_support_wildcard_arns_only(self):
        """querying.actions.get_actions_at_access_level_that_support_wildcard_arns_only"""
        read_output = get_actions_at_access_level_that_support_wildcard_arns_only(
            "secretsmanager", "Read"
        )
        list_output = get_actions_at_access_level_that_support_wildcard_arns_only(
            "secretsmanager", "List"
        )
        write_output = get_actions_at_access_level_that_support_wildcard_arns_only(
            "secretsmanager", "Write"
        )
        tagging_output = get_actions_at_access_level_that_support_wildcard_arns_only(
            "secretsmanager", "Tagging"
        )
        permissions_output = get_actions_at_access_level_that_support_wildcard_arns_only(
            "s3", "Permissions management"
        )
        # print(json.dumps(read_output, indent=4))
        # print(json.dumps(list_output, indent=4))
        # print(json.dumps(write_output, indent=4))
        # print(json.dumps(tagging_output, indent=4))
        # print(json.dumps(permissions_output, indent=4))
        self.assertListEqual(read_output, ['secretsmanager:GetRandomPassword'])
        self.assertListEqual(list_output, ['secretsmanager:ListSecrets'])
        self.assertListEqual(write_output, [])
        self.assertListEqual(tagging_output, [])
        self.assertListEqual(permissions_output, ["s3:PutAccountPublicAccessBlock"])

        all_permissions_output = get_actions_at_access_level_that_support_wildcard_arns_only(
            "all", "Permissions management"
        )
        all_write_output = get_actions_at_access_level_that_support_wildcard_arns_only(
            "all", "Write"
        )

        print(len(all_permissions_output) + len(all_write_output))
        # print(len(all_write_output))
        # print(json.dumps(all_write_output, indent=4))
        # print(json.dumps(all_permissions_output, indent=4))

    def test_get_actions_with_access_level(self):
        """querying.actions.get_actions_with_access_level"""
        desired_output = ['workspaces:CreateTags', 'workspaces:DeleteTags']
        output = get_actions_with_access_level(
            "workspaces", "Tagging"
        )
        self.maxDiff = None
        self.assertListEqual(desired_output, output)
        # output = get_actions_with_access_level(
        #     "all", "Tagging"
        # )
        # print(output)

    def test_get_actions_with_arn_type_and_access_level_case_1(self):
        """querying.actions.get_actions_with_arn_type_and_access_level"""
        desired_output = [
            's3:DeleteBucketPolicy',
            's3:PutBucketAcl',
            's3:PutBucketPolicy',
            's3:PutBucketPublicAccessBlock'
        ]
        output = get_actions_with_arn_type_and_access_level(
            # "ram", "resource-share", "Write"
            "s3", "bucket", "Permissions management"
        )
        self.maxDiff = None
        self.assertListEqual(desired_output, output)

    def test_get_actions_with_arn_type_and_access_level_case_2(self):
        """querying.actions.get_actions_with_arn_type_and_access_level with arn type"""
        desired_output = [
            'ssm:DeleteParameter',
            'ssm:DeleteParameters',
            'ssm:LabelParameterVersion',
            'ssm:PutParameter'
]
        output = get_actions_with_arn_type_and_access_level(
            "ssm", "parameter", "Write"
        )
        self.assertListEqual(desired_output, output)

    def test_get_actions_with_arn_type_and_access_level_case_3(self):
        """querying.actions.get_actions_with_arn_type_and_access_level with arn type"""
        desired_output = [
            's3:PutAccountPublicAccessBlock'
        ]
        output = get_actions_with_arn_type_and_access_level(
            # "ram", "resource-share", "Write"
            "s3", "*", "Permissions management"
        )
        self.assertListEqual(desired_output, output)

    def test_get_actions_with_arn_type_and_access_level_case_4(self):
        """querying.actions.get_actions_with_arn_type_and_access_level with arn type"""
        desired_output = [
            'secretsmanager:ListSecrets'
        ]
        output = get_actions_with_arn_type_and_access_level(
            "secretsmanager", "*", "List"
        )
        self.assertListEqual(desired_output, output)

    def test_get_actions_with_arn_type_and_access_level_case_5(self):
        """querying.actions.get_actions_with_arn_type_and_access_level with arn type"""

        output = get_actions_with_arn_type_and_access_level(
            "all", "object", "List"
        )

        self.assertTrue(len(output) == 2)

    def test_get_actions_matching_arn_type_case_1(self):
        """querying.actions.get_actions_matching_arn_type"""
        output = get_actions_matching_arn_type('ecr', '*')
        self.assertEqual(output, ["ecr:GetAuthorizationToken"])

    def test_get_actions_matching_arn_type_case_2(self):
        """querying.actions.get_actions_matching_arn_type"""
        output = get_actions_matching_arn_type('all', 'object')
        self.assertTrue('all:AbortMultipartUpload' in output)

    def test_get_actions_matching_arn_type_case_3(self):
        """querying.actions.get_actions_matching_arn_type"""
        output = get_actions_matching_arn_type('rds', 'object')
        self.assertTrue(len(output) == 0)

    def test_get_actions_matching_arn_type_case_4(self):
        """querying.actions.get_actions_matching_arn_type"""

        desired_output = [
            'codestar:CreateUserProfile',
            'codestar:DeleteUserProfile',
            'codestar:UpdateUserProfile'
        ]

        output = get_actions_matching_arn_type("codestar", "user")

        self.assertTrue(output, desired_output)

    def test_get_actions_matching_condition_key(self):
        """querying.actions.get_actions_matching_condition_key"""

        results = get_actions_matching_condition_key(
            "ses", "ses:FeedbackAddress"
        )
        desired_results = [
            'ses:SendBulkTemplatedEmail',
            'ses:SendCustomVerificationEmail',
            'ses:SendEmail',
            'ses:SendRawEmail',
            'ses:SendTemplatedEmail'
        ]
        # print(output)
        self.maxDiff = None
        print(results)
        self.assertListEqual(results, desired_results)

    # def test_get_actions_matching_condition_crud_and_arn(self):
    #     """querying.actions.get_actions_matching_condition_crud_and_arn"""
    #     results = get_actions_matching_condition_crud_and_arn(
    #         "elasticbeanstalk:InApplication",
    #         "List",
    #         "arn:${Partition}:elasticbeanstalk:${Region}:${Account}:environment/${ApplicationName}/${EnvironmentName}",
    #     )
    #     desired_results = [
    #         "elasticbeanstalk:DescribeEnvironments",
    #     ]
    #     print(results)
    #     self.assertListEqual(results, desired_results)
    #
    # def test_get_actions_matching_condition_crud_and_wildcard_arn(self):
    #     """querying.actions.get_actions_matching_condition_crud_and_wildcard_arn"""
    #     desired_results = [
    #         "swf:PollForActivityTask",
    #         "swf:PollForDecisionTask",
    #         "swf:RespondActivityTaskCompleted",
    #         "swf:StartWorkflowExecution",
    #     ]
    #     results = get_actions_matching_condition_crud_and_arn(
    #         "swf:taskList.name", "Write", "*"
    #     )
    #     print(results)
    #     self.assertListEqual(desired_results, results)
    #
    #     # This one leverages a condition key that is partway through a string in the database
    #     # - luckily, SQLAlchemy's ilike function allows us to find it anyway because it's a substring
    #     # kms:CallerAccount,kms:EncryptionAlgorithm,kms:EncryptionContextKeys,kms:ViaService
    #     desired_results = [
    #         "kms:Decrypt",
    #         "kms:Encrypt",
    #         "kms:GenerateDataKey",
    #         "kms:GenerateDataKeyPair",
    #         "kms:GenerateDataKeyPairWithoutPlaintext",
    #         "kms:GenerateDataKeyWithoutPlaintext",
    #         "kms:ReEncryptFrom",
    #         "kms:ReEncryptTo",
    #     ]
    #     print(results)
    #     results = get_actions_matching_condition_crud_and_arn(
    #         "kms:EncryptionAlgorithm", "Write", "*"
    #     )
    #     self.assertListEqual(desired_results, results)

    def test_remove_actions_not_matching_access_level(self):
        # TODO: This method normalized the access level unnecessarily. Make sure to change that in the final iteration
        """querying.actions.remove_actions_not_matching_access_level"""
        actions_list = [
            "ecr:batchgetimage",  # read
            "ecr:createrepository",  # write
            "ecr:describerepositories",  # list
            "ecr:tagresource",  # tagging
            "ecr:setrepositorypolicy",  # permissions management
        ]
        self.maxDiff = None
        # Read
        result = remove_actions_not_matching_access_level(
            actions_list, "Read"
        )
        self.assertListEqual(result, ["ecr:BatchGetImage"])
        # Write
        result = remove_actions_not_matching_access_level(
            actions_list, "Write"
        )

        self.assertListEqual(result, ["ecr:CreateRepository"])
        # List
        result = remove_actions_not_matching_access_level(
            actions_list, "List"
        )
        self.assertListEqual(result, ["ecr:DescribeRepositories"])
        # Tagging
        result = remove_actions_not_matching_access_level(
            actions_list, "Tagging"
        )
        self.assertListEqual(result, ["ecr:TagResource"])
        # Permissions management
        result = remove_actions_not_matching_access_level(
            actions_list, "Permissions management"
        )
        self.assertListEqual(result, ["ecr:SetRepositoryPolicy"])

        bad_actions_list = [
            "codecommit:CreatePullRequest",
            "codecommit:CreatePullRequestApprovalRule",
            "codecommit:CreateRepository",
            "codecommit:CreateUnreferencedMergeCommit",
            "codecommit:DeleteBranch",
            "codecommit:DeleteFile",
        ]

    def test_get_dependent_actions(self):
        """querying.actions.get_dependent_actions"""
        dependent_actions_single = ["ec2:associateiaminstanceprofile"]
        dependent_actions_double = ["shield:associatedrtlogbucket"]
        dependent_actions_several = ["chime:getcdrbucket"]
        self.assertEqual(
            get_dependent_actions(dependent_actions_single),
            ["iam:PassRole"],
        )
        self.assertEqual(
            get_dependent_actions(dependent_actions_double),
            ["s3:GetBucketPolicy", "s3:PutBucketPolicy"],
        )
        self.assertEqual(
            get_dependent_actions(dependent_actions_several),
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
            "secretsmanager:getrandompassword",
            "secretsmanager:listsecrets",
            # These ones are wildcard OR "secret"
            "secretsmanager:createsecret",
            "secretsmanager:putsecretvalue",
        ]
        desired_output = [
            # 2 wildcard only actions
            "secretsmanager:GetRandomPassword",
            "secretsmanager:ListSecrets",
        ]
        output = remove_actions_that_are_not_wildcard_arn_only(
            provided_actions_list
        )
        self.maxDiff = None
        self.assertListEqual(desired_output, output)


    def test_weird_lowercase_uppercase(self):
        """test_weird_lowercase_uppercase: Same as test_remove_actions_that_are_not_wildcard_arn_only, but with wEiRd cases"""
        provided_actions_list = [
            # 2 wildcard only actions
            "secretsmanager:gEtRaNdOmPasSwOrD",
            "secretsmanager:LIstsEcretS",
            # This one is wildcard OR "secret"
            "secretsmanager:cReAtEsEcReT",
            "secretsmanager:pUtSeCrEtVaLuE",
        ]
        desired_output = [
            # 2 wildcard only actions
            "secretsmanager:GetRandomPassword",
            "secretsmanager:ListSecrets",
        ]
        output = remove_actions_that_are_not_wildcard_arn_only(
            provided_actions_list
        )
        print(json.dumps(output))
        self.maxDiff = None
        self.assertListEqual(desired_output, output)

    def test_get_actions_matching_arn(self):
        """querying.actions.get_actions_matching_arn"""
        arn = "arn:aws:cloud9:us-east-1:account-id:environment:123456"
        results = get_actions_matching_arn(arn)
        # print(json.dumps(results, indent=4))
        # Don't want to keep an updated list of actions in these tests,
        # so let's just test the lengths and look for some contents that should or should not be in there.
        self.assertTrue(len(results) > 10)
        self.assertTrue("cloud9:ListEnvironments" not in results)
        self.assertTrue("cloud9:DeleteEnvironment" in results)

    def test_gh_226_elasticloadbalancing_v1_and_v2(self):
        """Test that elasticloadbalancing combines v1 and v2"""
        results = get_actions_for_service("elasticloadbalancing")
        # print(json.dumps(results, indent=4))
        lb_v1_only_action = "elasticloadbalancing:CreateTargetGroup"
        lb_v2_only_action = "elasticloadbalancing:SetSecurityGroups"
        self.assertTrue(lb_v1_only_action in results)
        self.assertTrue(lb_v2_only_action in results)

