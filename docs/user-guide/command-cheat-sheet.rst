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
  ``analyze``: Analyze IAM policies downloaded locally, expands the wildcards (like ``s3:List*``) if necessary, and generates a report based on policies that are flagged for these risk categories:

  #. **Privilege Escalation**: This is based off of `Rhino Security Labs research <https://github.com/RhinoSecurityLabs/AWS-IAM-Privilege-Escalation>`_

  #. **Resource Exposure**: This contains all IAM Actions at the "Permissions Management" resource level. Essentially - if your policy can (1) write IAM Trust Policies, (2) write to the RAM service, or (3) write Resource-based Policies, then the action has the potential to result in resource exposure if an IAM principal with that policy was compromised.

  #. **Network Exposure**: This highlights IAM actions that indicate an IAM principal possessing these actions could create resources that could be exposed to the public at the network level. For example, public RDS clusters, public EC2 instances. While possession of these privileges does not constitute a security vulnerability, it is important to know exactly who has these permissions.

  #. **Credentials Exposure**: This includes IAM actions that grant some kind of credential, where if exposed, it could grant access to sensitive information. For example, ``ecr:GetAuthorizationToken`` creates a token that is valid for 12 hours, which you can use to authenticate to Elastic Container Registries and download Docker images that are private to the account.

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
    policy_sentry write-policy --crud --input-file examples/yml/crud.yml

    # Write policy_sentry YML files based on resource-specific access levels on a directory basis
    policy_sentry write-policy-dir --crud --input-dir examples/input-dir --output-dir examples/output-dir

    # Create a template file for use in the write-policy command (actions mode)
    policy_sentry create-template --name myRole --output-file tmp.yml --template-type actions

    # Write policy based on a list of actions
    policy_sentry write-policy --input-file examples/yml/actions.yml


Policy Download and Analysis Commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    # Initialize the policy_sentry config folder and create the IAM database tables.
    policy_sentry initialize

    # Download customer managed IAM policies from a live account under 'default' profile. By default, it looks for policies that are 1. in use and 2. customer managed
    policy_sentry download-policies # this will download to ~/.policy_sentry/accountid/customer-managed/.json

    # Download customer-managed IAM policies, including those that are not attached
    policy_sentry download-policies --include-unattached # this will download to ~/.policy_sentry/accountid/customer-managed/.json

    # 1. Use a tool like Gossamer (https://github.com/GESkunkworks/gossamer) to update your AWS credentials profile all at once
    # 2. Recursively download all IAM policies from accounts in your credentials file
    # Note: alternatively, you can just place them there yourself.
    policy_sentry download --recursive

    # Audit all IAM policies downloaded locally and generate CSV and JSON reports.
    policy_sentry analyze

    # Audit all IAM policies and also include a Markdown formatted report, then convert it to HTML
    policy_sentry analyze --include-markdown report
    pandoc -f markdown ~/.policy_sentry/analysis/overall.md -t html > overall.html

    # Use a custom report configuration. This is typically used for excluding role names. Defaults to ~/.policy_sentry/report-config.yml
    policy_sentry analyze --report-config custom-config.yml


IAM Database Query Commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~


* Query the **Action**\  table:

.. code-block:: bash

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
