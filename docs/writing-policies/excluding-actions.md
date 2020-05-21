
In basic CRUD mode, Policy Sentry provides a "granular select all" approach, so to speak, by identifying all Access Levels for actions under a Resource ARN.

However, there are sometimes cases where you don't want to select **all** of those actions - you just want some of them.

The `exclude-actions` section allows you to do this.

You can specify actions that you don't want to include in the resulting policy, no matter what. See the example below.

**Input**:

```yaml
mode: crud
write:
- arn:aws:kms:us-east-1:123456789012:key/aaaa-bbbb-cccc
exclude-actions:
- "kms:Delete*"
- "kms:Disable*"
- "kms:Schedule*"
```

**Output**

As you can see in the `exclude-actions` section above, we are telling Policy Sentry to not include `kms:Delete*`, `kms:Disable*`, and `kms:Schedule*`. Notice that each line includes a wildcard (`*`) so you can tell Policy Sentry to exclude actions matching that pattern. The resulting policy should not include any of these actions that would normally be generated if the `exclude-actions` section were not used:

* `kms:DeleteAlias`
* `kms:DeleteImportedKeyMaterial`
* `kms:DisableKey`
* `kms:DisableKeyRotation`
* `kms:ScheduleKeyDeletion`

Notice how none of those actions are included in the resulting JSON policy output below:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "KmsWriteKey",
            "Effect": "Allow",
            "Action": [
                "kms:CancelKeyDeletion",
                "kms:CreateAlias",
                "kms:Decrypt",
                "kms:EnableKey",
                "kms:EnableKeyRotation",
                "kms:Encrypt",
                "kms:GenerateDataKey",
                "kms:GenerateDataKeyPair",
                "kms:GenerateDataKeyPairWithoutPlaintext",
                "kms:GenerateDataKeyWithoutPlaintext",
                "kms:ImportKeyMaterial",
                "kms:ReEncryptFrom",
                "kms:ReEncryptTo",
                "kms:Sign",
                "kms:UpdateAlias",
                "kms:UpdateKeyDescription",
                "kms:Verify"
            ],
            "Resource": [
                "arn:aws:kms:us-east-1:123456789012:key/aaaa-bbbb-cccc"
            ]
        }
    ]
}
```
