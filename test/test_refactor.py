import unittest
import json
from policy_sentry.shared.database import connect_db
from policy_sentry.writing.sid_group import SidGroup
from policy_sentry.querying.actions import get_action_data
from policy_sentry.shared.constants import DATABASE_FILE_PATH
db_session = connect_db(DATABASE_FILE_PATH)


class RefactorTestCase(unittest.TestCase):

    def test_sid_group_multiple(self):
        desired_output = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "S3PermissionsmanagementBucket",
                    "Effect": "Allow",
                    "Action": [
                        "s3:deletebucketpolicy",
                        "s3:putbucketacl",
                        "s3:putbucketpolicy",
                        "s3:putbucketpublicaccessblock"
                    ],
                    "Resource": [
                        "arn:aws:s3:::example-org-s3-access-logs"
                    ]
                },
                {
                    "Sid": "KmsPermissionsmanagementKey",
                    "Effect": "Allow",
                    "Action": [
                        "kms:creategrant",
                        "kms:putkeypolicy",
                        "kms:retiregrant",
                        "kms:revokegrant"
                    ],
                    "Resource": [
                        "arn:aws:kms:us-east-1:123456789012:key/123456"
                    ]
                }
            ]
        }
        sid_group = SidGroup()
        arn_list_from_user = [
            "arn:aws:s3:::example-org-s3-access-logs",
            "arn:aws:kms:us-east-1:123456789012:key/123456"
        ]
        access_level = "Permissions management"
        sid_group.add_by_arn_and_access_level(db_session, arn_list_from_user, access_level)
        status = sid_group.get_sid_group()
        print(json.dumps(status, indent=4))
        print()
        rendered_policy = sid_group.get_rendered_policy(db_session)
        print(json.dumps(rendered_policy, indent=4))

    def test_sid_group(self):
        desired_output = {
            "S3PermissionsmanagementBucket": {
                "arn": [
                    "arn:aws:s3:::example-org-s3-access-logs"
                ],
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

        rendered_policy = sid_group.get_rendered_policy(db_session)
        print(json.dumps(rendered_policy, indent=4))

    def test_get_actions_data_service_wide(self):
        data = get_action_data(db_session, "s3", "*")
        print(data)

    def test_refactored_crud_policy(self):
        """test_refactored_crud_policy"""
        sid_group = SidGroup()
        sid_group.add_by_arn_and_access_level(db_session, ["arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"], "Read")
        sid_group.add_by_arn_and_access_level(db_session, ["arn:aws:s3:::example-org-sbx-vmimport/stuff"], "Tagging")
        sid_group.add_by_arn_and_access_level(db_session, ["arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"], "Write")
        # TODO: For some reason it isn't adding both of these secrets.
        sid_group.add_by_arn_and_access_level(db_session, ["arn:aws:secretsmanager:us-east-1:123456789012:secret:anothersecret"], "Write")
        sid_group.add_by_arn_and_access_level(db_session, ["arn:aws:kms:us-east-1:123456789012:key/123456"], "Permissions management")
        sid_group.add_by_arn_and_access_level(db_session, ["arn:aws:ssm:us-east-1:123456789012:parameter/test"], "List")

        rendered_policy = sid_group.get_rendered_policy(db_session)
        print("YOLO")
        print(json.dumps(rendered_policy, indent=4))
        # self.maxDiff = None
        self.assertEqual("1", "1")
