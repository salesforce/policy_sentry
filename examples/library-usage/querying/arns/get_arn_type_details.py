#!/usr/bin/env python
from policy_sentry.shared.database import connect_db
from policy_sentry.querying.arns import get_arn_type_details


if __name__ == '__main__':
    db_session = connect_db('bundled')
    output = get_arn_type_details(db_session, "cloud9", "environment")
    print(output)

"""
Output:

{
    "resource_type_name": "environment",
    "raw_arn": "arn:${Partition}:cloud9:${Region}:${Account}:environment:${ResourceId}",
    "condition_keys": None
}
"""
