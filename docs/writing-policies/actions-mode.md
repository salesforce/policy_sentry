Actions Mode
============

-   **TLDR**: Supply a list of actions in a YAML file and generate the policy accordingly.

Command options
---------------

-   `--input-file`: YAML file containing the list of actions
-   `--minimize`: Whether or not to minimize the resulting statement with *safe* usage of wildcards to reduce policy length. Set this to the character lengh you want - for example, 4
-   `-v`: Set the logging level. Choices are critical, error, warning, info, or debug. Defaults to info

Example:

```bash
policy_sentry write-policy --input-file examples/yml/actions.yml
```

Instructions
------------

-   If you already know the IAM actions, you can just run this command to create a template to fill out:

```bash
policy_sentry create-template --output-file actions.yml --template-type actions
```

-   It will generate a file with contents like this:

```yaml
mode: actions
name: myRole
description: '' # Insert value here
role_arn: '' # Insert value here
actions:
- ''  # Fill in your IAM actions here
```

-   Create a yaml file with the following contents:

```yaml
mode: actions
name: 'RoleNameWithActions'
actions:
- kms:CreateGrant
- kms:CreateCustomKeyStore
- ec2:AuthorizeSecurityGroupEgress
- ec2:AuthorizeSecurityGroupIngress
```

-   Then run this command:

```bash
policy_sentry write-policy --input-file actions.yml
```

-   The output will look like this:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "KmsPermissionsmanagementKey",
            "Effect": "Allow",
            "Action": [
                "kms:creategrant"
            ],
            "Resource": [
                "arn:aws:kms:${Region}:${Account}:key/${KeyId}"
            ]
        },
        {
            "Sid": "Ec2WriteSecuritygroup",
            "Effect": "Allow",
            "Action": [
                "ec2:authorizesecuritygroupegress",
                "ec2:authorizesecuritygroupingress"
            ],
            "Resource": [
                "arn:aws:ec2:${Region}:${Account}:security-group/${SecurityGroupId}"
            ]
        },
        {
            "Sid": "MultMultNone",
            "Effect": "Allow",
            "Action": [
                "kms:createcustomkeystore",
                "cloudhsm:describeclusters"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```
