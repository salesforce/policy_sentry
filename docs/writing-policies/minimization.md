Character Minimization
======================

IAM Policies have character limits, which apply to individual policies, and there are also limits on the total aggregate policy sizes. As such, it is not possible to use exhaustive list of explicit IAM actions. To have granular control of specific IAM policies, we must use wildcards on IAM Actions, only in a programmatic manner.

This is typically performed by humans by reducing policies to `s3:Get*`, `ec2:Describe*`, and other approaches of the sort.

We borrow some strategies from Netflix's PolicyUniverse[1](https://github.com/Netflix-Skunkworks/policyuniverse/) for this. Let's see it in action, using the same template as the CRUD example.

## Input

* Use this as your `crud.yml` file:

```yaml
mode: crud
name: ''
read:
- 'arn:aws:ssm:us-east-1:123456789012:parameter/myparameter'
write:
- 'arn:aws:ssm:us-east-1:123456789012:parameter/myparameter'
list:
- 'arn:aws:ssm:us-east-1:123456789012:parameter/myparameter'
tagging:
- 'arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret'
permissions-management:
- 'arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret'
wildcard-only:
  single-actions: # standalone actions
  - ''
  # Service-wide - like 's3' or 'ec2'
  service-read:
  - ''
  service-write:
  - ''
  service-list:
  - ''
  service-tagging:
  - ''
  service-permissions-management:
  - ''
```


## Output - with character minimization

* To write the policy **with** Character minimization run this command:

```bash
policy_sentry write-policy --input-file crud.yml --minimize 0
```

The output has **500 characters** (not counting whitespaces) and will look like this:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "SsmMultParametermyparameter",
            "Effect": "Allow",
            "Action": [
                "ssm:getpar*",
                "ssm:deletepar*",
                "ssm:la*",
                "ssm:putp*",
                "ssm:listt*"
            ],
            "Resource": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter"
            ]
        },
        {
            "Sid": "SecretsmanagerMultSecretmysecret",
            "Effect": "Allow",
            "Action": [
                "secretsmanager:t*",
                "secretsmanager:un*",
                "secretsmanager:deleter*",
                "secretsmanager:putr*",
                "secretsmanager:v*"
            ],
            "Resource": [
                "arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"
            ]
        }
    ]
}
```

## Output - without character minimization


* To write the policy **without** Character minimization run this command:

```bash
policy_sentry write-policy --input-file crud.yml
```

* The output has **935 characters** and will look like this:

<details open>
<summary>policy_sentry query action-table --service all</summary>
<br>
<pre>
<code>
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "SsmReadParameter",
            "Effect": "Allow",
            "Action": [
                "ssm:GetParameter",
                "ssm:GetParameterHistory",
                "ssm:GetParameters",
                "ssm:GetParametersByPath",
                "ssm:ListTagsForResource"
            ],
            "Resource": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter"
            ]
        },
        {
            "Sid": "SsmWriteParameter",
            "Effect": "Allow",
            "Action": [
                "ssm:DeleteParameter",
                "ssm:DeleteParameters",
                "ssm:LabelParameterVersion",
                "ssm:PutParameter"
            ],
            "Resource": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter"
            ]
        },
        {
            "Sid": "SecretsmanagerPermissionsmanagementSecret",
            "Effect": "Allow",
            "Action": [
                "secretsmanager:DeleteResourcePolicy",
                "secretsmanager:PutResourcePolicy"
            ],
            "Resource": [
                "arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"
            ]
        },
        {
            "Sid": "SecretsmanagerTaggingSecret",
            "Effect": "Allow",
            "Action": [
                "secretsmanager:TagResource",
                "secretsmanager:UntagResource"
            ],
            "Resource": [
                "arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"
            ]
        }
    ]
}
</code>
</pre>
</details>


## Conclusion

As you can see, we used the minimization command to shave off 200 characters from the resulting IAM policy.

This becomes more and more useful as the amount of ARNs used in the policy add up.
