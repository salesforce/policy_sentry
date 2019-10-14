# policy_sentry

IAM Least Privilege Policy Generator, auditor, and analysis database.

## Wiki

For walkthroughs and full documentation, please visit the [wiki](https://github.com/salesforce/policy_sentry/wiki).

## Overview

Writing security-conscious IAM Policies by hand can be very tedious and inefficient. Many Infrastructure as Code developers have experienced something like this:
 
 * Determined to make your best effort to give users and roles the least amount of privilege you need to perform your duties, you spend way too much time combing through the AWS IAM Documentation on [Actions, Resources, and Condition Keys for AWS Services][1]. 
 * Your team lead encourages you to build security into your IAM Policies for product quality, but eventually you get frustrated due to project deadlines.
 * You don't have an embedded security person on your team who can write those IAM policies for you, and there's no automated tool that will automagically sense the AWS API calls that you perform and then write them for you in a least-privilege manner. 
 * After fantasizing about that level of automation, you realize that writing least privilege IAM Policies, seemingly out of charity, will jeopardize your ability to finish your code in time to meet project deadlines.
 * You use Managed Policies (because hey, why not) or you eyeball the names of the API calls and use wildcards instead so you can move on with your life.
 
Such a process is not ideal for security or for Infrastructure as Code developers. We need to make it easier to write IAM Policies securely and abstract the complexity of writing least-privilege IAM policies. That's why I made this tool.

## Quickstart

* `policy_sentry` is available via pip. To install, run:

```bash
pip install --user policy_sentry
```

* Command cheat sheet

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

# Analyze an IAM policy to identify actions with specific access levels
policy_sentry analyze-iam-policy --show permissions-management --file examples/analyze/wildcards.json

# Analyze an IAM policy to identify higher-risk IAM calls
policy_sentry analyze-iam-policy --file examples/analyze/wildcards.json
```

## Commands

### Usage
* `initialize`: Create a SQLite database that contains all of the services available through the [Actions, Resources, and Condition Keys documentation][1]. See the [documentation][12].

* `create-template`: Creates the YML file templates for use in the `write-policy` command types.

* `write-policy`: Leverage a YAML file to write policies for you
  - Option 1: Specify CRUD levels (Read, Write, List, Tagging, or Permissions management) and the ARN of the resource. It will write this for you. See the [documentation][13]
  - Option 2: Specify a list of actions. It will write the IAM Policy for you, but you will have to fill in the ARNs. See the [documentation][14].

* `write-policy-dir`: This can be helpful in the Terraform use case. For more information, see the wiki.

* `analyze-iam-policy`: Analyze an IAM policy read from a JSON file, expands the wildcards (like `s3:List*` if necessary.
  - Option 1: Audits them to see if certain IAM actions are permitted, based on actions in a separate text file. See the [documentation][12].
  - Option 2: Audits them to see if any of the actions in the policy meet a certain access level, such as "Permissions management."

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
[12]: https://github.com/salesforce/policy_sentry/wiki/Initializing-policy_sentry
[13]: https://github.com/salesforce/policy_sentry/wiki/Writing-IAM-Policies-with-Resource-ARNs-and-Access-Levels
[14]: https://github.com/salesforce/policy_sentry/wiki/Writing-IAM-Policies-with-a-List-of-Actions
