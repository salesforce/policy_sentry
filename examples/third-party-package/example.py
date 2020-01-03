#! /usr/bin/env python
from policy_sentry.shared.database import connect_db
from policy_sentry.querying.actions import get_actions_for_service, get_actions_with_access_level


def example():
    db_session = connect_db('bundled')  # This is the critical line. You just need to specify `'bundled'` as the parameter.
    print("connected to db")
    actions = get_actions_for_service(db_session, 'cloud9')  # Then you can leverage any method that requires access to the database.
    print(actions)
    actions = get_actions_with_access_level(db_session, 's3', 'Permissions management')
    print(actions)


if __name__ == '__main__':
    print("Executing example")
    example()
    print("Done with example")
