import unittest
import json
from policy_sentry.shared.database import connect_db
from policy_sentry.writing.sid_group import SidGroup
from policy_sentry.querying.actions import get_action_data
from policy_sentry.shared.constants import DATABASE_FILE_PATH
db_session = connect_db(DATABASE_FILE_PATH)


data_example = {
    "s3": [
        {'action': 's3:abortmultipartupload', 'description': 'Aborts a multipart upload.', 'access_level': 'Write', 'resource_arn_format': '*', 'condition_keys': ['s3:DataAccessPointArn', 's3:DataAccessPointAccount', 's3:AccessPointNetworkOrigin', 's3:authtype', 's3:signatureage', 's3:signatureversion', 's3:x-amz-content-sha256'], 'dependent_actions': None}
    ]
}



class RefactorTestCase(unittest.TestCase):
    def test_sid_group(self):
        desired_output = {
            "S3PermissionsmanagementBucket": {
                "arn": "arn:aws:s3:::example-org-s3-access-logs",
                "service": "s3",
                "access_level": "Permissions management",
                "arn_format": "arn:${Partition}:s3:::${BucketName}",
                "actions": [
                    "s3:deletebucketpolicy",
                    "s3:putbucketacl",
                    "s3:putbucketpolicy",
                    "s3:putbucketpublicaccessblock"
                ]
            }
        }
        sid_group = SidGroup()
        arn_list_from_user = ["arn:aws:s3:::example-org-s3-access-logs"]
        access_level = "Permissions management"
        sid_group.add_by_arn_and_access_level(db_session, arn_list_from_user, access_level)
        status = sid_group.get_sid_group()
        print(json.dumps(status, indent=4))
        self.assertEqual(status, desired_output)

    def test_get_actions_data_service_wide(self):
        data = get_action_data(db_session, "s3", "*")
        print(data)
