
Example: Wildcard-only - Single Actions
-----------------------------------------

This is for actions that do not support resource ARN constraints, such as secretsmanager:CreateSecret.

**Input**:

```yaml
mode: crud
wildcard-only:
    single-actions:
    - secretsmanager:CreateSecret
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
                "secretsmanager:CreateSecret"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```
