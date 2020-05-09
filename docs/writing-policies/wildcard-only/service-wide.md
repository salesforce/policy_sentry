### CRUD-based support for Wildcard-only Actions

That previous example is very cool - but it's not terribly fast for users to have to run the CLI queries. We decided that it should be even easier than this. If you're using the [Terraform module](https://github.com/kmcquade/terraform-aws-policy-sentry), then *you should never, ever have to query the IAM database*.

Now bear witness to the latest feature addition to Policy Sentry: wildcard-only, CRUD-based, service-specific actions.

```yaml
mode: crud
wildcard-only:
    service-read:
    - ecr           # This will add ecr:GetAuthorizationToken to the policy
    - s3            # This adds s3:GetAccessPoint, s3:GetAccountPublicAccessBlock, s3:ListAccessPoints
```

As shown above, the input only required the user to supply `s3` and `ecr` under the service-read array in the wildcard-only map.

Now run the command:

```bash
policy_sentry write-policy --input-file crud.yml
```

Notice how the output includes *wildcard-only* actions at the *read* access level for the ecr and s3 services:

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
        }
    ]
}
```
