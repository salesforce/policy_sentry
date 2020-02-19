Querying the IAM Database
--------------------------------

Policy Sentry relies on a SQLite database that contains all of the data from the `Actions, Resources, and Condition Keys documentation <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html>`__ hosted by AWS.

Policy Sentry supports querying that database through the CLI. This can help with writing policies and generally knowing what values to supply in your policies.


.. toctree::
   :maxdepth: 2
   :caption: Querying the IAM Database

   action-table
   arn-table
   condition-table
