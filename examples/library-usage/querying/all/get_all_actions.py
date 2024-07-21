#!/usr/bin/env python

from policy_sentry.querying.all import get_all_actions

if __name__ == "__main__":
    all_actions = get_all_actions()  # returns a set
    all_actions = list(all_actions)  # convert to list
    all_actions.sort()  # sort in alphabetical order
    print(all_actions)  # print

"""
Output:

Every IAM action available across all services, without duplicates
"""
