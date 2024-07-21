#!/usr/bin/env python

import json

from policy_sentry.analysis.analyze import determine_actions_to_expand
from policy_sentry.util.policy_files import get_actions_from_policy

POLICY_JSON_TO_EXPAND = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "cloud9:*",
            ],
            "Resource": "*",
        }
    ],
}


if __name__ == "__main__":
    requested_actions = get_actions_from_policy(POLICY_JSON_TO_EXPAND)
    expanded_actions = determine_actions_to_expand(requested_actions)
    print(json.dumps(expanded_actions, indent=4))


"""
Output:

[
    "cloud9:createenvironmentec2",
    "cloud9:createenvironmentmembership",
    "cloud9:deleteenvironment",
    "cloud9:deleteenvironmentmembership",
    "cloud9:describeenvironmentmemberships",
    "cloud9:describeenvironments",
    "cloud9:describeenvironmentstatus",
    "cloud9:getusersettings",
    "cloud9:listenvironments",
    "cloud9:updateenvironment",
    "cloud9:updateenvironmentmembership",
    "cloud9:updateusersettings"
]
"""
