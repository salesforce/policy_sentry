#!/usr/bin/env python

from policy_sentry.querying.actions import get_dependent_actions
import json

if __name__ == '__main__':

    output = get_dependent_actions(["ec2:associateiaminstanceprofile"])
    print(json.dumps(output, indent=4))

"""
Output:

[
    "iam:passrole"
]
"""
