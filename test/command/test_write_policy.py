import unittest
import json
import os
from policy_sentry.command.write_policy import write_policy_with_template
from policy_sentry.util.file import read_yaml_file
from policy_sentry.util.policy_files import (
    get_sid_names_from_policy,
    get_statement_from_policy_using_sid,
)


# class WritePolicyPreventWildcardEscalation(unittest.TestCase):
#     def test_wildcard_when_not_necessary(self):
#         """test_wildcard_when_not_necessary: Attempts bypass of CRUD mode wildcard-only"""
#         cfg = {
#             "mode": "crud",
#             "name": "RoleNameWithCRUD",
#             "permissions-management": ["arn:aws:s3:::example-org-s3-access-logs"],
#             "wildcard-only": {
#                 "single-actions": [
#                     # The first three are legitimately wildcard only.
#                     # Verify with `policy_sentry query action-table --service secretsmanager --wildcard-only`
#                     "ram:EnableSharingWithAwsOrganization",
#                     "ram:GetResourcePolicies",
#                     "secretsmanager:CreateSecret",
#                     # This last one can be "secret" ARN type OR wildcard. We want to prevent people from
#                     # bypassing this mechanism, while allowing them to explicitly
#                     # request specific privs that require wildcard mode. This next value -
#                     # secretsmanager:putsecretvalue - is an example of someone trying to beat the tool.
#                     "secretsmanager:PutSecretValue",
#                 ],
#             }
#         }
#         output = write_policy_with_template(cfg)
#         # print(json.dumps(output, indent=4))
#         desired_output = {
#             "Version": "2012-10-17",
#             "Statement": [
#                 {
#                     "Sid": "MultMultNone",
#                     "Effect": "Allow",
#                     "Action": [
#                         "ram:EnableSharingWithAwsOrganization",
#                         "ram:GetResourcePolicies",
#                     ],
#                     "Resource": ["*"],
#                 },
#                 {
#                     "Sid": "S3PermissionsmanagementBucket",
#                     "Effect": "Allow",
#                     "Action": [
#                         "s3:DeleteBucketPolicy",
#                         "s3:PutBucketAcl",
#                         "s3:PutBucketPolicy",
#                         "s3:PutBucketPublicAccessBlock",
#                     ],
#                     "Resource": ["arn:aws:s3:::example-org-s3-access-logs"],
#                 },
#             ],
#         }
#         self.maxDiff = None
#         print(output)
#         self.assertDictEqual(desired_output, output)


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
#         policy = write_policy_with_template(cfg)
#         print(policy)


class WildcardOnlyServiceLevelTestCase(unittest.TestCase):
    def test_add_wildcard_only_actions_matching_services_and_access_level(self):
        """test_add_wildcard_only_actions_matching_services_and_access_level: We'd never write a policy like this
        IRL but doing this as a quality check against how it handles the database"""
        policy_file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.path.pardir,
                os.path.pardir,
                "examples",
                "yml",
                "crud-with-wildcard-service-level.yml",
            )
        )
        cfg = read_yaml_file(policy_file_path)

        results = write_policy_with_template(cfg)

        # The Policy *should* look like this.

        # desired_output = {
        #     "Version": "2012-10-17",
        #     "Statement": [
        #         {
        #             "Sid": "MultMultNone",
        #             "Effect": "Allow",
        #             "Action": [
        #                 "ram:EnableSharingWithAwsOrganization",
        #                 "ram:GetResourcePolicies",
        #                 "ecr:GetAuthorizationToken",
        #                 "s3:GetAccessPoint",
        #                 "s3:GetAccountPublicAccessBlock",
        #                 "s3:ListAccessPoints",
        #                 "s3:ListJobs"
        #             ],
        #             "Resource": [
        #                 "*"
        #             ]
        #         },
        #         {
        #             "Sid": "S3PermissionsmanagementBucket",
        #             "Effect": "Allow",
        #             "Action": [
        #                 "s3:DeleteBucketPolicy",
        #                 "s3:PutBucketAcl",
        #                 "s3:PutBucketPolicy",
        #                 "s3:PutBucketPublicAccessBlock"
        #             ],
        #             "Resource": [
        #                 "arn:aws:s3:::example-org-s3-access-logs"
        #             ]
        #         }
        #     ]
        # }

        print(json.dumps(results, indent=4))
        self.maxDiff = None

        # To future-proof this unit test...
        # (1) check the Sid names
        sid_names = get_sid_names_from_policy(results)
        self.assertIn(
            "MultMultNone",
            sid_names,
            "Sid is not in the list of expected Statement Ids",
        )
        self.assertIn(
            "S3PermissionsmanagementBucket",
            sid_names,
            "Sid is not in the list of expected Statement Ids",
        )

        # (2) Check for the presence of certain actions that we know will be there
        statement_1 = get_statement_from_policy_using_sid(results, "MultMultNone")
        self.assertIn("ram:EnableSharingWithAwsOrganization", statement_1.get("Action"))
        self.assertIn("s3:GetAccountPublicAccessBlock", statement_1.get("Action"))

        statement_2 = get_statement_from_policy_using_sid(results, "S3PermissionsmanagementBucket")
        self.assertIn("s3:DeleteBucketPolicy", statement_2.get("Action"))
        self.assertIn("s3:PutBucketPolicy", statement_2.get("Action"))

        # (3) Check that the length of the list is at least the length that it is right now,
        # since we expect it to grow eventually
        self.assertTrue(len(statement_1.get("Action")) > 5)  # Size is 6 at time of writing
        self.assertTrue(len(statement_2.get("Action")) > 3)  # Size is 4 at time of writing

    def test_eks_gh_155(self):
        """test_eks_gh_155: Test EKS issue raised in GH-155"""
        template_file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.path.pardir,
                "files",
                "eks-service-wide.yml",
            )
        )
        cfg = read_yaml_file(template_file_path)
        result = write_policy_with_template(cfg)
        print(json.dumps(result, indent=4))
        expected_results = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "MultMultNone",
                    "Effect": "Allow",
                    "Action": [
                        "eks:ListClusters",
                        "eks:CreateCluster",
                        "eks:RegisterCluster",
                    ],
                    "Resource": ["*"],
                }
            ],
        }
        self.assertEqual(result["Statement"][0]["Sid"], expected_results["Statement"][0]["Sid"])
        self.assertTrue("eks:ListClusters" in result["Statement"][0]["Action"])
        self.assertTrue("eks:CreateCluster" in result["Statement"][0]["Action"])
        self.assertTrue("eks:RegisterCluster" in result["Statement"][0]["Action"])

    def test_dynamodb_arn_policy_gh_215(self):
        """test_dynamodb_arn_matching_gh_215: Test writing a policy with DynamoDB"""
        template_file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.path.pardir,
                "files",
                "dynamodb_gh_215.yml",
            )
        )
        cfg = read_yaml_file(template_file_path)
        results = write_policy_with_template(cfg)
        print(json.dumps(results, indent=4))
        expected_statement_ids = [
            "MultMultNone",
            "DynamodbReadTable",
            "DynamodbWriteTable",
        ]
        for statement in results.get("Statement"):
            self.assertTrue(statement.get("Sid") in expected_statement_ids)


