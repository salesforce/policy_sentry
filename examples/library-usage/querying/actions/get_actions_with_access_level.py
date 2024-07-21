#!/usr/bin/env python

import json

from policy_sentry.querying.actions import get_actions_with_access_level

if __name__ == "__main__":
    output = get_actions_with_access_level("s3", "Permissions management")
    print(json.dumps(output, indent=4))

"""
Output:

    s3:bypassgovernanceretention
    s3:deleteaccesspointpolicy
    s3:deletebucketpolicy
    s3:objectowneroverridetobucketowner
    s3:putaccesspointpolicy
    s3:putaccountpublicaccessblock
    s3:putbucketacl
    s3:putbucketpolicy
    s3:putbucketpublicaccessblock
    s3:putobjectacl
    s3:putobjectversionacl
"""
