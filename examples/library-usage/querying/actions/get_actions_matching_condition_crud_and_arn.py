#!/usr/bin/env python
from policy_sentry.shared.database import connect_db
from policy_sentry.querying.actions import get_actions_matching_condition_crud_and_arn
import json

if __name__ == '__main__':
    db_session = connect_db('bundled')
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
