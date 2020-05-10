
The basic CRUD mode gives you actions at the specified access level, constrained to the specific resource ARNs supplied.

**Input**:

```yaml
mode: crud
read:
- 'arn:aws:ssm:us-east-1:123456789012:parameter/myparameter'
```

**Output**:

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
        }
    ]
}
```
