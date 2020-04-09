import unittest
import os
import json
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
    remove_actions_that_are_not_wildcard_arn_only
)


class QueryActionsTestCase(unittest.TestCase):
    def test_get_service_prefix_data(self):
        result = get_service_prefix_data("cloud9")
        # print(json.dumps(result, indent=4))

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
        # print(json.dumps(results, indent=4))
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
            "secretsmanager:CreateSecret",
            "secretsmanager:GetRandomPassword",
            "secretsmanager:ListSecrets",
        ]
        output = get_actions_that_support_wildcard_arns_only("secretsmanager")
        self.maxDiff = None
        self.assertListEqual(desired_output, output)

    def test_get_actions_at_access_level_that_support_wildcard_arns_only(self):
        """querying.actions.get_actions_at_access_level_that_support_wildcard_arns_only"""
        read_output = get_actions_at_access_level_that_support_wildcard_arns_only(
            "secretsmanager", "Read"
        )
        list_output = get_actions_at_access_level_that_support_wildcard_arns_only(
            "secretsmanager", "List"
        )
        permissions_output = get_actions_at_access_level_that_support_wildcard_arns_only(
            "s3", "Permissions management"
        )
        self.assertListEqual(permissions_output, ["s3:PutAccountPublicAccessBlock"])
        self.assertListEqual(list_output, ['secretsmanager:ListSecrets'])
        self.assertListEqual(read_output, ['secretsmanager:GetRandomPassword'])

    def test_get_actions_with_access_level(self):
        """querying.actions.get_actions_with_access_level"""
        desired_output = ['workspaces:CreateTags', 'workspaces:DeleteTags']
        output = get_actions_with_access_level(
            "workspaces", "Tagging"
        )
        self.maxDiff = None
        self.assertListEqual(desired_output, output)

    def test_get_actions_with_arn_type_and_access_level(self):
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
            provided_actions_list
        )
        self.maxDiff = None
        self.assertListEqual(desired_output, output)


    def test_weird_lowercase_uppercase(self):
        """test_weird_lowercase_uppercase: Same as test_remove_actions_that_are_not_wildcard_arn_only, but with wEiRd cases"""
        provided_actions_list = [
            # 3 wildcard only actions
            "secretsmanager:cReAtEsEcReT",
            "secretsmanager:gEtRaNdOmPasSwOrD",
            "secretsmanager:LIstsEcretS",
            # This one is wildcard OR "secret"
            "secretsmanager:pUtSeCrEtVaLuE",
        ]
        desired_output = [
            # 3 wildcard only actions
            "secretsmanager:CreateSecret",
            "secretsmanager:GetRandomPassword",
            "secretsmanager:ListSecrets",
        ]
        output = remove_actions_that_are_not_wildcard_arn_only(
            provided_actions_list
        )
        self.maxDiff = None
        self.assertListEqual(desired_output, output)
