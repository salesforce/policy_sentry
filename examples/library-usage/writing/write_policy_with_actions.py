#!/usr/bin/env python

import json

from policy_sentry.command.write_policy import write_policy_with_template
from policy_sentry.writing.template import get_actions_template_dict

if __name__ == "__main__":
    actions_template = get_actions_template_dict()
    actions_to_add = [
        "kms:CreateGrant",
        "kms:CreateCustomKeyStore",
        "ec2:AuthorizeSecurityGroupEgress",
        "ec2:AuthorizeSecurityGroupIngress",
    ]
    actions_template["actions"].extend(actions_to_add)
    policy = write_policy_with_template(actions_template)
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
