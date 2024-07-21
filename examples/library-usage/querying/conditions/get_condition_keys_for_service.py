#!/usr/bin/env python

import json

from policy_sentry.querying.conditions import get_condition_keys_for_service

if __name__ == "__main__":
    output = get_condition_keys_for_service("cloud9")
    print(json.dumps(output, indent=4))

"""
Output:

[
    'cloud9:EnvironmentId',
    'cloud9:EnvironmentName',
    'cloud9:InstanceType',
    'cloud9:Permissions',
    'cloud9:SubnetId',
    'cloud9:UserArn'
]
"""
