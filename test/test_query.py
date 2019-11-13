import unittest
from pathlib import Path
from policy_sentry.shared.database import connect_db
from policy_sentry.shared.query import query_condition_table_by_name, query_condition_table, \
    query_arn_table_for_raw_arns, query_arn_table_by_name, query_action_table, query_action_table_by_name, \
    query_action_table_by_access_level, query_action_table_by_arn_type_and_access_level, \
    query_action_table_for_all_condition_key_matches, query_action_table_for_actions_supporting_wildcards_only, \
    query_arn_table_for_arn_types, remove_actions_that_are_not_wildcard_arn_only

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

    def test_query_arn_table_for_raw_arns(self):
        """test_query_arn_table_for_raw_arns: Tests function that grabs a list of raw ARNs per service"""
        desired_output = [
            'arn:aws:ssm:${Region}:${Account}:document/${DocumentName}',
            'arn:aws:ssm:${Region}:${Account}:maintenancewindow/${ResourceId}',
            'arn:aws:ssm:${Region}:${Account}:managed-instance/${ManagedInstanceName}',
            'arn:aws:ssm:${Region}:${Account}:parameter/${FullyQualifiedParameterName}',
            'arn:aws:ssm:${Region}:${Account}:patchbaseline/${ResourceId}',
            'arn:aws:ssm:${Region}:${Account}:session/${ResourceId}',
            'arn:aws:ssm:${Region}:${Account}:opsitem/${ResourceId}'
        ]
        output = query_arn_table_for_raw_arns(db_session, "ssm")
        self.assertListEqual(desired_output, output)

    def test_query_arn_table_for_arn_types(self):
        """test_query_arn_table_for_arn_types: Tests function that grabs arn_type and raw_arn pairs"""
        desired_output = {
            'document': 'arn:aws:ssm:${Region}:${Account}:document/${DocumentName}',
            'maintenancewindow': 'arn:aws:ssm:${Region}:${Account}:maintenancewindow/${ResourceId}',
            'managed-instance': 'arn:aws:ssm:${Region}:${Account}:managed-instance/${ManagedInstanceName}',
            'parameter': 'arn:aws:ssm:${Region}:${Account}:parameter/${FullyQualifiedParameterName}',
            'patchbaseline': 'arn:aws:ssm:${Region}:${Account}:patchbaseline/${ResourceId}',
            'session': 'arn:aws:ssm:${Region}:${Account}:session/${ResourceId}',
            'opsitem': 'arn:aws:ssm:${Region}:${Account}:opsitem/${ResourceId}'
        }
        output = query_arn_table_for_arn_types(db_session, "ssm")
        print(output)
        self.assertDictEqual(desired_output, output)

    def test_query_arn_table_by_name(self):
        """test_query_arn_table_by_name: Tests function that grabs details about a specific ARN name"""
        desired_output = {
            "resource_type_name": "environment",
            "raw_arn": "arn:aws:cloud9:${Region}:${Account}:environment:${ResourceId}",
            "condition_keys": None
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
            'ram': [
                {
                    'action': 'ram:createresourceshare',
                    'description': 'Create resource share with provided resource(s) and/or principal(s)',
                    'access_level': 'Permissions management',
                    'resource_arn_format': 'arn:aws:ram:${Region}:${Account}:resource-share/${ResourcePath}',
                    'condition_keys': [
                        'ram:RequestedResourceType',
                        'ram:ResourceArn',
                        'ram:AllowsExternalPrincipals'
                    ],
                    'dependent_actions': None
                },
                {
                    'action': 'ram:createresourceshare',
                    'description': 'Create resource share with provided resource(s) and/or principal(s)',
                    'access_level': 'Permissions management',
                    'resource_arn_format': '*',
                    'condition_keys': [
                        'aws:RequestTag/${TagKey}',
                        'aws:TagKeys'
                    ],
                    'dependent_actions': None
                }
            ]
        }
        output = query_action_table_by_name(db_session, 'ram', 'createresourceshare')
        self.maxDiff = None
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
        self.maxDiff = None
        self.assertListEqual(desired_output, output)

    def test_query_action_table_by_arn_type_and_access_level(self):
        """test_query_action_table_by_arn_type_and_access_level: Tests a function that gets a list of
        actions in a service under different access levels, specific to an ARN format."""
        desired_output = ['ram:associateresourceshare', 'ram:createresourceshare', 'ram:deleteresourceshare',
                          'ram:disassociateresourceshare', 'ram:updateresourceshare']
        output = query_action_table_by_arn_type_and_access_level(db_session, "ram", "resource-share",
                                                                 "Permissions management")
        print(output)
        self.maxDiff = None
        self.assertListEqual(desired_output, output)

    def test_query_action_table_for_service_specific_condition_key_matches(self):
        """test_query_action_table_for_all_condition_key_matches: Tests a function that gathers all instances in
        the action tables where the condition key exists."""
        desired_output = ['ses:sendbulktemplatedemail', 'ses:sendcustomverificationemail', 'ses:sendemail',
                          'ses:sendrawemail', 'ses:sendtemplatedemail']
        output = query_action_table_for_all_condition_key_matches(db_session, "ses", "ses:FeedbackAddress")
        print(output)
        self.maxDiff = None
        self.assertListEqual(desired_output, output)

    def test_query_action_table_for_all_condition_key_matches(self):
        """test_query_action_table_for_all_condition_key_matches: Tests a function that creates a list of all IAM
        actions that support the supplied condition key."""
        # condition_key = "aws:RequestTag"
        desired_list = ['appstream:associatefleet', 'appstream:batchassociateuserstack', 'appstream:batchdisassociateuserstack', 'appstream:copyimage', 'appstream:createimagebuilderstreamingurl', 'appstream:createstreamingurl', 'appstream:deletefleet', 'appstream:deleteimage', 'appstream:deleteimagebuilder', 'appstream:deleteimagepermissions', 'appstream:deletestack', 'appstream:disassociatefleet', 'appstream:startfleet', 'appstream:startimagebuilder', 'appstream:stopfleet', 'appstream:stopimagebuilder', 'appstream:tagresource', 'appstream:updatefleet', 'appstream:updateimagepermissions', 'appstream:updatestack', 'appsync:deletegraphqlapi', 'appsync:getgraphqlapi', 'appsync:listtagsforresource', 'appsync:tagresource', 'appsync:updategraphqlapi', 'codecommit:tagresource', 'cognito-identity:createidentitypool', 'cognito-identity:listtagsforresource', 'cognito-identity:tagresource', 'cognito-identity:untagresource', 'cognito-idp:createuserpool', 'cognito-idp:listtagsforresource', 'cognito-idp:tagresource', 'cognito-idp:untagresource', 'cognito-idp:updateuserpool', 'dms:describereplicationinstancetasklogs', 'mobiletargeting:createapp', 'mobiletargeting:createcampaign', 'mobiletargeting:createsegment', 'mobiletargeting:deletecampaign', 'mobiletargeting:deletesegment', 'mobiletargeting:getapp', 'mobiletargeting:getapps', 'mobiletargeting:getcampaign', 'mobiletargeting:getcampaignversion', 'mobiletargeting:getcampaignversions', 'mobiletargeting:getcampaigns', 'mobiletargeting:getsegment', 'mobiletargeting:getsegmentversion', 'mobiletargeting:getsegmentversions', 'mobiletargeting:getsegments', 'mobiletargeting:listtagsforresource', 'mobiletargeting:tagresource', 'mobiletargeting:untagresource', 'mobiletargeting:updatecampaign', 'mobiletargeting:updatesegment']
        stuff = "aws:ResourceTag/${TagKey}"
        output = query_action_table_for_all_condition_key_matches(db_session, service=None, condition_key=stuff)
        self.maxDiff = None
        print(output)
        self.assertListEqual(desired_list, output)

    def test_query_action_table_for_actions_supporting_wildcards_only(self):
        """test_query_action_table_for_actions_supporting_wildcards_only: Tests function that shows all
        actions that support * resources only."""
        desired_output = [
            "secretsmanager:createsecret",
            "secretsmanager:getrandompassword",
            "secretsmanager:listsecrets"
        ]
        output = query_action_table_for_actions_supporting_wildcards_only(db_session, "secretsmanager")
        self.maxDiff = None
        print(output)
        self.assertListEqual(desired_output, output)

    def test_remove_actions_that_are_not_wildcard_arn_only(self):
        """test_remove_actions_that_are_not_wildcard_arn_only: Tests function that removes actions from a list that
        are not wildcard ARNs only"""
        provided_actions_list = [
            # 3 wildcard only actions
            "secretsmanager:createsecret",
            "secretsmanager:getrandompassword",
            "secretsmanager:listsecrets",
            # This one is wildcard OR "secret"
            "secretsmanager:putsecretvalue"
        ]
        desired_output = [
            # 3 wildcard only actions
            "secretsmanager:createsecret",
            "secretsmanager:getrandompassword",
            "secretsmanager:listsecrets",
        ]
        output = remove_actions_that_are_not_wildcard_arn_only(db_session, provided_actions_list)
        self.assertListEqual(desired_output, output)

