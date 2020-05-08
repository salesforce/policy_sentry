* To generate a policy according to resources and access levels, start by
creating a template with this command so you can just fill out the ARNs:

```bash
policy_sentry create-template --output-file crud.yml --template-type crud
```

* It will generate a file like this:

```yaml
mode: crud
name: ''
# Specify resource ARNs
read:
- ''
write:
- ''
list:
- ''
tagging:
- ''
permissions-management:
- ''
# Skip resource constraint requirements by listing actions here.
skip-resource-constraints:
- ''
# Actions that do not support resource constraints
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

* Copy/paste the ARNs you want to include in your policy. You can delete lines that you don't use, or just leave them there.

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

* Then run this command:

```bash
policy_sentry write-policy --input-file crud.yml
```

* It will generate these results:

```json
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
```

Notice how the policy above recognizes the ARNs that the user supplies,
along with the requested access level. For instance, the SID
`SecretsmanagerTaggingSecret` contains Tagging actions that are assigned
to the secret resource type only.

This rapidly speeds up the time to develop IAM policies, and ensures
that all policies created limit access to exactly what your role needs
access to. This way, developers only have to determine the resources
that they need to access, and we abstract the complexity of IAM policies
away from their development processes.
