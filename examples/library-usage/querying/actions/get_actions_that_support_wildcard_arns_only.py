#!/usr/bin/env python

from policy_sentry.querying.actions import get_actions_that_support_wildcard_arns_only
import json

if __name__ == '__main__':

    output = get_actions_that_support_wildcard_arns_only("secretsmanager")
    print(json.dumps(output, indent=4))

"""
Output:

[
    "secretsmanager:createsecret",
    "secretsmanager:getrandompassword",
    "secretsmanager:listsecrets"
]
"""
