#!/usr/bin/env python

from policy_sentry.querying.arns import get_arn_types_for_service
import json

if __name__ == '__main__':

    output = get_arn_types_for_service("s3")
    print(json.dumps(output, indent=4))

"""
Output:

{
    "accesspoint": "arn:${Partition}:s3:${Region}:${Account}:accesspoint/${AccessPointName}",
    "bucket": "arn:${Partition}:s3:::${BucketName}",
    "object": "arn:${Partition}:s3:::${BucketName}/${ObjectName}",
    "job": "arn:${Partition}:s3:${Region}:${Account}:job/${JobId}",
}
"""
