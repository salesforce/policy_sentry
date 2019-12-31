#! /usr/bin/env python
"""NOTE: The next few lines until the `from policy_sentry`...  are included just
so that it can run without installing the PyPi package, and can run from the Git repo instead.
You do not need to include it when you leverage policy sentry as a third party package"""
# These lines
import sys
import os
from pathlib import Path
sys.path.append(str(Path(Path(os.path.dirname(__file__)).parent).parent))
"""NOTE: The rest of this file is the example code"""
from policy_sentry.shared.database import connect_db
from policy_sentry.querying.actions import get_actions_for_service


def example():
    db_session = connect_db('bundled')  # This is the critical line. You just need to specify `'bundled'` as the parameter.
    actions = get_actions_for_service(db_session, 'cloud9')  # Then you can leverage any method that requires access to the database.
    for action in actions:
        print(action)


if __name__ == '__main__':
    example()
