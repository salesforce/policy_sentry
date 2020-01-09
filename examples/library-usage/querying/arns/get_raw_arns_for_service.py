#!/usr/bin/env python
from policy_sentry.shared.database import connect_db
from policy_sentry.querying.arns import get_raw_arns_for_service
import json

if __name__ == '__main__':
    db_session = connect_db('bundled')
    output = get_raw_arns_for_service(db_session, "s3")
    print(json.dumps(output, indent=4))

"""
Output:

[
    "arn:${Partition}:s3:${Region}:${Account}:accesspoint/${AccessPointName}",
    "arn:${Partition}:s3:::${BucketName}",
    "arn:${Partition}:s3:::${BucketName}/${ObjectName}",
    "arn:${Partition}:s3:${Region}:${Account}:job/${JobId}"
]
"""
