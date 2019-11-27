Downloading Policies
####################

.. code-block:: text

    Usage: policy_sentry download-policies [OPTIONS]

      Download remote IAM policies to a directory for use in the analyze-iam-
      policies command.

    Options:
      --recursive           Use this flag to download *all* IAM policies from
                            accounts listed in your AWS credentials file.
      --profile TEXT        To authenticate to AWS and analyze *all* existing IAM
                            policies.
      --aws-managed         Use flag if you want to download AWS Managed policies
                            too.
      --include-unattached  Download both attached and unattached policies.
      --help                Show this message and exit.


* Make sure you are authenticated to AWS.

Customer-managed policies - one account
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Run this command:

.. code-block:: bash

   policy_sentry download-policies --profile dev


*
  It will download the policies to ``$HOME/.policy_sentry/policy-analysis/account-number/customer-managed``.

*
  You can then run analysis on the entire directory:

.. code-block:: bash

   policy_sentry analyze

Then it will generate a report based on risky IAM actions for a variety of categories, like Network Exposure, Resource Exposure, Credentials Exposure, or Privilege Escalation.


AWS Managed policies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


* Run this command:

.. code-block:: bash

   policy_sentry download-policies --profile dev --aws-managed


*
  It will download the policies to ``$HOME/.policy_sentry/policy-analysis/account-number/aws-managed``.

*
  You can then run analysis on the entire directory:

.. code-block:: bash

   analyze-iam-policy --policy $HOME/.policy_sentry/policy-analysis/0123456789012/customer-managed --from-access-level permissions-management

Then it will print out the AWS Managed IAM policies that contain actions with "Permissions management" access levels.
