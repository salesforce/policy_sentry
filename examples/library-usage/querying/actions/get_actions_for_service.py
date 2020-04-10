#!/usr/bin/env python
from policy_sentry.querying.actions import get_actions_for_service
import json

if __name__ == '__main__':
    output = get_actions_for_service('cloud9')
    print(json.dumps(output, indent=4))

"""
Output:

[
    'ram:acceptresourceshareinvitation',
    'ram:associateresourceshare',
    'ram:createresourceshare',
    'ram:deleteresourceshare',
    'ram:disassociateresourceshare',
    'ram:enablesharingwithawsorganization',
    'ram:rejectresourceshareinvitation',
    'ram:updateresourceshare'
]
"""
