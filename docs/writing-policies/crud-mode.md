CRUD Mode
=========

-   **TLDR**: Building IAM policies with resource constraints and access levels.

This is the flagship feature of this tool. You can just specify the CRUD levels (Read, Write, List, Tagging, or Permissions management) for each action in a YAML File. The policy will be generated for you. You might need to fiddle with the results for your use in Terraform, but it significantly reduces the level of effort to build least privilege into your policies.

Command options
---------------

-   `--input-file`: YAML file containing the CRUD levels + Resource ARNs. Required.
-   `--minimize`: Whether or not to minimize the resulting statement with *safe* usage of wildcards to reduce policy length. Set this to the character length you want. This can be extended for readability. I suggest setting it to `0`.
-   `-v`: Set the logging level. Choices are critical, error, warning, info, or debug. Defaults to info

Example:

```bash
policy_sentry write-policy --input-file examples/crud.yml
```

Instructions
------------

-   To generate a policy according to resources and access levels, start by creating a template with this command so you can just fill out the ARNs:

```bash
policy_sentry create-template --output-file crud.yml --template-type crud
```

-   It will generate a file like this:

```yaml
mode: crud
name: myRole
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
# Actions that do not support resource constraints
wildcard-only:
  single-actions: # standalone actions
  - ''
  # Service-wide, per access level - like 's3' or 'ec2'
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

-   Then just fill it out:

```yaml
mode: crud
name: myRole
description: 'Justification for privileges'
role_arn: 'arn:aws:iam::123456789102:role/myRole'
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
```

-   Run the command:

```bash
policy_sentry write-policy --input-file crud.yml
```

-   It will generate an IAM Policy containing an IAM policy with the actions restricted to the ARNs specified above.
-   The resulting policy (without the `--minimize command`) will look like this:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "SsmReadParameter",
            "Effect": "Allow",
            "Action": [
                "ssm:getparameter",
                "ssm:getparameterhistory",
                "ssm:getparameters",
                "ssm:getparametersbypath",
                "ssm:listtagsforresource"
            ],
            "Resource": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter"
            ]
        },
        {
            "Sid": "SsmWriteParameter",
            "Effect": "Allow",
            "Action": [
                "ssm:deleteparameter",
                "ssm:deleteparameters",
                "ssm:putparameter",
                "ssm:labelparameterversion"
            ],
            "Resource": [
                "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter"
            ]
        },
        {
            "Sid": "SecretsmanagerPermissionsmanagementSecret",
            "Effect": "Allow",
            "Action": [
                "secretsmanager:deleteresourcepolicy",
                "secretsmanager:putresourcepolicy"
            ],
            "Resource": [
                "arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"
            ]
        },
        {
            "Sid": "SecretsmanagerTaggingSecret",
            "Effect": "Allow",
            "Action": [
                "secretsmanager:tagresource",
                "secretsmanager:untagresource"
            ],
            "Resource": [
                "arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"
            ]
        }
    ]
}
```

