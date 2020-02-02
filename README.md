
# Policy Sentry

IAM Least Privilege Policy Generator, auditor, and analysis database.

[![Build Status](https://travis-ci.org/salesforce/policy_sentry.svg?branch=master)](https://travis-ci.org/salesforce/policy_sentry)
[![Documentation Status](https://readthedocs.org/projects/policy-sentry/badge/?version=latest)](https://policy-sentry.readthedocs.io/en/latest/?badge=latest)
[![Join the chat at https://gitter.im/salesforce/policy_sentry](https://badges.gitter.im/salesforce/policy_sentry.svg)](https://gitter.im/salesforce/policy_sentry?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Downloads](https://pepy.tech/badge/policy-sentry)](https://pepy.tech/project/policy-sentry)

![](http://i.imgur.com/uITz0cM.gif)

- [Documentation](#documentation)
- [Overview](#overview)
  * [Authoring Secure IAM Policies](#authoring-secure-iam-policies)
- [Quickstart](#quickstart)
    + [Installation](#installation)
    + [Shell completion](#shell-completion)
  * [Initialization](#initialization)
  * [Policy Writing cheat sheet](#policy-writing-cheat-sheet)
  * [IAM Database Query Cheat Sheet](#iam-database-query-cheat-sheet)
  * [Policy Analysis Cheat Sheet](#policy-analysis-cheat-sheet)
- [Commands](#commands)
  * [Usage](#usage)
  * [Library usage](#library-usage)
  * [Docker](#docker)
  * [Updating the AWS HTML files](#updating-the-aws-html-files)
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

### Authoring Secure IAM Policies

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

To get started, install Policy Sentry:

```bash
pip3 install --user policy_sentry
```

Then initialize the IAM database:

```bash
policy_sentry initialize
```

To generate a policy according to resources and access levels, start by creating a template with this command so you can just fill out the ARNs:

```bash
policy_sentry create-template --name myRole --output-file crud.yml --template-type crud
```

It will generate a file like this:

```yaml
policy_with_crud_levels:
- name: myRole
  description: '' # For human auditability
  role_arn: '' # For human auditability
  # Insert ARNs under each access level below
  # If you do not need to use certain access levels, delete them.
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
  # If the policy needs to use IAM actions that cannot be restricted to ARNs,
  # like ssm:DescribeParameters, specify those actions here.
  wildcard:
    - ''
```

Then just fill it out:

```yaml
policy_with_crud_levels:
- name: myRole
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


#### Installation

* Policy Sentry is available via pip. To install, run:

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


### Initialization

```bash
# Initialize the policy_sentry config folder and create the IAM database tables.
policy_sentry initialize

# Fetch the most recent version of the AWS documentation so you can experiment with new services.
policy_sentry initialize --fetch

# Override the Access Levels by specifying your own Access Levels (example:, correcting Permissions management levels)
policy_sentry initialize --access-level-overrides-file ~/.policy_sentry/overrides-resource-policies.yml

policy_sentry initialize --access-level-overrides-file ~/.policy_sentry/access-level-overrides.yml
```

### Policy Writing cheat sheet

```bash
# Initialize the policy_sentry config folder and create the IAM database tables.
policy_sentry initialize

# Create templates first!!! This way you can just paste the values you need rather than remembering the YAML format
# CRUD mode
policy_sentry create-template --name myRole --output-file tmp.yml --template-type crud
# Actions mode
policy_sentry create-template --name myRole --output-file tmp.yml --template-type actions

# Write policy based on resource-specific access levels
policy_sentry write-policy --crud --input-file examples/yml/crud.yml

# Write policy_sentry YML files based on resource-specific access levels on a directory basis
policy_sentry write-policy-dir --crud --input-dir examples/input-dir --output-dir examples/output-dir

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


### Policy Analysis Cheat Sheet

```bash
# Initialize the policy_sentry config folder and create the IAM database tables.
policy_sentry initialize

# Initialize the database, but instead of using the AWS HTML files in the Python package, download the very latest AWS HTML Docs and make sure that Policy Sentry uses them
policy_sentry initialize --fetch

# Analyze a single IAM policy FILE
policy_sentry analyze policy-file --policy examples/explicit-actions.json

# Download customer managed IAM policies from a live account under 'default' profile. By default, it looks for policies that are 1. in use and 2. customer managed
policy_sentry download-policies # this will download to ~/.policy_sentry/accountid/customer-managed/.json

# Download customer-managed IAM policies, including those that are not attached
policy_sentry download-policies --include-unattached # this will download to ~/.policy_sentry/accountid/customer-managed/.json

# 1. Use a tool like Gossamer (https://github.com/GESkunkworks/gossamer) to update your AWS credentials profile all at once
# 2. Recursively download all IAM policies from accounts in your credentials file
policy_sentry download-policies --recursive

# Audit all IAM policies downloaded locally and generate CSV and JSON reports.
policy_sentry analyze downloaded-policies

# Audit all IAM policies and also include a Markdown formatted report, then convert it to HTML
policy_sentry analyze downloaded-policies --include-markdown-report
pandoc -f markdown ~/.policy_sentry/analysis/overall.md -t html > overall.html

# Use a custom report configuration. This is typically used for excluding role names. Defaults to ~/.policy_sentry/report-config.yml
policy_sentry analyze downloaded-policies --report-config custom-config.yml

# Analyze a specific policy file
policy_sentry analyze policy-file --policy examples/analyze/explicit-actions.json
```


## Commands

### Usage
* `initialize`: Create a SQLite database that contains all of the services available through the [Actions, Resources, and Condition Keys documentation][1]. See the [documentation][12].

* `create-template`: Creates the YML file templates for use in the `write-policy` command types.

* `write-policy`: Leverage a YAML file to write policies for you
  - Option 1: Specify CRUD levels (Read, Write, List, Tagging, or Permissions management) and the ARN of the resource. It will write this for you. See the [documentation][13]
  - Option 2: Specify a list of actions. It will write the IAM Policy for you, but you will have to fill in the ARNs. See the [documentation][14].

* `write-policy-dir`: This can be helpful in the Terraform use case. For more information, see the [documentation][15].

* `query`: Query the IAM database tables. This can help when filling out the Policy Sentry templates, or just querying the database for quick knowledge.
  - Option 1: Query the Actions Table (`action-table`)
  - Option 2: Query the ARNs Table (`arn-table`)
  - Option 3: Query the Conditions Table (`condition-table`)

* `download-policies`: Download IAM policies from your AWS account for analysis.

* `analyze`: Analyze IAM policies downloaded locally, expands the wildcards (like ``s3:List*``) if necessary, and generates a report based on policies that are flagged for these risk categories:

  - Privilege Escalation: This is based off of [Rhino Security Labs research](https://github.com/RhinoSecurityLabs/AWS-IAM-Privilege-Escalation).

  - Resource Exposure: This contains all IAM Actions at the "Permissions Management" resource level. Essentially - if your policy can (1) write IAM Trust Policies, (2) write to the RAM service, or (3) write Resource-based Policies, then the action has the potential to result in resource exposure if an IAM principal with that policy was compromised.

  - Network Exposure: This highlights IAM actions that indicate an IAM principal possessing these actions could create resources that could be exposed to the public at the network level. For example, public RDS clusters, public EC2 instances. While possession of these privileges does not constitute a security vulnerability, it is important to know exactly who has these permissions.

  - Credentials Exposure: This includes IAM actions that grant some kind of credential, where if exposed, it could grant access to sensitive information. For example, `ecr:GetAuthorizationToken` creates a token that is valid for 12 hours, which you can use to authenticate to Elastic Container Registries and download Docker images that are private to the account.

### Library usage

When using Policy Sentry manually, you have to build a local database file with the `policy_sentry initialize` command.

However, if you are developing your own Python code and you want to import Policy Sentry as a third party package, you can skip the initialization and leverage the local database file that is bundled with the Python package itself.

This is especially useful for developers who wish to leverage Policy Sentry’s capabilities that require the use of the IAM database (such as querying the IAM database table). This way, you don’t have to initialize the database and can just query it immediately.

The code example is located [here](https://github.com/salesforce/policy_sentry/blob/master/examples/library-usage/example.py). It is also shown below.

We’ve built a trick into the `connect_db` function that developers can specify to leverage the local database. The trick is to just use `bundled` as the single parameter for the `connect_db` method. See the example.

```python
from policy_sentry.querying.actions import get_actions_for_service
from policy_sentry.shared.database import connect_db

def example():
    db_session = connect_db('bundled')  # This is the critical line. You just need to specify `'bundled'` as the parameter.
    actions = get_actions_for_service(db_session, 'cloud9')  # Then you can leverage any method that requires access to the database.
    for action in actions:
        print(action)

if __name__ == '__main__':
    example()
```

The results will look like:

```
cloud9:createenvironmentec2
cloud9:createenvironmentmembership
cloud9:deleteenvironment
cloud9:deleteenvironmentmembership
cloud9:describeenvironmentmemberships
cloud9:describeenvironmentstatus
cloud9:describeenvironments
cloud9:getusersettings
cloud9:listenvironments
cloud9:updateenvironment
cloud9:updateenvironmentmembership
cloud9:updateusersettings
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
cat examples/yml/crud.yml | docker run -i --rm kmcquade/policy_sentry:latest "write-policy --crud"

cat examples/yml/actions.yml | docker run -i --rm kmcquade/policy_sentry:latest "write-policy"
```

### Updating the AWS HTML files

This will update the HTML files stored in `policy_sentry/shared/data/docs/list_*.partial.html`:

```bash
pipenv shell
python3 ./utils/download_docs.py
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
