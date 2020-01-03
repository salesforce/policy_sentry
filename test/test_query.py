import unittest
from policy_sentry.shared.constants import DATABASE_FILE_PATH
from policy_sentry.shared.database import connect_db
from policy_sentry.querying.actions import get_actions_for_service, get_action_data, \
    get_actions_with_access_level, get_actions_with_arn_type_and_access_level, \
    get_actions_matching_condition_key, get_actions_that_support_wildcard_arns_only
from policy_sentry.querying.arns import get_raw_arns_for_service, get_arn_type_details, \
    get_arn_types_for_service
from policy_sentry.querying.conditions import get_condition_key_details, get_condition_keys_for_service
from policy_sentry.writing.policy import remove_actions_that_are_not_wildcard_arn_only

db_session = connect_db(DATABASE_FILE_PATH)


class QueryTestCase(unittest.TestCase):
    def test_get_condition_keys_for_service(self):
        """test_get_condition_keys_for_service: Tests function that grabs a list of condition keys per service."""
        desired_output = [
            'cloud9:EnvironmentId',
            'cloud9:EnvironmentName',
            'cloud9:InstanceType',
            'cloud9:Permissions',
            'cloud9:SubnetId',
            'cloud9:UserArn'
        ]
        output = get_condition_keys_for_service(db_session, "cloud9")
        self.assertEquals(desired_output, output)

    def test_get_condition_key_details(self):
        """test_get_condition_key_details: Tests function that grabs details about a specific condition key"""
        desired_output = {
            "name": "cloud9:Permissions",
            "description": "Filters access by the type of AWS Cloud9 permissions",
            "condition_value_type": "string"
        }
        output = get_condition_key_details(db_session, "cloud9", "cloud9:Permissions")
        self.assertEquals(desired_output, output)

    def test_get_raw_arns_for_service(self):
        """test_get_raw_arns_for_service: Tests function that grabs a list of raw ARNs per service"""
        desired_output = [
            "arn:${Partition}:s3:${Region}:${Account}:accesspoint/${AccessPointName}",
            "arn:${Partition}:s3:::${BucketName}",
            "arn:${Partition}:s3:::${BucketName}/${ObjectName}",
            "arn:${Partition}:s3:${Region}:${Account}:job/${JobId}"
        ]
        output = get_raw_arns_for_service(db_session, "s3")
        self.maxDiff = None
        self.assertListEqual(desired_output, output)

    def test_get_arn_types_for_service(self):
        """test_get_arn_types_for_service: Tests function that grabs arn_type and raw_arn pairs"""
        desired_output = {
            "accesspoint": "arn:${Partition}:s3:${Region}:${Account}:accesspoint/${AccessPointName}",
            "bucket": "arn:${Partition}:s3:::${BucketName}",
            "object": "arn:${Partition}:s3:::${BucketName}/${ObjectName}",
            "job": "arn:${Partition}:s3:${Region}:${Account}:job/${JobId}",
        }
        output = get_arn_types_for_service(db_session, "s3")
        print(output)
        self.maxDiff = None
        self.assertDictEqual(desired_output, output)

    def test_get_arn_type_details(self):
        """test_get_arn_type_details: Tests function that grabs details about a specific ARN name"""
        desired_output = {
            "resource_type_name": "environment",
            "raw_arn": "arn:${Partition}:cloud9:${Region}:${Account}:environment:${ResourceId}",
            "condition_keys": None
        }
        output = get_arn_type_details(db_session, "cloud9", "environment")
        self.assertEquals(desired_output, output)

    def test_get_actions_for_service(self):
        """test_get_actions_for_service: Tests function that gets a list of actions per AWS service."""
        desired_output = [
            'ram:acceptresourceshareinvitation',
            'ram:associateresourceshare',
            'ram:associateresourcesharepermission',
            'ram:createresourceshare',
            'ram:deleteresourceshare',
            'ram:disassociateresourceshare',
            'ram:disassociateresourcesharepermission',
            'ram:enablesharingwithawsorganization',
            'ram:getpermission',
            'ram:getresourcepolicies',
            'ram:getresourceshareassociations',
            'ram:getresourceshareinvitations',
            'ram:getresourceshares',
            'ram:listpendinginvitationresources',
            'ram:listpermissions',
            'ram:listprincipals',
            'ram:listresourcesharepermissions',
            'ram:listresources',
            'ram:rejectresourceshareinvitation',
            'ram:tagresource',
            'ram:untagresource',
            'ram:updateresourceshare'
        ]
        output = get_actions_for_service(db_session, "ram")
        self.maxDiff = None
        self.assertListEqual(desired_output, output)

    def test_get_action_data(self):
        """test_get_action_data: Tests function that gets details on a specific IAM Action."""
        desired_output = {
            'ram': [
                {
                    'action': 'ram:createresourceshare',
                    'description': 'Create resource share with provided resource(s) and/or principal(s)',
                    'access_level': 'Permissions management',
                    'resource_arn_format': 'arn:${Partition}:ram:${Region}:${Account}:resource-share/${ResourcePath}',
                    'condition_keys': [
                        'ram:RequestedResourceType',
                        'ram:ResourceArn',
                        # 'ram:AllowsExternalPrincipals',
                        'ram:RequestedAllowsExternalPrincipals'
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
        output = get_action_data(db_session, 'ram', 'createresourceshare')
        self.maxDiff = None
        self.assertDictEqual(desired_output, output)

    def test_get_actions_with_access_level(self):
        """test_get_actions_with_access_level: Tests function that gets a list of actions in a
        service under different access levels."""
        desired_output = ['ram:acceptresourceshareinvitation', 'ram:associateresourceshare', 'ram:createresourceshare',
                        'ram:deleteresourceshare', 'ram:disassociateresourceshare',
                        'ram:enablesharingwithawsorganization', 'ram:rejectresourceshareinvitation',
                        'ram:updateresourceshare']
        output = get_actions_with_access_level(db_session, "ram", "Permissions management")
        print(output)
        self.maxDiff = None
        self.assertListEqual(desired_output, output)

    def test_get_actions_with_arn_type_and_access_level(self):
        """test_get_actions_with_arn_type_and_access_level: Tests a function that gets a list of
        actions in a service under different access levels, specific to an ARN format."""
        desired_output = ['ram:associateresourceshare', 'ram:createresourceshare', 'ram:deleteresourceshare',
                          'ram:disassociateresourceshare', 'ram:updateresourceshare']
        output = get_actions_with_arn_type_and_access_level(db_session, "ram", "resource-share",
                                                                 "Permissions management")
        print(output)
        self.maxDiff = None
        self.assertListEqual(desired_output, output)

    def test_get_actions_matching_condition_key(self):
        """test_get_actions_matching_condition_key: Tests a function that gathers all instances in
        the action tables where the condition key exists."""
        desired_output = [
            'ses:sendemail',
            'ses:sendbulktemplatedemail',
            'ses:sendcustomverificationemail',
            'ses:sendemail',
            'ses:sendrawemail',
            'ses:sendtemplatedemail'
        ]
        output = get_actions_matching_condition_key(db_session, "ses", "ses:FeedbackAddress")
        print(output)
        self.maxDiff = None
        self.assertListEqual(desired_output, output)

    # Nuking this test... as AWS adds on more condition keys, this becomes impossible to maintain as a single test.
    # def test_get_actions_matching_condition_key(self):
    #     """test_get_actions_matching_condition_key: Tests a function that creates a list of all IAM
    #     actions that support the supplied condition key."""
    #     # condition_key = "aws:RequestTag"
    #     desired_list = [
    #         'appstream:associatefleet', 'appstream:batchassociateuserstack', 'appstream:batchdisassociateuserstack', 'appstream:copyimage', 'appstream:createimagebuilderstreamingurl', 'appstream:createstreamingurl', 'appstream:deletefleet', 'appstream:deleteimage', 'appstream:deleteimagebuilder', 'appstream:deleteimagepermissions', 'appstream:deletestack', 'appstream:disassociatefleet', 'appstream:startfleet', 'appstream:startimagebuilder', 'appstream:stopfleet', 'appstream:stopimagebuilder', 'appstream:tagresource', 'appstream:updatefleet', 'appstream:updateimagepermissions', 'appstream:updatestack', 'appsync:deletegraphqlapi', 'appsync:getgraphqlapi', 'appsync:listtagsforresource', 'appsync:tagresource', 'appsync:updategraphqlapi', 'codecommit:tagresource', 'cognito-identity:createidentitypool', 'cognito-identity:listtagsforresource', 'cognito-identity:tagresource', 'cognito-identity:untagresource', 'cognito-idp:createuserpool', 'cognito-idp:listtagsforresource', 'cognito-idp:tagresource', 'cognito-idp:untagresource', 'cognito-idp:updateuserpool', 'dms:describereplicationinstancetasklogs', 'mobiletargeting:createapp', 'mobiletargeting:createcampaign', 'mobiletargeting:createsegment', 'mobiletargeting:deletecampaign', 'mobiletargeting:deletesegment', 'mobiletargeting:getapp', 'mobiletargeting:getapps', 'mobiletargeting:getcampaign', 'mobiletargeting:getcampaignversion', 'mobiletargeting:getcampaignversions', 'mobiletargeting:getcampaigns', 'mobiletargeting:getsegment', 'mobiletargeting:getsegmentversion', 'mobiletargeting:getsegmentversions', 'mobiletargeting:getsegments', 'mobiletargeting:listtagsforresource', 'mobiletargeting:tagresource', 'mobiletargeting:untagresource', 'mobiletargeting:updatecampaign', 'mobiletargeting:updatesegment']
    #     stuff = "aws:ResourceTag/${TagKey}"
    #     output = get_actions_matching_condition_key(db_session, service=None, condition_key=stuff)
    #     self.maxDiff = None
    #     print(output)
    #     self.assertListEqual(desired_list, output)

    def test_get_actions_that_support_wildcard_arns_only(self):
        """test_get_actions_that_support_wildcard_arns_only: Tests function that shows all
        actions that support * resources only."""
        desired_output = [
            "secretsmanager:createsecret",
            "secretsmanager:getrandompassword",
            "secretsmanager:listsecrets"
        ]
        output = get_actions_that_support_wildcard_arns_only(db_session, "secretsmanager")
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
        self.maxDiff = None
        self.assertListEqual(desired_output, output)

