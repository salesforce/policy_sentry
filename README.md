# Policy Sentry

IAM Least Privilege Policy Generator, auditor, and analysis database.

## Wiki

For walkthroughs and full documentation, please visit the [project on ReadTheDocs](https://policy-sentry.readthedocs.io/en/latest/index.html).

## Overview

Writing security-conscious IAM Policies by hand can be very tedious and inefficient. Many Infrastructure as Code developers have experienced something like this:
 
 * Determined to make your best effort to give users and roles the least amount of privilege you need to perform your duties, you spend way too much time combing through the AWS IAM Documentation on [Actions, Resources, and Condition Keys for AWS Services][1]. 
 * Your team lead encourages you to build security into your IAM Policies for product quality, but eventually you get frustrated due to project deadlines.
 * You don't have an embedded security person on your team who can write those IAM policies for you, and there's no automated tool that will automagically sense the AWS API calls that you perform and then write them for you in a least-privilege manner. 
 * After fantasizing about that level of automation, you realize that writing least privilege IAM Policies, seemingly out of charity, will jeopardize your ability to finish your code in time to meet project deadlines.
 * You use Managed Policies (because hey, why not) or you eyeball the names of the API calls and use wildcards instead so you can move on with your life.
 
Such a process is not ideal for security or for Infrastructure as Code developers. We need to make it easier to write IAM Policies securely and abstract the complexity of writing least-privilege IAM policies. That's why I made this tool.

### Authoring Secure IAM Policies

Policy Sentry's flagship feature is that it can create IAM policies based on resource ARNs and access levels. Our CRUD functionality takes the opinionated approach that IAC developers shouldn't have to understand the complexities of AWS IAM - we should abstract the complexity for them. In fact, developers should just be able to say...

* "I need Read/Write/List access to `arn:aws:s3:::example-org-sbx-vmimport`"
* "I need Permissions Management access to `arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret`"
* "I need Tagging access to `arn:aws:ssm:us-east-1:123456789012:parameter/test`"

...and our automation should create policies that correspond to those access levels. 

How do we accomplish this? Well, Policy Sentry leverages the AWS documentation on [Actions, Resources, and Condition Keys](1) documentation to look up the actions, access levels, and resource types, and generates policies according to the ARNs and access levels. Consider the table snippet below:

<table class="tg">
  <tr>
    <th class="tg-fymr">Actions</th>
    <th class="tg-fymr">Access Level</th>
    <th class="tg-fymr">Resource Types</th>
  </tr>
  <tr>
    <td class="tg-0pky">ssm:GetParameter</td>
    <td class="tg-0pky">Read</td>
    <td class="tg-0pky">parameter</td>
  </tr>
  <tr>
    <td class="tg-0pky">ssm:DescribeParameters</td>
    <td class="tg-0pky">List</td>
    <td class="tg-0pky">parameter</td>
  </tr>
  <tr>
    <td class="tg-0pky">ssm:PutParameter</td>
    <td class="tg-0pky">Write</td>
    <td class="tg-0pky">parameter</td>
  </tr>
  <tr>
    <td class="tg-0pky">secretsmanager:PutResourcePolicy</td>
    <td class="tg-0pky">Permissions management</td>
    <td class="tg-0pky">secret</td>
  </tr>
  <tr>
    <td class="tg-0pky">secretsmanager:TagResource</td>
    <td class="tg-0pky">Tagging</td>
    <td class="tg-0pky">secret</td>
  </tr>
</table>

Policy Sentry aggregates all of that documentation into a single database and uses that database to generate policies according to actions, resources, and access levels. To generate a policy according to resources and access levels, start by creating a template with this command so you can just fill out the ARNs: 

```bash
policy_sentry create-template --name myRole --output-file crud.yml --template-type crud
```

It will generate a file like this:

```yaml
roles_with_crud_levels:
- name: myRole
  description: '' # Insert description
  arn: '' # Insert the ARN of the role that will use this
  read:
    - '' # Insert ARNs for Read access
  write:
    - '' # Insert ARNs...
  list:
    - '' # Insert ARNs...
  tag:
    - '' # Insert ARNs...
  permissions-management:
    - '' # Insert ARNs...
```

Then just fill it out:

```yaml
roles_with_crud_levels:
- name: myRole
  description: 'Justification for privileges'
  arn: 'arn:aws:iam::123456789102:role/myRole'
  read:
    - 'arn:aws:ssm:us-east-1:123456789012:parameter/myparameter'
  write:
    - 'arn:aws:ssm:us-east-1:123456789012:parameter/myparameter'
  list:
    - 'arn:aws:ssm:us-east-1:123456789012:parameter/myparameter'
  tag:
    - 'arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret'
  permissions-management:
    - 'arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret'
```

Then run this command:

```bash
policy_sentry write-policy --crud --input-file crud.yml
```

It will generate these results:

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

Notice how the policy above recognizes the ARNs that the user supplies, along with the requested access level. For instance, the SID “SecretsmanagerTaggingSecret” contains Tagging actions that are assigned to the secret resource type only.

This rapidly speeds up the time to develop IAM policies, and ensures that all policies created limit access to exactly what your role needs access to. This way, developers only have to determine the resources that they need to access, and we abstract the complexity of IAM policies away from their development processes.

## Quickstart

* `policy_sentry` is available via pip. To install, run:

```bash
pip install --user policy_sentry
```

* Policy Writing cheat sheet

```bash
# Initialize the policy_sentry config folder and create the IAM database tables.
policy_sentry initialize

# Create a template file for use in the write-policy command (crud mode)
policy_sentry create-template --name myRole --output-file tmp.yml --template-type crud

# Write policy based on resource-specific access levels
policy_sentry write-policy --crud --file examples/crud.yml

# Write policy_sentry YML files based on resource-specific access levels on a directory basis
policy_sentry write-policy-dir --crud --input-dir examples/input-dir --output-dir examples/output-dir

# Create a template file for use in the write-policy command (actions mode)
policy_sentry create-template --name myRole --output-file tmp.yml --template-type actions

# Write policy based on a list of actions
policy_sentry write-policy --file examples/actions.yml
```

* Policy Analysis Cheat Sheet

```bash
# Initialize the policy_sentry config folder and create the IAM database tables.
policy_sentry initialize

# Analyze a policy FILE to determine actions with "Permissions Management" access levels
policy_sentry analyze-iam-policy --from-access-level permissions-management --file examples/analyze/wildcards.json

# Download customer managed IAM policies from a live account under 'default' profile. By default, it looks for policies that are 1. in use and 2. customer managed
policy_sentry download-policies # this will download to ~/.policy_sentry/accountid/customer-managed/.json

# Download customer-managed IAM policies, including those that are not attached
policy_sentry download-policies --include-unattached # this will download to ~/.policy_sentry/accountid/customer-managed/.json

# Analyze a DIRECTORY of policy files
policy_sentry analyze-iam-policy --show ~/.policy_sentry/123456789012/customer-managed

# Analyze a policy FILE to identify higher-risk IAM calls
policy_sentry analyze-iam-policy --file examples/analyze/wildcards.json

# Analyze a policy against a custom file containing a list of IAM actions
policy_sentry analyze-iam-policy --file examples/analyze/wildcards.json --from-audit-file ~/.policy_sentry/audit/privilege-escalation.txt
```

* IAM Database Query Cheat Sheet

```bash

###############
# Actions Table
###############

# Get a list of all IAM Actions available to the RAM service
policy_sentry query action-table --service ram

# Get details about the `ram:TagResource` IAM Action
policy_sentry query action-table --service ram --name tagresource

# Get a list of all IAM actions under the RAM service that have the Permissions management access level.
policy_sentry query action-table --service ram --access-level permissions-management

# Get a list of all IAM actions under the SES service that support the `ses:FeedbackAddress` condition key.
policy_sentry query action-table --service ses --condition ses:FeedbackAddress

###########
# ARN Table
###########

# Get a list of all RAW ARN formats available through the SSM service.
policy_sentry query arn-table --service ssm

# Get the raw ARN format for the `cloud9` ARN with the short name `environment`
policy_sentry query arn-table --service cloud9 --name environment

# Get key/value pairs of all RAW ARN formats plus their short names
policy_sentry query arn-table --service cloud9 --list-arn-types

######################
# Condition Keys Table
######################

# Get a list of all condition keys available to the Cloud9 service
policy_sentry query condition-table --service cloud9
# Get details on the condition key titled `cloud9:Permissions`
policy_sentry query condition-table --service cloud9 --name cloud9:Permissions
```


## Commands

### Usage
* `initialize`: Create a SQLite database that contains all of the services available through the [Actions, Resources, and Condition Keys documentation][1]. See the [documentation][12].

* `create-template`: Creates the YML file templates for use in the `write-policy` command types.

* `write-policy`: Leverage a YAML file to write policies for you
  - Option 1: Specify CRUD levels (Read, Write, List, Tagging, or Permissions management) and the ARN of the resource. It will write this for you. See the [documentation][13]
  - Option 2: Specify a list of actions. It will write the IAM Policy for you, but you will have to fill in the ARNs. See the [documentation][14].

* `write-policy-dir`: This can be helpful in the Terraform use case. For more information, see the [documentation][15].

* `download-policies`: Download IAM policies from your AWS account for analysis.

* `analyze-iam-policy`: Analyze an IAM policy read from a JSON file, expands the wildcards (like `s3:List*` if necessary.
  - Option 1: Audits them to see if certain IAM actions are permitted, based on actions in a separate text file. See the [documentation][12].
  - Option 2: Audits them to see if any of the actions in the policy meet a certain access level, such as "Permissions management."
  
* `query`: Query the IAM database tables. This can help when filling out the Policy Sentry templates, or just querying the database for quick knowledge.
  - Option 1: Query the Actions Table (`action-table`)
  - Option 2: Query the ARNs Table (`arn-table`)
  - Option 3: Query the Conditions Table (`condition-table`)
  

### Updating the AWS HTML files

Run the following:

```bash
./utils/grab-docs.sh
# Or:
./utils/download-docs.sh
```

## References

* The document scraping process was inspired and borrowed from a similar [ansible hacking script][3].
* [Identity-Based vs Resource-based policies][5]
* [Actions, Resources, and Condition Keys for AWS Services][7]

[1]: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html
[2]: https://nose.readthedocs.io/en/latest/
[3]: https://github.com/ansible/ansible/blob/devel/hacking/aws_config/build_iam_policy_framework.py
[4]: https://github.com/evilpete/aws_access_adviser
[5]: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_identity-vs-resource.html
[6]: https://docs.aws.amazon.com/IAM/latest/APIReference/API_SimulatePrincipalPolicy.html
[7]: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html
[8]: https://docs.aws.amazon.com/awssupport/latest/user/Welcome.html
[9]: https://docs.aws.amazon.com/signer/latest/api/Welcome.html
[10]: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/permissions-reference-cwe.html
[11]: https://docs.aws.amazon.com/IAM/latest/UserGuide/list_awskeymanagementservice.html#awskeymanagementservice-policy-keys
[12]: https://policy-sentry.readthedocs.io/en/latest/user-guide/initialize.html
[13]: https://policy-sentry.readthedocs.io/en/latest/user-guide/write-policy.html#crud-mode-arns-and-access-levels
[14]: https://policy-sentry.readthedocs.io/en/latest/user-guide/write-policy.html#actions-mode-lists-of-iam-actions
[15]: https://policy-sentry.readthedocs.io/en/latest/user-guide/write-policy.html#folder-mode-write-multiple-policies-from-crud-mode-files
