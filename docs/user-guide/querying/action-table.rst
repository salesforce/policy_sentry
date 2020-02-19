Action table
===============

.. code-block:: bash

    # NOTE: Use --fmt yaml or --fmt json to change the output format. Defaults to json for querying

    # Get a list of actions that do not support resource constraints
    policy_sentry query action-table --service s3 --wildcard-only --fmt yaml

    # Get a list of actions at the "Read" level in S3 that do not support resource constraints
    policy_sentry query action-table --service s3 --access-level read --wildcard-only --fmt yaml

    # Get a list of all IAM Actions available to the RAM service
    policy_sentry query action-table --service ram

    # Get details about the `ram:TagResource` IAM Action
    policy_sentry query action-table --service ram --name tagresource

    # Get a list of all IAM actions under the RAM service that have the Permissions management access level.
    policy_sentry query action-table --service ram --access-level permissions-management

    # Get a list of all IAM actions under the SES service that support the `ses:FeedbackAddress` condition key.
    policy_sentry query action-table --service ses --condition ses:FeedbackAddress

---------
Options
---------

.. code-block:: text

    Usage: policy_sentry query action-table [OPTIONS]

    Options:
      --service TEXT                  Filter according to AWS service.  [required]
      --name TEXT                     The name of IAM Action. For example, if the
                                      action is "iam:ListUsers", supply
                                      "ListUsers" here.
      --access-level [read|write|list|tagging|permissions-management]
                                      If action table is chosen, you can use this
                                      to filter according to CRUD levels.
                                      Acceptable values are read, write, list,
                                      tagging, permissions-management
      --condition TEXT                If action table is chosen, you can supply a
                                      condition key to show a list of all IAM
                                      actions that support the condition key.
      --wildcard-only                 If action table is chosen, show the IAM
                                      actions that only support wildcard resources
                                      - i.e., cannot support ARNs in the resource
                                      block.
      --fmt [yaml|json]               Format output as YAML or JSON. Defaults to
                                      "yaml"
      --log-level                     Set the logging level. Choices are CRITICAL, ERROR, WARNING, INFO, or DEBUG. Defaults to INFO
      --help                          Show this message and exit.
