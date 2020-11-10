# Policy Sentry

IAM Least Privilege Policy Generator.

[![continuous-integration](https://github.com/salesforce/policy_sentry/workflows/continuous-integration/badge.svg?)](https://github.com/salesforce/policy_sentry/actions?query=workflow%3Acontinuous-integration)
[![Documentation Status](https://readthedocs.org/projects/policy-sentry/badge/?version=latest)](https://policy-sentry.readthedocs.io/en/latest/?badge=latest)
[![Join the chat at https://gitter.im/salesforce/policy_sentry](https://badges.gitter.im/salesforce/policy_sentry.svg)](https://gitter.im/salesforce/policy_sentry?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Downloads](https://pepy.tech/badge/policy-sentry)](https://pepy.tech/project/policy-sentry)

![](https://raw.githubusercontent.com/salesforce/policy_sentry/master/examples/asciinema/policy_sentry.gif)

- [Tutorial](#tutorial)
  * [Installation](#installation)
    + [Package managers](#package-managers)
    + [Shell completion](#shell-completion)
  * [Step 1: Create the Template](#step-1--create-the-template)
  * [Step 2: Copy/paste ARNs](#step-2--copy-paste-arns)
  * [Step 3: Write-policy command](#step-3--write-policy-command)
- [Cheat sheets](#cheat-sheets)
  * [Policy Writing cheat sheet](#policy-writing-cheat-sheet)
  * [IAM Database Query Cheat Sheet](#iam-database-query-cheat-sheet)
  * [Local Initialization (Optional)](#local-initialization--optional-)
- [Other Usage](#other-usage)
  * [Commands](#commands)
  * [Python Library usage](#python-library-usage)
  * [Docker](#docker)
  * [Terraform](#terraform)
- [References](#references)

## Documentation

For walkthroughs and full documentation, please visit the [project on ReadTheDocs](https://policy-sentry.readthedocs.io/en/latest/index.html).

See the [Salesforce Engineering Blog post](https://engineering.salesforce.com/salesforce-cloud-security-automating-least-privilege-in-aws-iam-with-policy-sentry-b04fe457b8dc) on Policy Sentry.

## Overview

Writing security-conscious IAM Policies by hand can be very tedious and inefficient. Many Infrastructure as Code developers have experienced something like this:

 * Determined to make your best effort to give users and roles the least amount of privilege you need to perform your duties, you spend way too much time combing through the AWS IAM Documentation on [Actions, Resources, and Condition Keys for AWS Services][1].
 * Your team lead encourages you to build security into your IAM Policies for product quality, but eventually you get frustrated due to project deadlines.
 * You don't have an embedded security person on your team who can write those IAM policies for you, and there's no automated tool that will automagically sense the AWS API calls that you perform and then write them for you in a least-privilege manner.
 * After fantasizing about that level of automation, you realize that writing least privilege IAM Policies, seemingly out of charity, will jeopardize your ability to finish your code in time to meet project deadlines.
 * You use Managed Policies (because hey, why not) or you eyeball the names of the API calls and use wildcards instead so you can move on with your life.

Such a process is not ideal for security or for Infrastructure as Code developers. We need to make it easier to write IAM Policies securely and abstract the complexity of writing least-privilege IAM policies. That's why I made this tool.

Policy Sentry allows users to create least-privilege IAM policies in a matter of seconds, rather than tediously writing IAM policies by hand. These policies are scoped down according to access levels and resources. In the case of a breach, this helps to limit the blast radius of compromised credentials by only giving IAM principals access to what they need.

**Before this tool, it could take hours to craft an IAM Policy with resource ARN constraints — but now it can take a matter of seconds**. This way, developers only have to determine the resources that they need to access, and **Policy Sentry abstracts the complexity of IAM policies** away from their development processes.

### Writing Secure Policies based on Resource Constraints and Access Levels

Policy Sentry's flagship feature is that it can create IAM policies based on resource ARNs and access levels. Our CRUD functionality takes the opinionated approach that IAC developers shouldn't have to understand the complexities of AWS IAM - we should abstract the complexity for them. In fact, developers should just be able to say...

* "I need Read/Write/List access to `arn:aws:s3:::example-org-sbx-vmimport`"
* "I need Permissions Management access to `arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret`"
* "I need Tagging access to `arn:aws:ssm:us-east-1:123456789012:parameter/test`"

...and our automation should create policies that correspond to those access levels.

How do we accomplish this? Well, Policy Sentry leverages the AWS documentation on [Actions, Resources, and Condition Keys][1] documentation to look up the actions, access levels, and resource types, and generates policies according to the ARNs and access levels. Consider the table snippet below:

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

Policy Sentry aggregates all of that documentation into a single database and uses that database to generate policies according to actions, resources, and access levels.

## Tutorial


### Installation

#### Package managers

* Homebrew

```bash
brew tap salesforce/policy_sentry https://github.com/salesforce/policy_sentry
brew install policy_sentry
```

* Pip

```bash
pip3 install --user policy_sentry
```

#### Shell completion

To enable Bash completion, put this in your `.bashrc`:

```bash
eval "$(_POLICY_SENTRY_COMPLETE=source policy_sentry)"
```

To enable ZSH completion, put this in your `.zshrc`:

```
eval "$(_POLICY_SENTRY_COMPLETE=source_zsh policy_sentry)"
```

### Step 1: Create the Template

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
# Skip resource constraint requirements by listing actions here.
skip-resource-constraints:
- ''
# Exclude actions from the output by specifying them here. Accepts wildcards, like kms:Delete*
exclude-actions:
- ''
```

### Step 2: Copy/paste ARNs

* Copy/paste the ARNs you want to include in your policy. You can delete lines that you don't use, or just leave them there.

```yaml
mode: crud
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

### Step 3: Write-policy command

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

Notice how the policy above recognizes the ARNs that the user supplies, along with the requested access level. For instance, the SID `SecretsmanagerTaggingSecret` contains Tagging actions that are assigned to the secret resource type only.

This rapidly speeds up the time to develop IAM policies, and ensures that all policies created limit access to exactly what your role needs access to. This way, developers only have to determine the resources that they need to access, and we abstract the complexity of IAM policies away from their development processes.

## Cheat sheets

### Policy Writing cheat sheet

```bash
# Create templates first!!! This way you can just paste the values you need rather than remembering the YAML format
# CRUD mode
policy_sentry create-template --output-file tmp.yml --template-type crud
# Actions mode
policy_sentry create-template --output-file tmp.yml --template-type actions

# Write policy based on resource-specific access levels
policy_sentry write-policy --input-file examples/yml/crud.yml

# Write policy based on a list of actions
policy_sentry write-policy --input-file examples/yml/actions.yml
```

### IAM Database Query Cheat Sheet

```bash

###############
# Actions Table
###############
# NOTE: Use --fmt yaml or --fmt json to change the output format. Defaults to json for querying

# Get a list of actions that do not support resource constraints
policy_sentry query action-table --service s3 --wildcard-only --fmt yaml

# Get a list of actions at the "Write" level in S3 that do not support resource constraints
policy_sentry query action-table --service s3 --access-level write --wildcard-only --fmt yaml

# Get a list of all IAM actions across ALL services that have "Permissions management" access
policy_sentry query action-table --service all --access-level permissions-management

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

### Local Initialization (Optional)

```bash
# Initialize the policy_sentry config folder and create the IAM database tables.
policy_sentry initialize

# Fetch the most recent version of the AWS documentation so you can experiment with new services.
policy_sentry initialize --fetch

# Override the Access Levels by specifying your own Access Levels (example:, correcting Permissions management levels)
policy_sentry initialize --access-level-overrides-file ~/.policy_sentry/overrides-resource-policies.yml

policy_sentry initialize --access-level-overrides-file ~/.policy_sentry/access-level-overrides.yml
```

## Other Usage

### Commands

* `create-template`: Creates the YML file templates for use in the `write-policy` command types.

* `write-policy`: Leverage a YAML file to write policies for you
  - Option 1: Specify CRUD levels (Read, Write, List, Tagging, or Permissions management) and the ARN of the resource. It will write this for you. See the [documentation][13]
  - Option 2: Specify a list of actions. It will write the IAM Policy for you, but you will have to fill in the ARNs. See the [documentation][14].

* `query`: Query the IAM database tables. This can help when filling out the Policy Sentry templates, or just querying the database for quick knowledge.
  - Option 1: Query the Actions Table (`action-table`)
  - Option 2: Query the ARNs Table (`arn-table`)
  - Option 3: Query the Conditions Table (`condition-table`)

* `initialize`: (Optional). Create a SQLite database that contains all of the services available through the [Actions, Resources, and Condition Keys documentation][1]. See the [documentation][12].

### Python Library usage

If you are developing your own Python code and you want to import Policy Sentry as a third party package, you can skip the initialization and leverage the local database file that is bundled with the Python package itself.

This is especially useful for developers who wish to leverage Policy Sentry’s capabilities that require the use of the IAM database (such as querying the IAM database table). This way, you don’t have to initialize the database and can just query it immediately.

The code example is located [here](https://github.com/salesforce/policy_sentry/blob/master/examples/library-usage/example.py). It is also shown below.

```python
from policy_sentry.querying.actions import get_actions_for_service


def example():
    actions = get_actions_for_service('cloud9')  # Then you can leverage any method that requires access to the database.
    for action in actions:
        print(action)

if __name__ == '__main__':
    example()
```

The results will look like:

```
cloud9:CreateEnvironmentEC2
cloud9:CreateEnvironmentMembership
cloud9:DeleteEnvironment
cloud9:DeleteEnvironmentMembership
cloud9:DescribeEnvironmentMemberships
cloud9:DescribeEnvironmentStatus
cloud9:DescribeEnvironments
cloud9:GetUserSettings
cloud9:ListEnvironments
cloud9:ListTagsForResource
cloud9:TagResource
cloud9:UntagResource
cloud9:UpdateEnvironment
cloud9:UpdateEnvironmentMembership
cloud9:UpdateUserSettings
```

### Docker

If you prefer using Docker instead of installing the script with Python, we support that as well. From the root of the repository, use this to build the docker image:

```bash
docker build -t kmcquade/policy_sentry .
```

Use this to run some basic commands:

```bash
# Basic commands with no arguments
docker run -i --rm kmcquade/policy_sentry:latest "--help"
docker run -i --rm kmcquade/policy_sentry:latest "query"

# Query the database
docker run -i --rm kmcquade/policy_sentry:latest "query action-table --service all --access-level permissions-management"
```

The `write-policy` command also supports passing in the YML config via STDIN. If you are using the docker method, try it out here:

```bash
# Write policies by passing in the config via STDIN
cat examples/yml/crud.yml | docker run -i --rm kmcquade/policy_sentry:latest "write-policy"

cat examples/yml/actions.yml | docker run -i --rm kmcquade/policy_sentry:latest "write-policy"
```

### Terraform

The Terraform module is published and maintained [here](https://github.com/salesforce/policy_sentry/tree/master/terraform_module).

## References

* The document scraping process was inspired and borrowed from a similar [ansible hacking script][3].
* [Identity-Based vs Resource-based policies][5]
* [Actions, Resources, and Condition Keys for AWS Services][7]

[1]: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html
[2]: https://nose.readthedocs.io/en/latest/
[3]: https://github.com/ansible/ansible/blob/stable-2.9/hacking/aws_config/build_iam_policy_framework.py
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
