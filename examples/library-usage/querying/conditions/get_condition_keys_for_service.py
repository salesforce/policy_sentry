#!/usr/bin/env python
from policy_sentry.shared.database import connect_db
from policy_sentry.querying.conditions import get_condition_keys_for_service


if __name__ == '__main__':
    db_session = connect_db('bundled')
    output = get_condition_keys_for_service(db_session, "cloud9")
    print(output)

"""
Output:

[
    'cloud9:EnvironmentId',
    'cloud9:EnvironmentName',
    'cloud9:InstanceType',
    'cloud9:Permissions',
    'cloud9:SubnetId',
    'cloud9:UserArn'
]
"""
