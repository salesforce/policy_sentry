Assume Role Actions
============

Using CRUD mode, you can add STS assume role actions to your larger CRUD policy by using the `sts` section.

**Input**:

```yaml
mode: crud
sts:
  assume-role:
    - arn:aws:iam::123456789012:role/demo
    - arn:aws:iam::123456789012:role/demo2
  assume-role-with-saml:
    - arn:aws:iam::123456789012:role/demo3
  assume-role-with-web-identity:
    - 'arn:aws:iam::123456789012:role/demo'
```

**Output**:

```json
{
    "Sid": "AssumeRole",
    "Effect": "Allow",
    "Action": [
        "sts:AssumeRole"
    ],
    "Resource": [
        "arn:aws:iam::123456789012:role/demo",
        "arn:aws:iam::123456789012:role/demo2"
    ]
},
{
    "Sid": "AssumeRoleWithSAML",
    "Effect": "Allow",
    "Action": [
        "sts:AssumeRoleWithSAML"
    ],
    "Resource": [
        "arn:aws:iam::123456789012:role/demo3"
    ]
},
{
    "Sid": "AssumeRoleWithWebIdentity",
    "Effect": "Allow",
    "Action": [
        "sts:AssumeRoleWithWebIdentity"
    ],
    "Resource": [
        "arn:aws:iam::123456789012:role/demo"
    ]
}
```
