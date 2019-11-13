Command cheat sheet
-------------------

Commands
~~~~~~~~

*
  ``initialize``\ : Create a SQLite database that contains all of the services available through the `Actions, Resources, and Condition Keys documentation <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html>`__. See the `documentation <./initialize.html>`__.

*
  ``download-policies``\ : Download IAM policies from an AWS account locally for analysis against the database.

*
  ``create-template``\ : Creates the YML file templates for use in the ``write-policy`` command types.

*
  ``write-policy``\ : Leverage a YAML file to write policies for you


  * Option 1: CRUD Mode. Specify CRUD levels (Read, Write, List, Tagging, or Permissions management) and the ARN of the resource. It will write this for you. See the documentation for more details.
  * Option 2: Actions Mode. Specify a list of actions. It will write the IAM Policy for you, but you will have to fill in the ARNs. See the documentation for more details.

*
  ``write-policy-dir``\ : This can be helpful in the Terraform use case. For more information, see the wiki.

*
  ``analyze-iam-policy``: Analyze an IAM policy read from a JSON file, expands the wildcards (like ``s3:List*`` if necessary.

  * Option 1: Audits them to see if certain IAM actions are permitted, based on actions in a separate text file. See the `documentation <./analyze-policy.html#audit-for-custom-list-of-actions>`__.
  * Option 2: Audits them to see if any of the actions in the policy meet a certain access level, such as "Permissions management." See the `documentation <./analyze-policy.html#audit-a-policy-file-for-permissions-with-specific-access-levels>`__.

* ``query``: Query the IAM database tables. This can help when filling out the Policy Sentry templates, or just querying the database for quick knowledge.

  * Option 1: Query the Actions Table (``--table action``)
  * Option 2: Query the ARNs Table (``--table arn``)
  * Option 3: Query the Conditions Table (``--table condition``)


Policy Writing Commands
~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

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


Policy Analysis Commands
~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

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


IAM Database Query Commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
