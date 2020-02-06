import unittest
import json
from policy_sentry.shared.database import connect_db
from policy_sentry.command.write_policy import write_policy
from policy_sentry.writing.sid_group import SidGroup
from policy_sentry.writing.template import get_crud_template_dict, get_actions_template_dict

desired_crud_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "MultMultNone",
            "Effect": "Allow",
            "Action": [
                "cloudhsm:describeclusters",
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
            "Sid": "KmsPermissionsmanagementKey",
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
        },
        {
            "Sid": "SsmTaggingParameter",
            "Effect": "Allow",
            "Action": [
                "ssm:addtagstoresource",
                "ssm:removetagsfromresource"
            ],
            "Resource": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/test"
            ]
        }
    ]
}

desired_actions_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "KmsPermissionsmanagementKey",
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
                "cloudhsm:describeclusters",
                "kms:createcustomkeystore"
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
        # print(actions_template)
        actions_to_add = ['kms:creategrant', 'kms:createcustomkeystore', 'ec2:authorizesecuritygroupegress', 'ec2:authorizesecuritygroupingress']
        actions_template['mode'] = 'actions'
        actions_template['actions'].extend(actions_to_add)
        # Modify it
        sid_group = SidGroup()
        minimize = None
        policy = sid_group.process_template(db_session, actions_template, minimize=minimize)
        self.maxDiff = None
        # print("desired_actions_policy")
        # print(json.dumps(desired_actions_policy, indent=4))
        # print("policy")
        # print(json.dumps(policy, indent=4))
        self.assertDictEqual(desired_actions_policy, policy)

    def test_write_crud_policy_with_library_only(self):
        """test_write_crud_policy_with_library_only: Write a policy in CRUD mode without using the command line at all (library only)"""
        db_session = connect_db('bundled')
        crud_template = get_crud_template_dict()
        wildcard_actions_to_add = ["kms:createcustomkeystore", "cloudhsm:describeclusters"]
        crud_template['mode'] = 'crud'
        crud_template['read'].append("arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret")
        crud_template['write'].append("arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret")
        crud_template['list'].append("arn:aws:s3:::example-org-sbx-vmimport/stuff")
        crud_template['permissions-management'].append("arn:aws:kms:us-east-1:123456789012:key/123456")
        crud_template['wildcard'].extend(wildcard_actions_to_add)
        crud_template['tagging'].append("arn:aws:ssm:us-east-1:123456789012:parameter/test")
        # Modify it
        sid_group = SidGroup()
        minimize = None
        policy = sid_group.process_template(db_session, crud_template, minimize=minimize)
        # print("desired_crud_policy")
        # print(json.dumps(desired_crud_policy, indent=4))
        # print("policy")
        # print(json.dumps(policy, indent=4))
        self.maxDiff = None
        self.assertDictEqual(desired_crud_policy, policy)
