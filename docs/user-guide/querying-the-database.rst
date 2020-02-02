Querying the IAM Policy Database
--------------------------------

Policy Sentry relies on a SQLite database, generated at `initialize` time, which contains all of the services available through the `Actions, Resources, and Condition Keys documentation <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html>`__. The HTML files from that AWS documentation is scraped and stored in the SQLite database, which is then stored in ``$HOME/.policy_sentry/aws.sqlite3``.

Policy Sentry supports querying that database through the CLI. This can help with writing policies and generally knowing what values to supply in your policies.

---------
Commands
---------

* Query the **Action**\  table:

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

* Query the **ARN**\  table:

.. code-block:: bash

    # Get a list of all RAW ARN formats available through the SSM service.
    policy_sentry query arn-table --service ssm

    # Get the raw ARN format for the `cloud9` ARN with the short name `environment`
    policy_sentry query arn-table --service cloud9 --name environment

    # Get key/value pairs of all RAW ARN formats plus their short names
    policy_sentry query arn-table --service cloud9 --list-arn-types

* Query the **Condition Keys**\  table:

.. code-block:: bash

    # Get a list of all condition keys available to the Cloud9 service
    policy_sentry query condition-table --service cloud9

    # Get details on the condition key titled `cloud9:Permissions`
    policy_sentry query condition-table --service cloud9 --name cloud9:Permissions

---------
Options
---------

* action-table

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
      --quiet             Set the logging level to WARNING instead of INFO.
      --help                          Show this message and exit.

* arn-table

.. code-block:: text

    Usage: policy_sentry query arn-table [OPTIONS]

      Query the ARN Table from the Policy Sentry database

    Options:
      --service TEXT     Filter according to AWS service.  [required]
      --name TEXT        The short name of the resource ARN type. For example,
                         `bucket` under service `s3`.
      --list-arn-types   Show the short names of ARN Types. If empty, this will
                         show RAW ARNs only.
      --fmt [yaml|json]  Format output as YAML or JSON. Defaults to "yaml"
      --quiet             Set the logging level to WARNING instead of INFO.
      --help             Show this message and exit.

* condition-table

.. code-block:: text

    Usage: policy_sentry query condition-table [OPTIONS]

      Query the condition keys table from the Policy Sentry database

    Options:
      --name TEXT        Get details on a specific condition key. Leave this blank
                         to get a list of all condition keys available to the
                         service.
      --service TEXT     Filter according to AWS service.  [required]
      --fmt [yaml|json]  Format output as YAML or JSON. Defaults to "yaml"
      --quiet             Set the logging level to WARNING instead of INFO.
      --help             Show this message and exit.

