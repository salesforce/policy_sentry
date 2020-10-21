import unittest
import json
import os
from policy_sentry.writing.sid_group import SidGroup

crud_with_override_template = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        os.path.pardir,
        os.path.pardir,
        "examples",
        "crud-with-override.yml",
    )
)


class SidGroupActionsTestCase(unittest.TestCase):
    def test_actions_test_case(self):
        cfg = {
            "mode": "actions",
            "name": "RoleNameWithCRUD",
            "actions": [
                "codestar-connections:UseConnection",
                "kms:CreateGrant",
                "kms:CreateCustomKeyStore",
                "ec2:AuthorizeSecurityGroupEgress",
                "ec2:AuthorizeSecurityGroupIngress",
            ],
        }
        sid_group = SidGroup()
        output = sid_group.process_template(cfg)
        # print(json.dumps(output, indent=4))
        desired_output = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "CodestarconnectionsReadConnection",
                    "Effect": "Allow",
                    "Action": [
                        "codestar-connections:UseConnection"
                    ],
                    "Resource": [
                        "arn:${Partition}:codestar-connections:${Region}:${Account}:connection/${ConnectionId}"
                    ]
                },
                {
                    "Sid": "KmsPermissionsmanagementKey",
                    "Effect": "Allow",
                    "Action": [
                        "kms:CreateGrant"
                    ],
                    "Resource": [
                        "arn:${Partition}:kms:${Region}:${Account}:key/${KeyId}"
                    ]
                },
                {
                    "Sid": "MultMultNone",
                    "Effect": "Allow",
                    "Action": [
                        "cloudhsm:DescribeClusters",
                        "kms:CreateCustomKeyStore"
                    ],
                    "Resource": [
                        "*"
                    ]
                },
                {
                    "Sid": "Ec2WriteSecuritygroup",
                    "Effect": "Allow",
                    "Action": [
                        "ec2:AuthorizeSecurityGroupEgress",
                        "ec2:AuthorizeSecurityGroupIngress"
                    ],
                    "Resource": [
                        "arn:${Partition}:ec2:${Region}:${Account}:security-group/${SecurityGroupId}"
                    ]
                }
            ]
        }
        self.maxDiff = None
        # print(json.dumps(output, indent=4))
        self.assertDictEqual(output, desired_output)

