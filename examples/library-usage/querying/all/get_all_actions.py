#!/usr/bin/env python
from policy_sentry.shared.database import connect_db
from policy_sentry.querying.all import get_all_actions


if __name__ == '__main__':
    db_session = connect_db('bundled')
    all_actions = get_all_actions(db_session)
    print(all_actions)

"""
Output:

Every IAM action available across all services, without duplicates
"""
