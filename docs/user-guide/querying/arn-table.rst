ARN Table
===============

.. code-block:: bash

    # Get a list of all RAW ARN formats available through the SSM service.
    policy_sentry query arn-table --service ssm

    # Get the raw ARN format for the `cloud9` ARN with the short name `environment`
    policy_sentry query arn-table --service cloud9 --name environment

    # Get key/value pairs of all RAW ARN formats plus their short names
    policy_sentry query arn-table --service cloud9 --list-arn-types

---------
Options
---------

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
        -v, LVL          Either CRITICAL, ERROR, WARNING, INFO or DEBUG
      --help             Show this message and exit.

