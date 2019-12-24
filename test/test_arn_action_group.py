import unittest
import logging
from policy_sentry.shared.database import connect_db
from policy_sentry.shared.policy import ArnActionGroup
from policy_sentry.shared.constants import DATABASE_FILE_PATH

db_session = connect_db(DATABASE_FILE_PATH)
logger = logging.getLogger('policy_sentry')


class ArnActionGroupTestCase(unittest.TestCase):
    def test_add_s3_permissions_management_arn(self):
        arn_action_group = ArnActionGroup()
        arn_list_from_user = ["arn:aws:s3:::example-org-s3-access-logs"]
        access_level = "Permissions management"
        desired_output = [
            {
                'arn': 'arn:aws:s3:::example-org-s3-access-logs',
                'service': 's3',
                'access_level': 'Permissions management',
                'arn_format': 'arn:${Partition}:s3:::${BucketName}',
                'actions': []
            }
        ]
        arn_action_group.add(db_session, arn_list_from_user, access_level)
        logger.debug(arn_action_group.get_arns())
        self.assertEqual(arn_action_group.get_arns(), desired_output)

    def test_update_actions_for_raw_arn_format(self):
        arn_action_group = ArnActionGroup()
        arn_list_from_user = ["arn:aws:s3:::example-org-s3-access-logs"]
        access_level = "Permissions management"
        desired_output = [
            {
                'arn': 'arn:aws:s3:::example-org-s3-access-logs',
                'service': 's3',
                'access_level': 'Permissions management',
                'arn_format': 'arn:${Partition}:s3:::${BucketName}',
                'actions': [
                    "s3:deletebucketpolicy",
                    "s3:putbucketacl",
                    "s3:putbucketpolicy",
                    "s3:putbucketpublicaccessblock"
                ]
            }
        ]
        arn_action_group.add(db_session, arn_list_from_user, access_level)
        arn_action_group.update_actions_for_raw_arn_format(db_session)
        logger.debug(arn_action_group.get_arns())
        self.assertEqual(arn_action_group.get_arns(), desired_output)

    def test_get_policy_elements(self):
        arn_action_group = ArnActionGroup()
        arn_list_from_user = ["arn:aws:s3:::example-org-s3-access-logs"]
        access_level = "Permissions management"
        desired_output = {
            'S3PermissionsmanagementBucket':
                {
                    'name': 'S3PermissionsmanagementBucket',
                    'actions': [
                        's3:deletebucketpolicy',
                        's3:putbucketacl',
                        's3:putbucketpolicy',
                        's3:putbucketpublicaccessblock'
                    ],
                    'arns': [
                        'arn:aws:s3:::example-org-s3-access-logs'
                    ]
                }
        }
        arn_action_group.add(db_session, arn_list_from_user, access_level)
        arn_action_group.update_actions_for_raw_arn_format(db_session)
        arn_dict = arn_action_group.get_policy_elements(db_session)
        logger.debug(arn_dict)
        self.assertEqual(arn_dict, desired_output)
