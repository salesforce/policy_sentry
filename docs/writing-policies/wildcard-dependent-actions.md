
In basic CRUD mode, Policy Sentry will also include any dependent actions recommended by AWS. Dependent actions are defined as "any additional permissions that you must have, 
in addition to the permission for the action itself, to successfully call the action." By default, these will be added with a wildcard, which could lead to a policy becoming more
permissive than intended especially if you're not using the action that brought along the dependent one.

If there is a case where you notice more actions than intended are making their way into your IAM policy, it could be because of dependent actions and there is a way to toggle this feature.
**Note:** This only applies to dependent actions that do not match the same resource type you specify in the YAML.

The `wildcard-dependent-actions` key allows you to do this. (by default, it is set to `true`)

You can specify that you don't want to include dependent actions as wildcard in the resulting policy. See the examples below.

### Default Behavior
`wildcard-dependent-actions: true` or not included in the crud template.

**Input**:

```yaml
mode: crud
write:
- arn:aws:s3:::example-org-s3-access-logs
- arn:aws:s3:::example-org-s3-access-logs/*
wildcard-dependent-actions: true
```

**Output**

As you can see the `wildcard-dependent-actions` key is set to `true`, we are using Policy Sentry's default behavior to include dependent actions as wildcards. The resulting policy will include any dependent actions that are
specified by AWS for the action to be called. For reference, `s3:PutReplicationConfiguration` has a dependent action `iam:PassRole` according to the documentation.

Notice how we have an extra section in the resulting JSON policy output allowing `iam:PassRole` on any resource:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "MultMultNone",
            "Effect": "Allow",
            "Action": [
                "iam:PassRole"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Sid": "S3WriteBucket",
            "Effect": "Allow",
            "Action": [
                "s3:CreateBucket",
                "s3:DeleteBucket",
                "s3:DeleteBucketWebsite",
                "s3:PutAccelerateConfiguration",
                "s3:PutAnalyticsConfiguration",
                "s3:PutBucketCORS",
                "s3:PutBucketLogging",
                "s3:PutBucketNotification",
                "s3:PutBucketObjectLockConfiguration",
                "s3:PutBucketOwnershipControls",
                "s3:PutBucketRequestPayment",
                "s3:PutBucketVersioning",
                "s3:PutBucketWebsite",
                "s3:PutEncryptionConfiguration",
                "s3:PutIntelligentTieringConfiguration",
                "s3:PutInventoryConfiguration",
                "s3:PutLifecycleConfiguration",
                "s3:PutMetricsConfiguration",
                "s3:PutReplicationConfiguration"
            ],
            "Resource": [
                "arn:aws:s3:::example-org-s3-access-logs"
            ]
        },
        {
            "Sid": "S3WriteObject",
            "Effect": "Allow",
            "Action": [
                "s3:AbortMultipartUpload",
                "s3:DeleteObject",
                "s3:DeleteObjectVersion",
                "s3:PutObject",
                "s3:PutObjectLegalHold",
                "s3:PutObjectRetention",
                "s3:ReplicateDelete",
                "s3:ReplicateObject",
                "s3:RestoreObject"
            ],
            "Resource": [
                "arn:aws:s3:::example-org-s3-access-logs/*"
            ]
        }
    ]
}
```

### Toggle Behavior
`wildcard-dependent-actions: false`

**Input**:

```yaml
mode: crud
write:
- arn:aws:s3:::example-org-s3-access-logs
- arn:aws:s3:::example-org-s3-access-logs/*
wildcard-dependent-actions: false
```

**Output**

As you can see the `wildcard-dependent-actions` key is set to `false`, we are telling Policy Sentry to not include dependent actions. The resulting policy should not include any dependent actions that would normally be generated if `wildcard-dependent-actions` was set to `true` (the default):
* `iam:PassRole`

Notice how none of those actions are included in the resulting JSON policy output below:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "S3WriteBucket",
            "Effect": "Allow",
            "Action": [
                "s3:CreateBucket",
                "s3:DeleteBucket",
                "s3:DeleteBucketWebsite",
                "s3:PutAccelerateConfiguration",
                "s3:PutAnalyticsConfiguration",
                "s3:PutBucketCORS",
                "s3:PutBucketLogging",
                "s3:PutBucketNotification",
                "s3:PutBucketObjectLockConfiguration",
                "s3:PutBucketOwnershipControls",
                "s3:PutBucketRequestPayment",
                "s3:PutBucketVersioning",
                "s3:PutBucketWebsite",
                "s3:PutEncryptionConfiguration",
                "s3:PutIntelligentTieringConfiguration",
                "s3:PutInventoryConfiguration",
                "s3:PutLifecycleConfiguration",
                "s3:PutMetricsConfiguration",
                "s3:PutReplicationConfiguration"
            ],
            "Resource": [
                "arn:aws:s3:::example-org-s3-access-logs"
            ]
        },
        {
            "Sid": "S3WriteObject",
            "Effect": "Allow",
            "Action": [
                "s3:AbortMultipartUpload",
                "s3:DeleteObject",
                "s3:DeleteObjectVersion",
                "s3:PutObject",
                "s3:PutObjectLegalHold",
                "s3:PutObjectRetention",
                "s3:ReplicateDelete",
                "s3:ReplicateObject",
                "s3:RestoreObject"
            ],
            "Resource": [
                "arn:aws:s3:::example-org-s3-access-logs/*"
            ]
        }
    ]
}
```
