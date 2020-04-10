#!/usr/bin/env python

from policy_sentry.querying.actions import get_actions_matching_condition_crud_and_arn
import json

if __name__ == '__main__':

    results = get_actions_matching_condition_crud_and_arn(
        db_session,
        "ram:ResourceArn",
        "Permissions management",
        "arn:${Partition}:ram:${Region}:${Account}:resource-share/${ResourcePath}"
    )
    print(json.dumps(results, indent=4))

"""
Output:

[
    'ram:createresourceshare'
]
"""
