Querying the Policy Database
----------------------------

Policy Sentry relies on a SQLite database, generated at `initialize` time, which contains all of the services available through the `Actions, Resources, and Condition Keys documentation <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html>`__. The HTML files from that AWS documentation is scraped and stored in the SQLite database, which is then stored in ``$HOME/.policy_sentry/aws.sqlite3``.

Policy Sentry supports querying that database through the CLI. This can help with writing policies and generally knowing what values to supply in your policies.

---------
Commands
---------

* Query the **Action**\  table:

.. code-block:: bash

    # Get a list of all IAM Actions available to the RAM service
    policy_sentry query --table action --service ram
    # Get details about the `ram:TagResource` IAM Action
    policy_sentry query --table action --service ram --name tagresource
    # Get a list of all IAM actions under the RAM service that have the Permissions management access level.
    policy_sentry query --table action --service ram --access-level permissions-management
    # Get a list of all IAM actions under the SES service that support the `ses:FeedbackAddress` condition key.
    policy_sentry query --table action --service ses --condition ses:FeedbackAddress

* Query the **ARN**\  table:

.. code-block:: bash

    # Get a list of all RAW ARN formats available through the SSM service.
    policy_sentry query --table arn --service ssm
    # Get the raw ARN format for the `cloud9` ARN with the short name `environment`
    policy_sentry query --table arn --service cloud9 --name environment
    # Get key/value pairs of all RAW ARN formats plus their short names
    policy_sentry query --table arn --service cloud9 --list-arn-types

* Query the **Condition Keys**\  table:

.. code-block:: bash

    # Get a list of all condition keys available to the Cloud9 service
    policy_sentry query --table condition --service cloud9
    # Get details on the condition key titled `cloud9:Permissions`
    policy_sentry query --table condition --service cloud9 --name cloud9:Permissions
