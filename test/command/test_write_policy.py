import unittest
import json
from os.path import abspath, pardir, dirname, join
from policy_sentry.shared.constants import DATABASE_FILE_PATH
from policy_sentry.shared.database import connect_db
from policy_sentry.command.write_policy import write_policy_with_template
from policy_sentry.util.file import read_yaml_file

db_session = connect_db(DATABASE_FILE_PATH)


class WritePolicyPreventWildcardEscalation(unittest.TestCase):
    def test_wildcard_when_not_necessary(self):
        """test_wildcard_when_not_necessary: Attempts bypass of CRUD mode wildcard-only"""
        cfg = {
            "mode": "crud",
            "name": "RoleNameWithCRUD",
            "permissions-management": ["arn:aws:s3:::example-org-s3-access-logs"],
            "wildcard-only": {
                "single-actions": [
                    # The first three are legitimately wildcard only.
                    # Verify with `policy_sentry query action-table --service secretsmanager --wildcard-only`
                    "ram:EnableSharingWithAwsOrganization",
                    "ram:GetResourcePolicies",
                    "secretsmanager:CreateSecret",
                    # This last one can be "secret" ARN type OR wildcard. We want to prevent people from
                    # bypassing this mechanism, while allowing them to explicitly
                    # request specific privs that require wildcard mode. This next value -
                    # secretsmanager:putsecretvalue - is an example of someone trying to beat the tool.
                    "secretsmanager:PutSecretValue",
                ],
            }
        }
        db_session = connect_db("bundled")
        output = write_policy_with_template(db_session, cfg)
        # print(json.dumps(output, indent=4))
        desired_output = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "MultMultNone",
                    "Effect": "Allow",
                    "Action": [
                        "ram:EnableSharingWithAwsOrganization",
                        "ram:GetResourcePolicies",
                        "secretsmanager:CreateSecret",
                    ],
                    "Resource": ["*"],
                },
                {
                    "Sid": "S3PermissionsmanagementBucket",
                    "Effect": "Allow",
                    "Action": [
                        "s3:DeleteBucketPolicy",
                        "s3:PutBucketAcl",
                        "s3:PutBucketPolicy",
                        "s3:PutBucketPublicAccessBlock",
                    ],
                    "Resource": ["arn:aws:s3:::example-org-s3-access-logs"],
                },
            ],
        }
        self.maxDiff = None
        print(output)
        self.assertDictEqual(desired_output, output)


# class TaggingTestCase(unittest.TestCase):
#     def test_write_tagging_only_policy(self):
#         """test_write_tagging_only_policy: We'd never write a policy like this IRL but doing this as a quality check against how it handles the database"""
#         policy_file_path = abspath(
#             join(
#                 dirname(__file__), pardir + "/" + pardir + "/examples/yml/tagging.yml",
#             )
#         )
#         cfg = read_yaml_file(policy_file_path)
#
#         policy = write_policy_with_template(db_session, cfg)
#         print(policy)

class WildcardOnlyServiceLevelTestCase(unittest.TestCase):
    def test_add_wildcard_only_actions_matching_services_and_access_level(self):
        """test_add_wildcard_only_actions_matching_services_and_access_level: We'd never write a policy like this
        IRL but doing this as a quality check against how it handles the database """
        policy_file_path = abspath(
            join(
                dirname(__file__), pardir + "/" + pardir + "/examples/yml/crud-with-wildcard-service-level.yml",
            )
        )
        cfg = read_yaml_file(policy_file_path)

        output = write_policy_with_template(db_session, cfg)
        print(json.dumps(output, indent=4))
        desired_output = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "MultMultNone",
                    "Effect": "Allow",
                    "Action": [
                        "ecr:GetAuthorizationToken",
                        "s3:GetAccessPoint",
                        "s3:GetAccountPublicAccessBlock",
                        "s3:ListAccessPoints"
                    ],
                    "Resource": [
                        "*"
                    ]
                },
                {
                    "Sid": "S3PermissionsmanagementBucket",
                    "Effect": "Allow",
                    "Action": [
                        "s3:DeleteBucketPolicy",
                        "s3:PutBucketAcl",
                        "s3:PutBucketPolicy",
                        "s3:PutBucketPublicAccessBlock"
                    ],
                    "Resource": [
                        "arn:aws:s3:::example-org-s3-access-logs"
                    ]
                }
            ]
        }
        self.assertDictEqual(output, desired_output)


