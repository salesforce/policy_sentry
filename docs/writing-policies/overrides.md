
In basic CRUD mode, Policy Sentry forces you to use resource constraints, but perhaps you do want to allow `kms:Decrypt` to `*` and there are mitigating circumstances that mean it is not a security risk to your organization. For example - let's say that given the context of your organization and its AWS security strategy, you can’t know the KMS Key Alias or Key ID beforehand. However, all of the KMS keys are tightly controlled via resource based policies and provisioned via Terraform/Cloudformation, therefore `kms:Decrypt` is ok. And in order to use Policy Sentry you’d need a way to handle exceptions/overrides.

The `skip-resource-constraints` section allows you to do this.

We avoid abuse by requiring that if you list actions under the `skip-resource-constraints` section, then you should have to list the actions out individually (I.e., don’t allow `s3:*`)

**Input**:

```yaml
mode: crud
skip-resource-constraints:
- s3:GetObject
- s3:PutObject
- ssm:GetParameter
- ssm:GetParameters
```

**Output**:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "SkipResourceConstraints",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "ssm:GetParameter",
                "ssm:GetParameters"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```
