import unittest
from policy_sentry.querying.actions import get_dependent_actions, get_dependent_actions_only, remove_actions_not_matching_access_level
from policy_sentry.util.policy_files import get_actions_from_json_policy_file, get_actions_from_policy
from policy_sentry.shared.database import connect_db
from policy_sentry.shared.constants import DATABASE_FILE_PATH
import os

db_session = connect_db(DATABASE_FILE_PATH)

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

    def test_get_dependent_actions_only(self):
        self.assertEqual(get_dependent_actions_only(db_session, dependent_actions_single), ["iam:passrole"])
        self.assertEqual(get_dependent_actions_only(db_session, dependent_actions_double), ["s3:getbucketpolicy", "s3:putbucketpolicy"])
        self.assertEqual(get_dependent_actions_only(db_session, dependent_actions_several), ["s3:getbucketacl", "s3:getbucketlocation", "s3:getbucketlogging", "s3:getbucketversioning", "s3:getbucketwebsite"])

