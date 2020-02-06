import unittest
from policy_sentry.shared.constants import DATABASE_FILE_PATH
from policy_sentry.shared.database import connect_db
from policy_sentry.querying.actions import get_actions_for_service, get_action_data, \
    get_actions_with_access_level, get_actions_with_arn_type_and_access_level, \
    get_actions_matching_condition_key, get_actions_that_support_wildcard_arns_only, \
    get_actions_matching_condition_crud_and_arn, get_actions_at_access_level_that_support_wildcard_arns_only, \
    remove_actions_that_are_not_wildcard_arn_only, get_dependent_actions, remove_actions_not_matching_access_level

db_session = connect_db(DATABASE_FILE_PATH)


class QueryActionsTestCase(unittest.TestCase):

    def test_get_actions_for_service(self):
        """querying.actions.get_actions_for_service"""
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
        """querying.actions.test_get_action_data"""
        desired_output = {
            "ram": [
                {
                    "action": "ram:createresourceshare",
                    "description": "Create resource share with provided resource(s) and/or principal(s)",
                    "access_level": "Permissions management",
                    "resource_arn_format": "*",
                    "condition_keys": [
                        "aws:RequestTag/${TagKey}",
                        "aws:TagKeys",
                        "ram:RequestedResourceType",
                        "ram:ResourceArn",
                        "ram:RequestedAllowsExternalPrincipals",
                        "ram:Principal"
                    ],
                    "dependent_actions": None
                }
            ]
        }
        output = get_action_data(db_session, 'ram', 'createresourceshare')
        # print(json.dumps(output, indent=4))
        self.maxDiff = None
        self.assertDictEqual(desired_output, output)

    def test_get_actions_that_support_wildcard_arns_only(self):
        """querying.actions.get_actions_that_support_wildcard_arns_only"""
        desired_output = [
            "secretsmanager:createsecret",
            "secretsmanager:getrandompassword",
            "secretsmanager:listsecrets"
        ]
        output = get_actions_that_support_wildcard_arns_only(db_session, "secretsmanager")
        self.maxDiff = None
        # print(output)
        self.assertListEqual(desired_output, output)

    def test_get_actions_at_access_level_that_support_wildcard_arns_only(self):
        """querying.actions.get_actions_at_access_level_that_support_wildcard_arns_only"""
        permissions_output = get_actions_at_access_level_that_support_wildcard_arns_only(db_session, "s3",
                                                                                         "Permissions management")
        list_output = get_actions_at_access_level_that_support_wildcard_arns_only(db_session, "s3", "List")
        read_output = get_actions_at_access_level_that_support_wildcard_arns_only(db_session, "s3", "Read")
        self.assertListEqual(permissions_output, ['s3:putaccountpublicaccessblock'])
        self.assertListEqual(list_output, ['s3:listallmybuckets'])
        self.assertListEqual(read_output,
                             ['s3:getaccesspoint', 's3:getaccountpublicaccessblock', 's3:listaccesspoints'])


    def test_get_actions_with_access_level(self):
        """querying.actions.get_actions_with_access_level"""
        desired_output = ['ram:acceptresourceshareinvitation', 'ram:associateresourceshare', 'ram:createresourceshare',
                        'ram:deleteresourceshare', 'ram:disassociateresourceshare',
                        'ram:enablesharingwithawsorganization', 'ram:rejectresourceshareinvitation',
                        'ram:updateresourceshare']
        output = get_actions_with_access_level(db_session, "ram", "Permissions management")
        # print(output)
        self.maxDiff = None
        self.assertListEqual(desired_output, output)

    def test_get_actions_with_arn_type_and_access_level(self):
        """querying.actions.get_actions_with_arn_type_and_access_level"""
        desired_output = [
            'ram:associateresourceshare',
            # 'ram:createresourceshare',
            'ram:deleteresourceshare',
            'ram:disassociateresourceshare',
            'ram:updateresourceshare'
        ]
        output = get_actions_with_arn_type_and_access_level(db_session, "ram", "resource-share",
                                                                 "Permissions management")
        # print(output)
        self.maxDiff = None
        self.assertListEqual(desired_output, output)

    def test_get_actions_matching_condition_key(self):
        """querying.actions.get_actions_matching_condition_key"""
        desired_output = [
            'ses:sendemail',
            'ses:sendbulktemplatedemail',
            'ses:sendcustomverificationemail',
            'ses:sendemail',
            'ses:sendrawemail',
            'ses:sendtemplatedemail'
        ]
        output = get_actions_matching_condition_key(db_session, "ses", "ses:FeedbackAddress")
        # print(output)
        self.maxDiff = None
        self.assertListEqual(desired_output, output)

    def test_get_actions_matching_condition_crud_and_arn(self):
        """querying.actions.get_actions_matching_condition_crud_and_arn"""
        results = get_actions_matching_condition_crud_and_arn(
            db_session,
            "elasticbeanstalk:InApplication",
            "List",
            "arn:${Partition}:elasticbeanstalk:${Region}:${Account}:environment/${ApplicationName}/${EnvironmentName}"
        )
        desired_results = [
            'elasticbeanstalk:describeenvironments',
        ]
        self.assertListEqual(desired_results, results)

    def test_get_actions_matching_condition_crud_and_wildcard_arn(self):
        """querying.actions.get_actions_matching_condition_crud_and_wildcard_arn"""
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

    def test_remove_actions_not_matching_access_level(self):
        """querying.actions.remove_actions_not_matching_access_level"""
        actions_list = [
            "ecr:BatchGetImage",  # Read
            "ecr:CreateRepository",  # Write
            "ecr:DescribeRepositories",  # List
            "ecr:TagResource",  # Tagging
            "ecr:SetRepositoryPolicy",  # Permissions management
        ]
        # print("Read ")
        self.maxDiff = None
        # Read
        read_result = remove_actions_not_matching_access_level(db_session, actions_list, "read")
        self.assertListEqual(read_result, ["ecr:batchgetimage"])
        # Write
        write_result = remove_actions_not_matching_access_level(db_session, actions_list, "write")
        self.assertListEqual(write_result, ["ecr:createrepository"])
        # List
        list_result = remove_actions_not_matching_access_level(db_session, actions_list, "list")
        self.assertListEqual(list_result, ["ecr:describerepositories"])
        # Tagging
        tagging_result = remove_actions_not_matching_access_level(db_session, actions_list, "tagging")
        self.assertListEqual(tagging_result, ["ecr:tagresource"])
        # Permissions management
        permissions_result = remove_actions_not_matching_access_level(db_session, actions_list, "permissions-management")
        self.assertListEqual(permissions_result, ["ecr:setrepositorypolicy"])

    def test_get_dependent_actions(self):
        """querying.actions.get_dependent_actions"""
        dependent_actions_single = ["ec2:associateiaminstanceprofile"]
        dependent_actions_double = ["shield:associatedrtlogbucket"]
        dependent_actions_several = ["chime:getcdrbucket"]
        self.assertEqual(get_dependent_actions(db_session, dependent_actions_single), ["iam:passrole"])
        self.assertEqual(get_dependent_actions(db_session, dependent_actions_double), ["s3:getbucketpolicy", "s3:putbucketpolicy"])
        self.assertEqual(get_dependent_actions(db_session, dependent_actions_several), ["s3:getbucketacl", "s3:getbucketlocation", "s3:getbucketlogging", "s3:getbucketversioning", "s3:getbucketwebsite"])

    def test_remove_actions_that_are_not_wildcard_arn_only(self):
        """querying.actions.remove_actions_that_are_not_wildcard_arn_only"""
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
