import unittest
from policy_sentry.querying.arns import get_raw_arns_for_service, get_arn_type_details, \
    get_arn_types_for_service
from policy_sentry.shared.constants import DATABASE_FILE_PATH
from policy_sentry.shared.database import connect_db
db_session = connect_db(DATABASE_FILE_PATH)


class QueryArnsTestCase(unittest.TestCase):
    def test_get_raw_arns_for_service(self):
        """querying.arns.get_raw_arns_for_service"""
        desired_output = [
            "arn:${Partition}:s3:${Region}:${Account}:accesspoint/${AccessPointName}",
            "arn:${Partition}:s3:::${BucketName}",
            "arn:${Partition}:s3:::${BucketName}/${ObjectName}",
            "arn:${Partition}:s3:${Region}:${Account}:job/${JobId}"
        ]
        output = get_raw_arns_for_service(db_session, "s3")
        self.maxDiff = None
        self.assertListEqual(desired_output, output)

    def test_get_arn_types_for_service(self):
        """querying.arns.get_arn_types_for_service: Tests function that grabs arn_type and raw_arn pairs"""
        desired_output = {
            "accesspoint": "arn:${Partition}:s3:${Region}:${Account}:accesspoint/${AccessPointName}",
            "bucket": "arn:${Partition}:s3:::${BucketName}",
            "object": "arn:${Partition}:s3:::${BucketName}/${ObjectName}",
            "job": "arn:${Partition}:s3:${Region}:${Account}:job/${JobId}",
        }
        output = get_arn_types_for_service(db_session, "s3")
        # print(output)
        self.maxDiff = None
        self.assertDictEqual(desired_output, output)

    def test_get_arn_type_details(self):
        """querying.arns.get_arn_type_details: Tests function that grabs details about a specific ARN name"""
        desired_output = {
            "resource_type_name": "environment",
            "raw_arn": "arn:${Partition}:cloud9:${Region}:${Account}:environment:${ResourceId}",
            "condition_keys": None
        }
        output = get_arn_type_details(db_session, "cloud9", "environment")
        self.assertEqual(desired_output, output)
