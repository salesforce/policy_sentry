import unittest
import json
from policy_sentry.shared.database import connect_db
from policy_sentry.writing.template import get_crud_template_dict, get_actions_template_dict
from policy_sentry.command.write_policy import write_policy_with_access_levels, write_policy_with_actions

desired_crud_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "MultMultNone",
            "Effect": "Allow",
            "Action": [
                "kms:createcustomkeystore"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Sid": "SecretsmanagerReadSecret",
            "Effect": "Allow",
            "Action": [
                "secretsmanager:describesecret",
                "secretsmanager:getresourcepolicy",
                "secretsmanager:getsecretvalue",
                "secretsmanager:listsecretversionids"
            ],
            "Resource": [
                "arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"
            ]
        },
        {
            "Sid": "SecretsmanagerWriteSecret",
            "Effect": "Allow",
            "Action": [
                "secretsmanager:cancelrotatesecret",
                "secretsmanager:deletesecret",
                "secretsmanager:putsecretvalue",
                "secretsmanager:restoresecret",
                "secretsmanager:rotatesecret",
                "secretsmanager:updatesecret",
                "secretsmanager:updatesecretversionstage"
            ],
            "Resource": [
                "arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"
            ]
        },
        {
            "Sid": "KmsPermissionsmanagementKmskey",
            "Effect": "Allow",
            "Action": [
                "kms:creategrant",
                "kms:putkeypolicy",
                "kms:retiregrant",
                "kms:revokegrant"
            ],
            "Resource": [
                "arn:aws:kms:us-east-1:123456789012:key/123456"
            ]
        }
    ]
}

desired_actions_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "KmsPermissionsmanagementKmskey",
            "Effect": "Allow",
            "Action": [
                "kms:creategrant"
            ],
            "Resource": [
                "arn:${Partition}:kms:${Region}:${Account}:key/${KeyId}"
            ]
        },
        {
            "Sid": "Ec2WriteSecuritygroup",
            "Effect": "Allow",
            "Action": [
                "ec2:authorizesecuritygroupegress",
                "ec2:authorizesecuritygroupingress"
            ],
            "Resource": [
                "arn:${Partition}:ec2:${Region}:${Account}:security-group/${SecurityGroupId}"
            ]
        },
        {
            "Sid": "MultMultNone",
            "Effect": "Allow",
            "Action": [
                "kms:createcustomkeystore",
                "cloudhsm:describeclusters"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}


class WritePolicyWithLibraryOnly(unittest.TestCase):

    def test_write_actions_policy_with_library_only(self):
        """test_write_actions_policy_with_library_only: Write an actions mode policy without using the command line at all (library only)"""
        db_session = connect_db('bundled')
        actions_template = get_actions_template_dict()
        print(actions_template)
        actions_to_add = ['kms:CreateGrant', 'kms:CreateCustomKeyStore', 'ec2:AuthorizeSecurityGroupEgress', 'ec2:AuthorizeSecurityGroupIngress']
        actions_template['policy_with_actions'][0]['name'] = "MyPolicy"
        actions_template['policy_with_actions'][0]['description'] = "Description"
        actions_template['policy_with_actions'][0]['role_arn'] = "somearn"
        actions_template['policy_with_actions'][0]['actions'].extend(actions_to_add)
        # Modify it
        policy = write_policy_with_actions(db_session, actions_template)
        # print(json.dumps(policy, indent=4))
        self.maxDiff = None
        self.assertDictEqual(desired_actions_policy, policy)

    def test_write_crud_policy_with_library_only(self):
        """test_write_crud_policy_with_library_only: Write an actions mode policy without using the command line at all (library only)"""
        db_session = connect_db('bundled')
        crud_template = get_crud_template_dict()
        wildcard_actions_to_add = ["kms:createcustomkeystore", "cloudhsm:describeclusters"]
        print(crud_template)
        crud_template['policy_with_crud_levels'][0]['name'] = "MyPolicy"
        crud_template['policy_with_crud_levels'][0]['description'] = "Description"
        crud_template['policy_with_crud_levels'][0]['role_arn'] = "somearn"
        crud_template['policy_with_crud_levels'][0]['read'].append("arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret")
        crud_template['policy_with_crud_levels'][0]['write'].append("arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret")
        crud_template['policy_with_crud_levels'][0]['list'].append("arn:aws:s3:::example-org-sbx-vmimport/stuff")
        crud_template['policy_with_crud_levels'][0]['permissions-management'].append("arn:aws:kms:us-east-1:123456789012:key/123456")
        crud_template['policy_with_crud_levels'][0]['wildcard'].extend(wildcard_actions_to_add)
        crud_template['policy_with_crud_levels'][0]['tagging'].append("arn:aws:ssm:us-east-1:123456789012:parameter/test")
        # Modify it
        policy = write_policy_with_access_levels(db_session, crud_template, None)
        # print(json.dumps(policy, indent=4))
        self.assertDictEqual(desired_crud_policy, policy)
