import unittest
from policy_sentry.shared.constants import DATABASE_FILE_PATH
from policy_sentry.shared.database import connect_db
from policy_sentry.querying.conditions import get_condition_key_details, get_condition_keys_for_service, \
    get_conditions_for_action_and_raw_arn, get_condition_value_type
db_session = connect_db(DATABASE_FILE_PATH)


class QueryConditionsTestCase(unittest.TestCase):
    def test_get_condition_keys_for_service(self):
        """querying.conditions.get_condition_keys_for_service test"""
        desired_output = [
            'cloud9:EnvironmentId',
            'cloud9:EnvironmentName',
            'cloud9:InstanceType',
            'cloud9:Permissions',
            'cloud9:SubnetId',
            'cloud9:UserArn'
        ]
        output = get_condition_keys_for_service(db_session, "cloud9")
        self.assertEqual(desired_output, output)

    def test_get_condition_key_details(self):
        """querying.conditions.get_condition_key_details"""
        desired_output = {
            "name": "cloud9:Permissions",
            "description": "Filters access by the type of AWS Cloud9 permissions",
            "condition_value_type": "string"
        }
        output = get_condition_key_details(db_session, "cloud9", "cloud9:Permissions")
        self.assertEqual(desired_output, output)

    def test_get_conditions_for_action_and_raw_arn(self):
        """querying.conditions.get_conditions_for_action_and_raw_arn"""
        # Test with wildcard as ARN
        desired_condition_keys_list = [
            'secretsmanager:Name',
            'secretsmanager:Description',
            'secretsmanager:KmsKeyId',
            'aws:RequestTag/tag-key',
            'aws:TagKeys',
            'secretsmanager:ResourceTag/tag-key'
        ]
        output = get_conditions_for_action_and_raw_arn(db_session, "secretsmanager:createsecret", "*")
        self.maxDiff = None
        # print(output)
        self.assertListEqual(desired_condition_keys_list, output)

    # Nuking this test... as AWS adds on more condition keys, this becomes impossible to maintain as a single test.
    # def test_get_actions_matching_condition_key(self):
    #     """test_get_actions_matching_condition_key: Tests a function that creates a list of all IAM
    #     actions that support the supplied condition key."""
    #     # condition_key = "aws:RequestTag"
    #     desired_list = []
    #     stuff = "aws:ResourceTag/${TagKey}"
    #     output = get_actions_matching_condition_key(db_session, service=None, condition_key=stuff)
    #     self.maxDiff = None
    #     print(output)
    #     self.assertListEqual(desired_list, output)

    def test_get_condition_value_type(self):
        """querying.conditions.get_condition_value_type"""
        desired_result = "Arn"
        condition_key = "secretsmanager:SecretId"
        result = get_condition_value_type(db_session, condition_key)
        self.maxDiff = None
        # print(result)
        self.assertEqual(desired_result, result)
