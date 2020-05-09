

### Combining approaches

Here's a slightly more complex policy. See the input file crud.yml below:

```yaml
mode: crud
read:
- arn:aws:s3:::example-org-s3-access-logs
wildcard-only:
    service-read:
    - ecr           # This will add ecr:GetAuthorizationToken to the policy
    - s3            # This adds s3:GetAccessPoint, s3:GetAccountPublicAccessBlock, s3:ListAccessPoints
```

After running the command:

```bash
policy_sentry write-policy --input-file crud.yml
```

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "MultMultNone",
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "s3:GetAccessPoint",
                "s3:GetAccountPublicAccessBlock",
                "s3:ListAccessPoints"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Sid": "S3PermissionsmanagementBucket",
            "Effect": "Allow",
            "Action": [
                "s3:DeleteBucketPolicy",
                "s3:PutBucketAcl",
                "s3:PutBucketPolicy",
                "s3:PutBucketPublicAccessBlock"
            ],
            "Resource": [
                "arn:aws:s3:::example-org-s3-access-logs"
            ]
        }
    ]
}
```

And yes, it's all available in the Terraform module :)
