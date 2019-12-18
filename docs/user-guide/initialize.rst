Initialization
##############

`initialize`: This will create a SQLite database that contains all of the services available through the `Actions, Resources, and Condition Keys documentation <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html>`__.

The database is stored in ``$HOME/.policy_sentry/aws.sqlite3``.

The database is generated based on the HTML files stored in the ``policy_sentry/shared/data/docs/`` directory.

Options
^^^^^^^

* ``--access-level-overrides-file`` (Optional): Path to your own custom access level overrides file, used to override the Access Levels per action provided by AWS docs. The default one is `here <https://github.com/salesforce/policy_sentry/blob/master/policy_sentry/shared/data/access-level-overrides.yml>`__.
* ``--fetch`` (Optional):  Specify this flag to fetch the HTML Docs directly from the AWS website. This will be helpful if the docs in the Git repository are behind the live docs and you need to use the latest version of the docs right now.

*  ``--fetch`` (Optional) Specify this flag to fetch the HTML Docs directly from the AWS website. This will be helpful if the docs in the Git repository are behind the live docs and you need to use the latest version of the docs right now.


Usage
^^^^^

.. code-block:: bash

    # Initialize the database, using the existing Access Level Overrides file
    policy_sentry initialize

    # Fetch the most recent version of the AWS documentation so you can experiment with new services.
    # This can be helpful in case the AWS HTML files in the Python package are outdated, even if it is a week old
    policy_sentry initialize --fetch

    # Initialize the database with a custom Access Level Overrides file

    policy_sentry initialize --access-level-overrides-file ~/.policy_sentry/access-level-overrides.yml
    policy_sentry initialize --access-level-overrides-file ~/.policy_sentry/overrides-resource-policies.yml
