#!/usr/bin/env python

from policy_sentry.querying.all import get_all_actions


if __name__ == '__main__':

    all_actions = get_all_actions()
    print(all_actions)

"""
Output:

Every IAM action available across all services, without duplicates
"""
