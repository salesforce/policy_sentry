#!/usr/bin/env python
from policy_sentry.shared.database import connect_db
from policy_sentry.querying.conditions import get_condition_key_details


if __name__ == '__main__':
    db_session = connect_db('bundled')
    output = get_condition_key_details(db_session, "cloud9", "cloud9:Permissions")
    print(output)

"""
Output:

{
    "name": "cloud9:Permissions",
    "description": "Filters access by the type of AWS Cloud9 permissions",
    "condition_value_type": "string"
}
"""
