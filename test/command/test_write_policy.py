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
            "description": "Why I need these privs",
            "role_arn": "arn:aws:iam::123456789012:role/RiskyEC2",
            "permissions-management": ["arn:aws:s3:::example-org-s3-access-logs"],
            "wildcard": [
                # The first three are legitimately wildcard only.
                # Verify with `policy_sentry query action-table --service secretsmanager --wildcard-only`
                "ram:enablesharingwithawsorganization",
                "ram:getresourcepolicies",
                "secretsmanager:createsecret",
                # This last one can be "secret" ARN type OR wildcard. We want to prevent people from
                # bypassing this mechanism, while allowing them to explicitly
                # request specific privs that require wildcard mode. This next value -
                # secretsmanager:putsecretvalue - is an example of someone trying to beat the tool.
                "secretsmanager:putsecretvalue",
            ],
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
                        "ram:enablesharingwithawsorganization",
                        "ram:getresourcepolicies",
                        "secretsmanager:createsecret",
                    ],
                    "Resource": ["*"],
                },
                {
                    "Sid": "S3PermissionsmanagementBucket",
                    "Effect": "Allow",
                    "Action": [
                        "s3:deletebucketpolicy",
                        "s3:putbucketacl",
                        "s3:putbucketpolicy",
                        "s3:putbucketpublicaccessblock",
                    ],
                    "Resource": ["arn:aws:s3:::example-org-s3-access-logs"],
                },
            ],
        }
        self.maxDiff = None
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