class RdsWritingTestCase(unittest.TestCase):
    def test_rds_policy_read_only(self):
        """test_rds_policy_read_only: Make sure that the RDS Policies work properly"""
        policy_file_path = abspath(
            join(
                dirname(__file__), pardir + "/" + pardir + "/examples/yml/crud-rds-read.yml",
            )
        )
        cfg = read_yaml_file(policy_file_path)
        desired_output = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "RdsReadDb",
                    "Effect": "Allow",
                    "Action": [
                        "rds:DownloadDBLogFilePortion",
                        "rds:ListTagsForResource"
                    ],
                    "Resource": [
                        "arn:aws:rds:us-east-1:123456789012:db:mydatabase"
                    ]
                }
            ]
        }
        policy = write_policy_with_template(db_session, cfg)
        print(json.dumps(policy, indent=4))
        self.assertDictEqual(desired_output, policy)

    def test_rds_policy_read_write_list(self):
        """test_rds_policy_read_write_list: Make sure that the RDS Policies work properly for multiple levels"""
        policy_file_path = abspath(
            join(
                dirname(__file__), pardir + "/" + pardir + "/examples/yml/crud-rds-mult.yml",
            )
        )
        cfg = read_yaml_file(policy_file_path)
        desired_output = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "RdsReadDb",
                    "Effect": "Allow",
                    "Action": [
                        "rds:DownloadDBLogFilePortion",
                        "rds:ListTagsForResource"
                    ],
                    "Resource": [
                        "arn:aws:rds:us-east-1:123456789012:db:mydatabase"
                    ]
                },
                {
                    "Sid": "MultMultNone",
                    "Effect": "Allow",
                    "Action": [
                        "iam:PassRole"
                    ],
                    "Resource": [
                        "*"
                    ]
                },
                {
                    "Sid": "RdsWriteDb",
                    "Effect": "Allow",
                    "Action": [
                        "rds:AddRoleToDBInstance",
                        "rds:ApplyPendingMaintenanceAction",
                        "rds:CreateDBInstance",
                        "rds:CreateDBInstanceReadReplica",
                        "rds:CreateDBSnapshot",
                        "rds:DeleteDBInstance",
                        "rds:DeregisterDBProxyTargets",
                        "rds:ModifyDBInstance",
                        "rds:PromoteReadReplica",
                        "rds:RebootDBInstance",
                        "rds:RemoveRoleFromDBInstance",
                        "rds:RestoreDBInstanceFromDBSnapshot",
                        "rds:RestoreDBInstanceFromS3",
                        "rds:RestoreDBInstanceToPointInTime",
                        "rds:StartDBInstance",
                        "rds:StopDBInstance"
                    ],
                    "Resource": [
                        "arn:aws:rds:us-east-1:123456789012:db:mydatabase"
                    ]
                },
                {
                    "Sid": "RdsListDb",
                    "Effect": "Allow",
                    "Action": [
                        "rds:DescribeDBLogFiles",
                        "rds:DescribeDBProxyTargets",
                        "rds:DescribeDBSnapshots",
                        "rds:DescribePendingMaintenanceActions",
                        "rds:DescribeValidDBInstanceModifications"
                    ],
                    "Resource": [
                        "arn:aws:rds:us-east-1:123456789012:db:mydatabase"
                    ]
                }
            ]
        }
        policy = write_policy_with_template(db_session, cfg)
        print(json.dumps(policy, indent=4))
        self.assertDictEqual(desired_output, policy)
