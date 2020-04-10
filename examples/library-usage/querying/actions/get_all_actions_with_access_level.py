#!/usr/bin/env python

from policy_sentry.querying.actions import get_actions_with_access_level
import json

if __name__ == '__main__':

    output = get_actions_with_access_level(db_session, 'all', 'Permissions management')
    print(json.dumps(output, indent=4))

"""
Output: Literally all IAM actions that are at the Permissions management access level
"""
