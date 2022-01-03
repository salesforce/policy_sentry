import unittest
import json
from policy_sentry.querying.conditions import (
    get_condition_keys_for_service,
    get_condition_key_details,
    get_condition_keys_available_to_raw_arn,
    get_conditions_for_action_and_raw_arn,
    get_condition_value_type
)


class QueryConditionsTestCase(unittest.TestCase):
    def test_get_condition_keys_for_service(self):
        """querying.conditions.get_condition_keys_for_service test"""
        expected_results = [
            "aws:RequestTag/${TagKey}",
            "aws:ResourceTag/${TagKey}",
            "aws:TagKeys",
            "ram:AllowsExternalPrincipals",
            "ram:PermissionArn",
            "ram:PermissionResourceType",
            "ram:Principal",
            "ram:RequestedAllowsExternalPrincipals",
            "ram:RequestedResourceType",
            "ram:ResourceArn",
            "ram:ResourceShareName",
            "ram:ShareOwnerAccountId"
        ]
        results = get_condition_keys_for_service("ram")
        for expected_result in expected_results:
            self.assertTrue(expected_result in results)
        print(results)
        # print(json.dumps(results, indent=4))
        # self.assertEqual(results, expected_results)

    def test_get_condition_keys_available_to_raw_arn(self):
        expected_results = [
            'aws:RequestTag/${TagKey}',
            'aws:ResourceTag/${TagKey}',
            'aws:TagKeys',
            'ec2:IsLaunchTemplateResource',
            'ec2:LaunchTemplate',
            'ec2:Region',
            'ec2:ResourceTag/${TagKey}',
            'ec2:Vpc'
        ]
        raw_arn = "arn:${Partition}:ec2:${Region}:${Account}:security-group/${SecurityGroupId}"
        result = get_condition_keys_available_to_raw_arn(raw_arn)
        print(result)
        self.assertListEqual(result, expected_results)

    def test_get_condition_key_details(self):
        """querying.conditions.get_condition_key_details"""
        desired_output = {
            "name": "cloud9:Permissions",
            "description": "Filters access by the type of AWS Cloud9 permissions",
            "condition_value_type": "string",
        }
        output = get_condition_key_details("cloud9", "cloud9:Permissions")
        self.assertEqual(desired_output, output)

    def test_get_conditions_for_action_and_raw_arn(self):
        """querying.conditions.get_conditions_for_action_and_raw_arn"""
        desired_condition_keys_list = [
            'aws:RequestTag/${TagKey}',
            'aws:ResourceTag/${TagKey}',
            'aws:TagKeys',
            'ec2:IsLaunchTemplateResource',
            'ec2:LaunchTemplate',
            'ec2:Region',
            'ec2:ResourceTag/${TagKey}',
            'ec2:Vpc'
        ]
        output = get_conditions_for_action_and_raw_arn(
            "ec2:AuthorizeSecurityGroupEgress",
            "arn:${Partition}:ec2:${Region}:${Account}:security-group/${SecurityGroupId}"
        )
        self.maxDiff = None
        # print(output)
        self.assertListEqual(desired_condition_keys_list, output)

    def test_get_condition_value_type(self):
        """querying.conditions.get_condition_value_type"""
        desired_result = "arn"
        condition_key = "secretsmanager:SecretId"
        result = get_condition_value_type(condition_key)
        self.maxDiff = None
        # print(result)
        self.assertEqual(desired_result, result)

    def test_gh_225_s3_conditions(self):
        """querying.actions.get_actions_matching_condition_key"""
        results = get_condition_keys_for_service("s3")
        # print(json.dumps(results, indent=4))
        expected_results = [
            "aws:RequestTag/${TagKey}",
            "aws:ResourceTag/${TagKey}",
            "aws:TagKeys",
            "s3:AccessPointNetworkOrigin",
            "s3:DataAccessPointAccount",
            "s3:DataAccessPointArn",
            "s3:ExistingJobOperation",
            "s3:ExistingJobPriority",
            "s3:ExistingObjectTag/<key>",
            "s3:JobSuspendedCause",
            "s3:LocationConstraint",
            "s3:RequestJobOperation",
            "s3:RequestJobPriority",
            "s3:RequestObjectTag/<key>",
            "s3:RequestObjectTagKeys",
            "s3:VersionId",
            "s3:authType",
            "s3:delimiter",
            "s3:locationconstraint",
            "s3:max-keys",
            "s3:object-lock-legal-hold",
            "s3:object-lock-mode",
            "s3:object-lock-remaining-retention-days",
            "s3:object-lock-retain-until-date",
            "s3:prefix",
            "s3:signatureAge",
            "s3:signatureversion",
            "s3:versionid",
            "s3:x-amz-acl",
            "s3:x-amz-content-sha256",
            "s3:x-amz-copy-source",
            "s3:x-amz-grant-full-control",
            "s3:x-amz-grant-read",
            "s3:x-amz-grant-read-acp",
            "s3:x-amz-grant-write",
            "s3:x-amz-grant-write-acp",
            "s3:x-amz-metadata-directive",
            "s3:x-amz-server-side-encryption",
            "s3:x-amz-server-side-encryption-aws-kms-key-id",
            "s3:x-amz-storage-class",
            "s3:x-amz-website-redirect-location"
        ]
        for expected_result in expected_results:
            self.assertTrue(expected_result in results)
        # self.assertListEqual(results, expected_results)