class RdsWritingTestCase(unittest.TestCase):
    def test_rds_policy_read_only(self):
        """test_rds_policy_read_only: Make sure that the RDS Policies work properly"""
        policy_file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.path.pardir,
                os.path.pardir,
                "examples",
                "yml",
                "crud-rds-read.yml",
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
                        "rds:DownloadCompleteDBLogFile",
                        "rds:DownloadDBLogFilePortion",
                        "rds:ListTagsForResource",
                    ],
                    "Resource": ["arn:aws:rds:us-east-1:123456789012:db:mydatabase"],
                }
            ],
        }
        expected_actions = [
            "rds:DownloadCompleteDBLogFile",
            "rds:DownloadDBLogFilePortion",
            "rds:ListTagsForResource",
        ]
        output = write_policy_with_template(cfg)
        print(json.dumps(output, indent=4))
        expected_statement_ids = ["RdsReadDb"]
        for statement in output.get("Statement"):
            self.assertTrue(statement.get("Sid") in expected_statement_ids)
        for action in expected_actions:
            self.assertTrue(action in output["Statement"][0]["Action"])

    def test_rds_policy_read_write_list(self):
        """test_rds_policy_read_write_list: Make sure that the RDS Policies work properly for multiple levels"""
        policy_file_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.path.pardir,
                os.path.pardir,
                "examples",
                "yml",
                "crud-rds-mult.yml",
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
                        "rds:ListTagsForResource",
                    ],
                    "Resource": ["arn:aws:rds:us-east-1:123456789012:db:mydatabase"],
                },
                {
                    "Sid": "MultMultNone",
                    "Effect": "Allow",
                    "Action": ["iam:PassRole"],
                    "Resource": ["*"],
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
                        "rds:StopDBInstance",
                    ],
                    "Resource": ["arn:aws:rds:us-east-1:123456789012:db:mydatabase"],
                },
                {
                    "Sid": "RdsListDb",
                    "Effect": "Allow",
                    "Action": [
                        "rds:DescribeDBLogFiles",
                        "rds:DescribeDBProxyTargets",
                        "rds:DescribeDBSnapshots",
                        "rds:DescribePendingMaintenanceActions",
                        "rds:DescribeValidDBInstanceModifications",
                    ],
                    "Resource": ["arn:aws:rds:us-east-1:123456789012:db:mydatabase"],
                },
            ],
        }
        expected_statement_ids = [
            "RdsReadDb",
            "MultMultNone",
            "RdsWriteDb",
            "RdsListDb",
        ]
        policy = write_policy_with_template(cfg)
        for statement in policy.get("Statement"):
            self.assertTrue(statement.get("Sid") in expected_statement_ids)
        # print(json.dumps(policy, indent=4))
        # self.assertDictEqual(desired_output, policy)
