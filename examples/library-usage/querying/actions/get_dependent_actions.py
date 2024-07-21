#!/usr/bin/env python

import json

from policy_sentry.querying.actions import get_dependent_actions

if __name__ == "__main__":
    output = get_dependent_actions(["ec2:associateiaminstanceprofile"])
    print(json.dumps(output, indent=4))

"""
Output:

[
    "iam:passrole"
]
"""
