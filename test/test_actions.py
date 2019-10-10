import unittest
from pathlib import Path
from policy_sentry.shared.actions import get_dependent_actions, get_actions_by_access_level
from policy_sentry.shared.database import connect_db

home = str(Path.home())
config_directory = '/.policy_sentry/'
database_file_name = 'aws.sqlite3'
database_path = home + config_directory + database_file_name
db_session = connect_db(database_path)

dependent_actions_single = ["ec2:associateiaminstanceprofile"]
dependent_actions_double = ["shield:associatedrtlogbucket"]
dependent_actions_several = ["chime:getcdrbucket"]


class ActionsTestCase(unittest.TestCase):

    def test_get_dependent_actions_single(self):
        self.assertEqual(get_dependent_actions(db_session, dependent_actions_single), ["ec2:associateiaminstanceprofile", "iam:passrole"])

    def test_get_dependent_actions_double(self):
        self.assertEqual(get_dependent_actions(db_session, dependent_actions_double), ["shield:associatedrtlogbucket", "s3:getbucketpolicy", "s3:putbucketpolicy"])

    def test_get_dependent_actions_several(self):
        self.assertEqual(get_dependent_actions(db_session, dependent_actions_several), ["chime:getcdrbucket", "s3:getbucketacl", "s3:getbucketlocation", "s3:getbucketlogging", "s3:getbucketversioning", "s3:getbucketwebsite"])

    def test_get_actions_by_access_level(self):
        actions_list = [
            "ecr:BatchGetImage",  # Read
            "ecr:CreateRepository",  # Write
            "ecr:DescribeRepositories",  # List
            "ecr:TagResource",  # Tagging
            "ecr:SetRepositoryPolicy",  # Permissions management
        ]
        print("Read")
        # Read
        self.assertListEqual(get_actions_by_access_level(db_session, actions_list, "read"), ["ecr:batchgetimage"])
        # Write
        self.assertListEqual(get_actions_by_access_level(db_session, actions_list, "write"), ["ecr:createrepository"])
        # List
        self.assertListEqual(get_actions_by_access_level(db_session, actions_list, "list"), ["ecr:describerepositories"])
        # Tagging
        self.assertListEqual(get_actions_by_access_level(db_session, actions_list, "tagging"), ["ecr:tagresource"])
        # Permissions management
        self.assertListEqual(get_actions_by_access_level(db_session, actions_list, "permissions-management"), ["ecr:setrepositorypolicy"])
