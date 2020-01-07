#!/usr/bin/env python
from policy_sentry.shared.database import connect_db
from policy_sentry.querying.actions import get_actions_that_support_wildcard_arns_only


if __name__ == '__main__':
    db_session = connect_db('bundled')
    output = get_actions_that_support_wildcard_arns_only(db_session, "secretsmanager")
    print(output)

"""
Output:

[
    "secretsmanager:createsecret",
    "secretsmanager:getrandompassword",
    "secretsmanager:listsecrets"
]
"""
