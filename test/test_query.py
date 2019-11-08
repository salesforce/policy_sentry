import unittest
from pathlib import Path
from policy_sentry.shared.database import connect_db
from policy_sentry.shared.query import query_condition_table_by_name, query_condition_table, query_arn_table, \
    query_arn_table_by_name, query_action_table, query_action_table_by_name, query_action_table_by_access_level, \
    query_action_table_by_arn_type_and_access_level

HOME = str(Path.home())
CONFIG_DIRECTORY = '/.policy_sentry/'
DATABASE_FILE_NAME = 'aws.sqlite3'
database_file_path = HOME + CONFIG_DIRECTORY + DATABASE_FILE_NAME
db_session = connect_db(database_file_path)


class QueryTestCase(unittest.TestCase):
    def test_query_condition_table(self):
        """test_query_condition_table: Tests function that grabs a list of condition keys per service."""
        desired_output = [
            'cloud9:EnvironmentId',
            'cloud9:EnvironmentName',
            'cloud9:InstanceType',
            'cloud9:Permissions',
            'cloud9:SubnetId',
            'cloud9:UserArn'
        ]
        output = query_condition_table(db_session, "cloud9")
        self.assertEquals(desired_output, output)

    def test_query_condition_table_by_name(self):
        """test_query_condition_table_by_name: Tests function that grabs details about a specific condition key"""
        desired_output = {
            "name": "cloud9:Permissions",
            "description": "Filters access by the type of AWS Cloud9 permissions",
            "condition_value_type": "string"
        }
        output = query_condition_table_by_name(db_session, "cloud9", "cloud9:Permissions")
        self.assertEquals(desired_output, output)

    def test_query_arn_table(self):
        """test_query_arn_table: Tests function that grabs a list of raw ARNs per service"""
        desired_output = [
            'arn:aws:ssm:${Region}:${Account}:document/${DocumentName}',
            'arn:aws:ssm:${Region}:${Account}:maintenancewindow/${ResourceId}',
            'arn:aws:ssm:${Region}:${Account}:managed-instance/${ManagedInstanceName}',
            'arn:aws:ssm:${Region}:${Account}:parameter/${FullyQualifiedParameterName}',
            'arn:aws:ssm:${Region}:${Account}:patchbaseline/${ResourceId}',
            'arn:aws:ssm:${Region}:${Account}:session/${ResourceId}',
            'arn:aws:ssm:${Region}:${Account}:opsitem/${ResourceId}'
        ]
        output = query_arn_table(db_session, "ssm")
        self.assertListEqual(desired_output, output)

    def test_query_arn_table_by_name(self):
        """test_query_arn_table_by_name: Tests function that grabs details about a specific ARN name"""
        desired_output = {
            "resource_type_name": "environment",
            "raw_arn": "arn:aws:cloud9:${Region}:${Account}:environment:${ResourceId}"
        }
        output = query_arn_table_by_name(db_session, "cloud9", "environment")
        self.assertEquals(desired_output, output)

    def test_query_action_table(self):
        """test_query_action_table: Tests function that gets a list of actions per AWS service."""
        desired_output = ['ram:acceptresourceshareinvitation', 'ram:associateresourceshare', 'ram:createresourceshare',
                        'ram:deleteresourceshare', 'ram:disassociateresourceshare',
                        'ram:enablesharingwithawsorganization', 'ram:getresourcepolicies',
                        'ram:getresourceshareassociations', 'ram:getresourceshareinvitations', 'ram:getresourceshares',
                        'ram:listpendinginvitationresources', 'ram:rejectresourceshareinvitation', 'ram:tagresource',
                        'ram:untagresource', 'ram:updateresourceshare']
        output = query_action_table(db_session, "ram")
        self.assertListEqual(desired_output, output)

    def test_query_action_table_by_name(self):
        """test_query_action_table_by_name: Tests function that gets details on a specific IAM Action."""
        desired_output = {
            "ram": [
                {
                    "action": "ram:createresourceshare",
                    "description": "Create resource share with provided resource(s) and/or principal(s)",
                    "access_level": "Permissions management",
                    "resource_arn_format": "arn:aws:ram:${Region}:${Account}:resource-share/${ResourcePath}",
                    "condition_keys": "ram:RequestedResourceType,ram:ResourceArn,ram:AllowsExternalPrincipals",
                    "dependent_actions": None
                },
                {
                    "action": "ram:createresourceshare",
                    "description": "Create resource share with provided resource(s) and/or principal(s)",
                    "access_level": "Permissions management",
                    "resource_arn_format": "*",
                    "condition_keys": "aws:RequestTag/${TagKey},aws:TagKeys",
                    "dependent_actions": None
                }
            ]
        }
        output = query_action_table_by_name(db_session, 'ram', 'createresourceshare')
        self.assertDictEqual(desired_output, output)

    def test_query_action_table_by_access_level(self):
        """test_query_action_table_by_access_level: Tests function that gets a list of actions in a
        service under different access levels."""
        desired_output = ['ram:acceptresourceshareinvitation', 'ram:associateresourceshare', 'ram:createresourceshare',
                        'ram:deleteresourceshare', 'ram:disassociateresourceshare',
                        'ram:enablesharingwithawsorganization', 'ram:rejectresourceshareinvitation',
                        'ram:updateresourceshare']
        output = query_action_table_by_access_level(db_session, "ram", "Permissions management")
        print(output)
        self.assertListEqual(desired_output, output)

    def test_query_action_table_by_arn_type_and_access_level(self):
        """test_query_action_table_by_arn_type_and_access_level: Tests a function that gets a list of
        actions in a service under different access levels, specific to an ARN format."""
        desired_output = ['ram:associateresourceshare', 'ram:createresourceshare', 'ram:deleteresourceshare',
                          'ram:disassociateresourceshare', 'ram:updateresourceshare']
        output = query_action_table_by_arn_type_and_access_level(db_session, "ram", "resource-share",
                                                                 "Permissions management")
        print(output)
        self.assertListEqual(desired_output, output)
