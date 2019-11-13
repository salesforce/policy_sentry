import unittest
import json
from pathlib import Path
from policy_sentry.shared.database import connect_db
from policy_sentry.shared.policy import ArnActionGroup
from policy_sentry.command.write_policy import print_policy
from policy_sentry.shared.actions import get_dependent_actions

home = str(Path.home())
config_directory = '/.policy_sentry/'
database_file_name = 'aws.sqlite3'
database_path = home + config_directory + database_file_name
db_session = connect_db(database_path)


class WritePolicyCrudTestCase(unittest.TestCase):

    def test_write_policy(self):
        arn_action_group = ArnActionGroup()
        arn_list_from_user = ["arn:aws:s3:::example-org-s3-access-logs"]
        access_level = "Permissions management"
        desired_output = {
            'Version': '2012-10-17',
            'Statement': [
                {
                    'Sid': 'S3PermissionsmanagementBucket',
                    'Effect': 'Allow',
                    'Action': [
                        's3:deletebucketpolicy',
                        's3:putbucketacl',
                        's3:putbucketpolicy',
                        's3:putbucketpublicaccessblock'
                    ],
                    'Resource': [
                        'arn:aws:s3:::example-org-s3-access-logs'
                    ]
                }
            ]
        }
        arn_action_group.add(db_session, arn_list_from_user, access_level)
        arn_action_group.update_actions_for_raw_arn_format(db_session)
        arn_dict = arn_action_group.get_policy_elements(db_session)
        policy = print_policy(arn_dict, db_session)
        # print(policy)
        self.assertEqual(policy, desired_output)


actions_test_data_1 = ['kms:CreateCustomKeyStore', 'kms:CreateGrant']
actions_test_data_2 = ['ec2:AuthorizeSecurityGroupEgress', 'ec2:AuthorizeSecurityGroupIngress']


class WritePolicyActionsTestCase(unittest.TestCase):

    def test_print_policy_with_actions_having_dependencies(self):
        desired_output = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "KmsPermissionsmanagementKey",
                        "Effect": "Allow",
                        "Action": [
                            "kms:creategrant"
                        ],
                        "Resource": [
                            "arn:aws:kms:${Region}:${Account}:key/${KeyId}"
                        ]
                    },
                    {
                        "Sid": "MultMultNone",
                        "Effect": "Allow",
                        "Action": [
                            "kms:createcustomkeystore",
                            "cloudhsm:describeclusters"
                        ],
                        "Resource": [
                            "*"
                        ]
                    }
                ]
            }
        supplied_actions = actions_test_data_1
        supplied_actions = get_dependent_actions(db_session, supplied_actions)
        arn_action_group = ArnActionGroup()
        arn_dict = arn_action_group.process_list_of_actions(supplied_actions, db_session)
        self.maxDiff = None
        policy = print_policy(arn_dict, db_session)
        self.assertDictEqual(policy, desired_output)


class WritePolicyPreventWildcardEscalation(unittest.TestCase):
    def test_wildcard_when_not_necessary(self):
        cfg = {
            'roles_with_crud_levels': [
                {
                    'name': 'RoleNameWithCRUD',
                    'description': 'Why I need these privs',
                    'arn': 'arn:aws:iam::123456789012:role/RiskyEC2',
                    'permissions-management': [
                        'arn:aws:s3:::example-org-s3-access-logs'
                    ],
                    'wildcard': [
                        'secretsmanager:deletesecret',
                        'secretsmanager:getsecretvalue',
                        'ram:enablesharingwithawsorganization',
                        'ram:getresourcepolicies'
                    ]
                }
            ]
        }
        arn_action_group = ArnActionGroup()

        arn_dict = arn_action_group.process_resource_specific_acls(cfg, db_session)
        output = print_policy(arn_dict, db_session, None)
        print(json.dumps(output, indent=4))
        desired_output = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "MultMultNone",
                    "Effect": "Allow",
                    "Action": [
                        "ram:enablesharingwithawsorganization",
                        "ram:getresourcepolicies"
                    ],
                    "Resource": [
                        "*"
                    ]
                },
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
                }
            ]
        }
        self.maxDiff = None
        # self.assertDictEqual(output, desired_output)
