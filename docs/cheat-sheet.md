Cheat sheet
===========


### Commands

- `create-template`: Creates the YML file templates for use in the `write-policy` command types.

- `write-policy`: Leverage a YAML file to write policies for you
    * Option 1: Specify CRUD levels (Read, Write, List, Tagging, or Permissions management) and the ARN of the resource. It will write this for you. See the [documentation](https://policy-sentry.readthedocs.io/en/latest/introduction/introduction.html)
    * Option 2: Specify a list of actions. It will write the IAM Policy for you, but you will have to fill in the ARNs. See the [documentation](https://policy-sentry.readthedocs.io/en/latest/introduction/introduction.html).

- `query`: Query the IAM database tables. This can help when filling out the Policy Sentry templates, or just querying the database for quick knowledge.
    * Option 1: Query the Actions Table (`action-table`)
    * Option 2: Query the ARNs Table (`arn-table`)
    * Option 3: Query the Conditions Table (`condition-table`)

- `initialize`: (Optional). Create a JSON file to use as a data source that contains all of the services available through the [Actions, Resources, and Condition Keys documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html). See the [documentation](https://policy-sentry.readthedocs.io/en/latest/introduction/introduction.html).

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
policy_sentry query action-table --service s3 --resource-type '*' --fmt yaml

# Get a list of actions at the "Write" level in S3 that do not support resource constraints
policy_sentry query action-table --service s3 --access-level write --resource-type '*' --fmt yaml

# Get a list of all IAM actions across ALL services that have "Permissions management" access
policy_sentry query action-table --service all --access-level permissions-management

# Get a list of actions at the "Write" level in SSM service for resource type "parameter"
policy_sentry query action-table --service ssm --access-level write --resource-type parameter

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
