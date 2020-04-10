import unittest
import os
import json
from policy_sentry.querying.arns import (
    get_arn_data,
    get_raw_arns_for_service,
    get_arn_types_for_service,
    get_arn_type_details,
    get_resource_type_name_with_raw_arn
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
        desired_output = [
            "arn:${Partition}:s3:${Region}:${Account}:accesspoint/${AccessPointName}",
            "arn:${Partition}:s3:::${BucketName}",
            "arn:${Partition}:s3:::${BucketName}/${ObjectName}",
            "arn:${Partition}:s3:${Region}:${Account}:job/${JobId}",
        ]
        output = get_raw_arns_for_service("s3")
        self.maxDiff = None
        self.assertListEqual(output, desired_output)

    def test_get_arn_types_for_service(self):
        """querying.arns.get_arn_types_for_service: Tests function that grabs arn_type and raw_arn pairs"""
        expected_results = {
            "accesspoint": "arn:${Partition}:s3:${Region}:${Account}:accesspoint/${AccessPointName}",
            "bucket": "arn:${Partition}:s3:::${BucketName}",
            "object": "arn:${Partition}:s3:::${BucketName}/${ObjectName}",
            "job": "arn:${Partition}:s3:${Region}:${Account}:job/${JobId}",
        }
        results = get_arn_types_for_service("s3")
        # print(json.dumps(results, indent=4))
        self.maxDiff = None
        self.assertEqual(results, expected_results)


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
