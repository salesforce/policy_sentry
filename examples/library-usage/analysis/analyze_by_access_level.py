#!/usr/bin/env python
from policy_sentry.analysis.analyze import analyze_by_access_level
import json

if __name__ == '__main__':
    permissions_management_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    # These ones are Permissions management
                    "ecr:SetRepositoryPolicy",
                    "secretsmanager:DeleteResourcePolicy",
                    "iam:UpdateAccessKey",
                    # These ones are not permissions management
                    "ecr:GetRepositoryPolicy",
                    "ecr:DescribeRepositories",
                    "ecr:ListImages",
                    "ecr:DescribeImages",
                ],
                "Resource": "*"
            }
        ]
    }
    permissions_management_actions = analyze_by_access_level(permissions_management_policy, "Permissions management")
    print(json.dumps(permissions_management_actions, indent=4))

"""
Output:

[
    'ecr:setrepositorypolicy',
    'iam:updateaccesskey',
    'secretsmanager:deleteresourcepolicy'
]
"""
