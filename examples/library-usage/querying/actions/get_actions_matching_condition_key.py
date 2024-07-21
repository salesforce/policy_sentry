#!/usr/bin/env python

import json

from policy_sentry.querying.actions import get_actions_matching_condition_key

if __name__ == "__main__":
    output = get_actions_matching_condition_key("ses", "ses:FeedbackAddress")
    print(json.dumps(output, indent=4))

"""
Output:

[
    'ses:sendemail',
    'ses:sendbulktemplatedemail',
    'ses:sendcustomverificationemail',
    'ses:sendemail',
    'ses:sendrawemail',
    'ses:sendtemplatedemail'
]
"""
