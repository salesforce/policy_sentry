import unittest
import os
import json
from policy_sentry.querying.arns import (
    get_arn_data,
    get_raw_arns_for_service,
    get_arn_types_for_service,
    get_arn_type_details,
    get_resource_type_name_with_raw_arn,
    get_matching_raw_arns
)


class QueryArnsTestCase(unittest.TestCase):
    def test_get_arn_data(self):
        results = get_arn_data("s3", "bucket")
        expected_results = [
            {
                "resource_type_name": "bucket",
                "raw_arn": "arn:${Partition}:s3:::${BucketName}",
                "condition_keys": []
            }
        ]
        # print(json.dumps(results, indent=4))
        self.assertListEqual(results, expected_results)

    def test_get_raw_arns_for_service(self):
        """querying.arns.get_raw_arns_for_service"""
        expected_results = [
            "arn:${Partition}:s3:${Region}:${Account}:accesspoint/${AccessPointName}",
            "arn:${Partition}:s3:::${BucketName}",
            "arn:${Partition}:s3:::${BucketName}/${ObjectName}",
            "arn:${Partition}:s3:${Region}:${Account}:job/${JobId}",
            "arn:${Partition}:s3:${Region}:${Account}:storage-lens/${ConfigId}"
        ]
        results = get_raw_arns_for_service("s3")
        self.maxDiff = None
        for expected_result in expected_results:
            self.assertTrue(expected_result in results)

    def test_get_arn_types_for_service(self):
        """querying.arns.get_arn_types_for_service: Tests function that grabs arn_type and raw_arn pairs"""
        expected_results = {
            "accesspoint": "arn:${Partition}:s3:${Region}:${Account}:accesspoint/${AccessPointName}",
            "bucket": "arn:${Partition}:s3:::${BucketName}",
            "object": "arn:${Partition}:s3:::${BucketName}/${ObjectName}",
            "job": "arn:${Partition}:s3:${Region}:${Account}:job/${JobId}",
        }
        results = get_arn_types_for_service("s3")
        self.maxDiff = None
        for expected_result in expected_results:
            self.assertTrue(expected_result in results)

    def test_get_arn_type_details(self):
        """querying.arns.get_arn_type_details: Tests function that grabs details about a specific ARN name"""
        expected_results = {
            "resource_type_name": "environment",
            "raw_arn": "arn:${Partition}:cloud9:${Region}:${Account}:environment:${ResourceId}",
            "condition_keys": ["aws:ResourceTag/${TagKey}"],
        }
        results = get_arn_type_details("cloud9", "environment")
        # print(json.dumps(results, indent=4))
        self.assertEqual(results, expected_results)

    def test_get_resource_type_name_with_raw_arn(self):
        """querying.arns.get_resource_type_name_with_raw_arn"""
        raw_arn = "arn:${Partition}:cloud9:${Region}:${Account}:environment:${ResourceId}"
        self.assertTrue(get_resource_type_name_with_raw_arn(raw_arn), "environment")

    def test_get_matching_raw_arn(self):
        """querying.arns.get_matching_raw_arns"""
        self.assertEqual(get_matching_raw_arns("arn:aws:s3:::bucket_name"), ["arn:${Partition}:s3:::${BucketName}"])
        self.assertEqual(get_matching_raw_arns("arn:aws:codecommit:us-east-1:123456789012:MyDemoRepo"), ["arn:${Partition}:codecommit:${Region}:${Account}:${RepositoryName}"])
        self.assertEqual(get_matching_raw_arns("arn:aws:ssm:us-east-1:123456789012:parameter/test"), ["arn:${Partition}:ssm:${Region}:${Account}:parameter/${ParameterNameWithoutLeadingSlash}"])
        self.assertEqual(get_matching_raw_arns("arn:aws:batch:region:account-id:job-definition/job-name:revision"), ["arn:${Partition}:batch:${Region}:${Account}:job-definition/${JobDefinitionName}:${Revision}"])
        self.assertEqual(get_matching_raw_arns("arn:aws:states:region:account-id:stateMachine:stateMachineName"), ["arn:${Partition}:states:${Region}:${Account}:stateMachine:${StateMachineName}", "arn:${Partition}:states:${Region}:${Account}:stateMachine:${StateMachineName}:${StateMachineVersionId}", "arn:${Partition}:states:${Region}:${Account}:stateMachine:${StateMachineName}:${StateMachineAliasName}"])
        self.assertEqual(get_matching_raw_arns("arn:aws:states:region:account-id:execution:stateMachineName:executionName"), ["arn:${Partition}:states:${Region}:${Account}:execution:${StateMachineName}:${ExecutionId}"])
        # self.assertEqual(get_matching_raw_arns("arn:aws:greengrass:region:account-id:/greengrass/definition/devices/1234567/versions/1"), ["arn:aws:greengrass:${Region}:${Account}:/greengrass/definition/devices/${DeviceDefinitionId}/versions/${VersionId}"])
        self.assertEqual(get_matching_raw_arns("arn:${Partition}:rds:region:account-id:db:mydatabase"), ["arn:${Partition}:rds:${Region}:${Account}:db:${DbInstanceName}"])
        self.assertIn("arn:${Partition}:rds:${Region}:${Account}:db:${DbInstanceName}", get_matching_raw_arns("arn:${Partition}:rds:region:account-id:*:*"))
        self.assertEqual(get_matching_raw_arns("arn:${Partition}:rds:region:account-id:invalid-resource:*"), [])
