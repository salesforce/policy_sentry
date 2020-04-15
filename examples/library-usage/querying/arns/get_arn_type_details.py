#!/usr/bin/env python

from policy_sentry.querying.arns import get_arn_type_details
import json

if __name__ == '__main__':

    output = get_arn_type_details("cloud9", "environment")
    print(json.dumps(output, indent=4))

"""
Output:

{
    "resource_type_name": "environment",
    "raw_arn": "arn:${Partition}:cloud9:${Region}:${Account}:environment:${ResourceId}",
    "condition_keys": None
}
"""
