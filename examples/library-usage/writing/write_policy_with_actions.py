#!/usr/bin/env python
from policy_sentry.shared.database import connect_db
from policy_sentry.writing.template import get_crud_template_dict, get_actions_template_dict
from policy_sentry.command.write_policy import write_policy_with_access_levels, write_policy_with_actions
import json


if __name__ == '__main__':
    db_session = connect_db('bundled')
    actions_template = get_actions_template_dict()
    print(actions_template)
    actions_to_add = ['kms:CreateGrant', 'kms:CreateCustomKeyStore', 'ec2:AuthorizeSecurityGroupEgress',
                      'ec2:AuthorizeSecurityGroupIngress']
    actions_template['policy_with_actions'][0]['name'] = "MyPolicy"
    actions_template['policy_with_actions'][0]['description'] = "Description"
    actions_template['policy_with_actions'][0]['role_arn'] = "somearn"
    actions_template['policy_with_actions'][0]['actions'].extend(actions_to_add)
    policy = write_policy_with_actions(db_session, actions_template)
    print(json.dumps(policy, indent=4))

"""
Output:

{
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
"""
