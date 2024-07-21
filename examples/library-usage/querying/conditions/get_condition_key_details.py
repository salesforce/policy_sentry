#!/usr/bin/env python

import json

from policy_sentry.querying.conditions import get_condition_key_details

if __name__ == "__main__":
    output = get_condition_key_details("cloud9", "cloud9:Permissions")
    print(json.dumps(output, indent=4))

"""
Output:

{
    "name": "cloud9:Permissions",
    "description": "Filters access by the type of AWS Cloud9 permissions",
    "condition_value_type": "string"
}
"""
