import unittest
from policy_sentry.shared.constants import DATABASE_FILE_PATH
from policy_sentry.shared.database import connect_db
from policy_sentry.querying.actions import get_actions_for_service, get_action_data, \
    get_actions_with_access_level, get_actions_with_arn_type_and_access_level, \
    get_actions_matching_condition_key, get_actions_that_support_wildcard_arns_only, \
    get_actions_matching_condition_crud_and_arn, get_actions_at_access_level_that_support_wildcard_arns_only
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
        self.assertEqual(desired_output, output)

    def test_get_condition_key_details(self):
        """test_get_condition_key_details: Tests function that grabs details about a specific condition key"""
        desired_output = {
            "name": "cloud9:Permissions",
            "description": "Filters access by the type of AWS Cloud9 permissions",
            "condition_value_type": "string"
        }
        output = get_condition_key_details(db_session, "cloud9", "cloud9:Permissions")
        self.assertEqual(desired_output, output)

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
        self.assertEqual(desired_output, output)

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

    def test_get_actions_at_access_level_that_support_wildcard_arns_only(self):
        """test_get_actions_at_access_level_that_support_wildcard_arns_only: Test function that gets a list of
         wildcard-only actions in a service under different access levels"""
        permissions_output = get_actions_at_access_level_that_support_wildcard_arns_only(db_session, "s3", "Permissions management")
        list_output = get_actions_at_access_level_that_support_wildcard_arns_only(db_session, "s3", "List")
        read_output = get_actions_at_access_level_that_support_wildcard_arns_only(db_session, "s3", "Read")
        self.assertListEqual(permissions_output, ['s3:putaccountpublicaccessblock'])
        self.assertListEqual(list_output, ['s3:listallmybuckets'])
        self.assertListEqual(read_output, ['s3:getaccesspoint', 's3:getaccountpublicaccessblock', 's3:listaccesspoints'])

    def test_get_all_actions_with_access_level(self):
        """test_get_all_actions_with_access_level: Get all actions with a given access level"""
        # list1 elements should be in result
        list1 = get_actions_with_access_level(db_session, "all", "Permissions management")
        list2 = ["s3:deleteaccesspointpolicy", "s3:putbucketacl"]
        self.maxDiff = None
        print(list1)
        # decision = list1 contains all elements of list2 using all()
        decision = all(elem in list1 for elem in list2)
        print(f"decision is {decision}")
        self.assertTrue(decision)

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

    def test_get_actions_matching_condition_crud_and_arn(self):
        """test_get_actions_matching_condition_crud_and_arn: Get a list of IAM Actions matching condition key,
        CRUD level, and raw ARN"""
        results = get_actions_matching_condition_crud_and_arn(
            db_session,
            "ram:ResourceArn",
            "Permissions management",
            "arn:${Partition}:ram:${Region}:${Account}:resource-share/${ResourcePath}"
        )
        desired_results = ['ram:createresourceshare']
        self.assertListEqual(desired_results, results)

    def test_get_actions_matching_condition_crud_and_wildcard_arn(self):
        """test_get_actions_matching_condition_crud_and_wildcard_arn: Get a list of IAM Actions matching condition key
        , CRUD level, and raw ARN. Raw ARN equals * in this case"""
        desired_results = [
            'swf:pollforactivitytask',
            'swf:pollfordecisiontask',
            'swf:respondactivitytaskcompleted',
            'swf:startworkflowexecution'
        ]
        results = get_actions_matching_condition_crud_and_arn(db_session, "swf:taskList.name", "Write", "*")
        self.assertListEqual(desired_results, results)

        # This one leverages a condition key that is partway through a string in the database
        # - luckily, SQLAlchemy's ilike function allows us to find it anyway because it's a substring
        # kms:CallerAccount,kms:EncryptionAlgorithm,kms:EncryptionContextKeys,kms:ViaService
        desired_results = [
            'kms:decrypt',
            'kms:encrypt',
            'kms:generatedatakey',
            'kms:generatedatakeypair',
            'kms:generatedatakeypairwithoutplaintext',
            'kms:generatedatakeywithoutplaintext',
            'kms:reencryptfrom',
            'kms:reencryptto'
        ]
        results = get_actions_matching_condition_crud_and_arn(db_session, "kms:EncryptionAlgorithm", "Write", "*")
        self.assertListEqual(desired_results, results)

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

