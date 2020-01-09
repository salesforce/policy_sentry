#!/usr/bin/env python
from policy_sentry.shared.database import connect_db
from policy_sentry.querying.actions import get_dependent_actions
import json

if __name__ == '__main__':
    db_session = connect_db('bundled')
    output = get_dependent_actions(db_session, ["ec2:associateiaminstanceprofile"])
    print(json.dumps(output, indent=4))

"""
Output:

[
    "ec2:associateiaminstanceprofile",
    "iam:passrole"
]
"""
