#!/usr/bin/env python
from policy_sentry.shared.database import connect_db
from policy_sentry.querying.all import get_all_service_prefixes


if __name__ == '__main__':
    db_session = connect_db('bundled')
    all_service_prefixes = get_all_service_prefixes(db_session)
    print(all_service_prefixes)

"""
Output:

A list of every service prefix (like 'kms' or 's3') available in the IAM database.
Note that this will not include services that do not support any ARN types, like AWS IQ.
"""
