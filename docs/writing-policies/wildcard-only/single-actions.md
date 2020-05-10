
### Basic support for Wildcard-only Actions

As you can see from the previous example, there are definitely valid use cases for providing access to IAM Actions that do not support resource constraints (i.e., where the Action must be set to `"Resource": "*"`).

**Single IAM Actions**

Previous to version 0.7.1, the user still had to provide specific IAM actions in that section. That is still supported, using the single-actions array under the wildcard-only map, as shown in the example crud.yml below.

```yaml
mode: crud
name: myRole
wildcard-only:
  single-actions:
  - 's3:ListAllMyBuckets'
```

The resulting policy would look like this:

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

And what's really cool about that - if the user tries to bypass it by supplying an action that supports resource constraints (like `secretsmanager:DeleteSecret`), Policy Sentry will ignore the user's request. Consider a file titled crud.yml with the contents below:

```yaml
mode: crud
name: myRole
wildcard-only:
  single-actions:
  - 's3:ListAllMyBuckets'
  - 'secretsmanager:DeleteSecret'  # Policy Sentry will ignore this!
```

Now run the command:

```bash
policy_sentry write-policy --input-file crud.yml
```

Notice how the output does not include `secretsmanager:DeleteSecret`:

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
