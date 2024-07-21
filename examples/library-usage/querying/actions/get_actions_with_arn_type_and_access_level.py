#!/usr/bin/env python

import json

from policy_sentry.querying.actions import get_actions_with_arn_type_and_access_level

if __name__ == "__main__":
    output = get_actions_with_arn_type_and_access_level("ram", "resource-share", "Permissions management")
    print(json.dumps(output, indent=4))

"""
Output:

[
    'ram:associateresourceshare',
    'ram:createresourceshare',
    'ram:deleteresourceshare',
    'ram:disassociateresourceshare',
    'ram:updateresourceshare'
]
"""
