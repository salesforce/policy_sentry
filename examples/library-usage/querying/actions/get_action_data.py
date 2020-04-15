#!/usr/bin/env python

from policy_sentry.querying.actions import get_action_data
import json

if __name__ == '__main__':

    output = get_action_data('ram', 'createresourceshare')
    print(json.dumps(output, indent=4))

"""
Output:

{
    'ram': [
        {
            'action': 'ram:createresourceshare',
            'description': 'Create resource share with provided resource(s) and/or principal(s)',
            'access_level': 'Permissions management',
            'resource_arn_format': 'arn:${Partition}:ram:${Region}:${Account}:resource-share/${ResourcePath}',
            'condition_keys': [
                'ram:RequestedResourceType',
                'ram:ResourceArn',
                'ram:RequestedAllowsExternalPrincipals'
            ],
            'dependent_actions': None
        },
        {
            'action': 'ram:createresourceshare',
            'description': 'Create resource share with provided resource(s) and/or principal(s)',
            'access_level': 'Permissions management',
            'resource_arn_format': '*',
            'condition_keys': [
                'aws:RequestTag/${TagKey}',
                'aws:TagKeys'
            ],
            'dependent_actions': None
        }
    ]
}
"""
