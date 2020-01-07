#!/usr/bin/env python
from policy_sentry.shared.database import connect_db
from policy_sentry.querying.actions import get_dependent_actions


if __name__ == '__main__':
    db_session = connect_db('bundled')
    actions = get_dependent_actions(db_session, ["ec2:associateiaminstanceprofile"])
    print(actions)

"""
Output:

[
    "ec2:associateiaminstanceprofile",
    "iam:passrole"
]
"""
