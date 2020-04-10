import unittest
from policy_sentry.querying.conditions import (
    get_condition_keys_for_service,
    get_condition_key_details,
    get_condition_keys_available_to_raw_arn,
    get_conditions_for_action_and_raw_arn,
    get_condition_value_type
)


class QueryConditionsTestCase(unittest.TestCase):
    def test_get_condition_keys_for_service(self):
        """querying.conditions.get_condition_keys_for_service test"""
        expected_results = [
            'aws:ResourceTag/${TagKey}',
            'ram:AllowsExternalPrincipals',
            'ram:ResourceShareName',
            'ram:PermissionArn'
        ]
        result = get_condition_keys_for_service("ram")
        self.assertEqual(result, expected_results)


    def test_get_condition_keys_available_to_raw_arn(self):
        expected_results = [
            'aws:RequestTag/${TagKey}',
            'aws:TagKeys',
            'ec2:Region',
            'ec2:ResourceTag/${TagKey}',
            'ec2:Vpc'
        ]
        raw_arn = "arn:${Partition}:ec2:${Region}:${Account}:security-group/${SecurityGroupId}"
        result = get_condition_keys_available_to_raw_arn(raw_arn)
        print(result)
        self.assertListEqual(result, expected_results)

    def test_get_condition_key_details(self):
        """querying.conditions.get_condition_key_details"""
        desired_output = {
            "name": "cloud9:Permissions",
            "description": "Filters access by the type of AWS Cloud9 permissions",
            "condition_value_type": "string",
        }
        output = get_condition_key_details("cloud9", "cloud9:Permissions")
        self.assertEqual(desired_output, output)

    def test_get_conditions_for_action_and_raw_arn(self):
        """querying.conditions.get_conditions_for_action_and_raw_arn"""
        desired_condition_keys_list = [
            'aws:RequestTag/${TagKey}',
            'aws:TagKeys',
            'ec2:Region',
            'ec2:ResourceTag/${TagKey}',
            'ec2:Vpc'
        ]
        output = get_conditions_for_action_and_raw_arn(
            "ec2:AuthorizeSecurityGroupEgress",
            "arn:${Partition}:ec2:${Region}:${Account}:security-group/${SecurityGroupId}"
        )
        self.maxDiff = None
        # print(output)
        self.assertListEqual(desired_condition_keys_list, output)

    def test_get_condition_value_type(self):
        """querying.conditions.get_condition_value_type"""
        desired_result = "arn"
        condition_key = "secretsmanager:SecretId"
        result = get_condition_value_type(condition_key)
        self.maxDiff = None
        # print(result)
        self.assertEqual(desired_result, result)
