
Example: Wildcard only - Bulk Selection Service-Wide
------------------------------------------------------

As mentioned before, there are some actions that do not support resource constraints - but all of those actions have access levels. You can use this strategy to "bulk select" wildcard-only actions at different access levels. It improves the user experience so you don't have to actually know the details of individual IAM Actions, just the service prefixes and access levels.

**Input**:

```yaml
mode: crud
wildcard-only:
    service-list:
    - s3
```

**Output**:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "MultMultNone",
            "Effect": "Allow",
            "Action": [
                "s3:ListAllMyBuckets"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```
