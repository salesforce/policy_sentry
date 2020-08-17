Example: Wildcard only - Bulk Selection Service-Wide
------------------------------------------------------

As mentioned before, there are some actions that do not support resource constraints - but all of those actions have access levels.

For example: notice how the table below - a recreation of the [Actions, Resources, and Condition Keys page for S3](https://docs.aws.amazon.com/IAM/latest/UserGuide/list_amazons3.html) - shows `s3:GetObject` having two potential resource entries - either the `object` resource type (which resembles the raw ARN format of `arn:aws:s3:::${BucketName}/${ObjectName}`) **OR** a wildcard (i.e., any object in any bucket).

Now, with Policy Sentry's CRUD mode, we could create a policy with that action simply by pasting the ARN with that resource type under the `read` key. However, if we wanted the policy to include `s3:ListAllMyBuckets` or `s3:ListAccessPoints`, it's not possible to do it that way, **since those actions do not support resource ARN constraints.**

| Actions               | Resource | Access Level |
|-----------------------|----------|--------------|
| `s3:GetObject`        | object   | Read         |
| `s3:GetObject`        | *        | Read         |
| `s3:ListAllMyBuckets` | *        | List         |
| `s3:ListAccessPoints` | *        | List         |

**Instead**, we can leverage the following keys under `wildcard-only` key:

* `service-read`
* `service-write`
* `service-list`
* `service-tagging`
* `service-permissions-management`

You can use this strategy to "bulk select" wildcard-only actions at different access levels. It improves the user experience so you don't have to actually know the details of individual IAM Actions, just the service prefixes and access levels.

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


### Note: Determining whether or not an AWS service has any actions that do not support resource ARN constraints

If you are doing this manually, and you want to figure out if an AWS service has any IAM actions that do not support resource ARN constraints, we can run the policy sentry query:

```bash
policy_sentry query action-table --service s3 --wildcard-only
```

The output will resemble the following:
```
IAM actions under s3 service that support wildcard resource values only:
[
    "s3:CreateJob",
    "s3:GetAccessPoint",
    "s3:GetAccountPublicAccessBlock",
    "s3:ListAccessPoints",
    "s3:ListAllMyBuckets",
    "s3:ListJobs",
    "s3:PutAccountPublicAccessBlock"
]
```

