Analyzing Policies
##################

``analyze``: Reads policies downloaded locally, and expands the wildcards (like ``s3:List*`` if necessary, and audits them to see if certain IAM actions are permitted.

Motivation
^^^^^^^^^^

**Case 1:**

Let's say that you have hundreds or thousands of engineers at your organization who have permissions to create or edit IAM policies. Perhaps this is just in Dev, or it's just allowed via Infrastructure as Code, or maybe there is rampant shadow IT.

You know that there is a huge issue with overpermissioning at your organization - not only is there widespread use of ``Resources: "*"`` in IAM policies, lots of engineers have the ability to create network resources, update security groups, create resource-based policies, escalate privileges via methods popularized through `Rhino Security Labs research <https://github.com/RhinoSecurityLabs/AWS-IAM-Privilege-Escalation>`_, and more. To convince your boss that a serious IAM uplift project should happen, you want to show your boss **the inherent risk levels in IAM policies per account, regardless of whether or not it is currently a vulnerability.**

If you're in this position - welcome to the right place.

**Case 2:**

Let's say you are a developer that handles creation of IAM policies.

* An internal customer asks you to create an IAM policy.
* You haven't been tasked with auditing IAM policies yourself, as that's not your area of expertise, and until this point there is no automation to do it for you.
* However, you want to make sure that the customers aren't asking for permissions that they don't need, since we need to have *some* guardrails in place to prevent unnecessary exposure of attack surfaces.
* This is made more difficult by the fact that sometimes, the customer will give you IAM policies that include ``*`` in the actions. Not only do you want to restrict actions to the specific ARNs, but you want to know what actions they actually need!

You can solve this with policy_sentry too, by auditing for IAM actions in a given policy. Tell them to supply the policy to you in JSON format, stash it in ``~/.policy_sentry/analysis/account_id/customer-managed/``, and feed it into the ``analyze_iam_policy`` command, as shown below.

Options
^^^^^^^

.. code-block:: text

    Usage: policy_sentry analyze [OPTIONS] COMMAND [ARGS]...

      Analyze locally stored IAM policies and generate a report.

    Options:
      --help  Show this message and exit.

    Commands:
      downloaded-policies  Analyze *all* locally downloaded IAM policy files and
                           generate a report.
      policy-file          Analyze a *single* policy file and generate a report



**downloaded-policies subcommand**:

.. code-block:: text

    Usage: policy_sentry analyze downloaded-policies [OPTIONS]

      Analyze all locally downloaded IAM policy files and generate a report.

    Options:
      --report-config PATH       Custom report configuration file. Contains policy
                                 name exclusions and custom risk score weighting.
                                 Defaults to ~/.policy_sentry/report-config.yml
      --report-name TEXT         Name of the report. Defaults to "overall".
      --include-markdown-report  Use this flag to enable a Markdown report, which
                                 can be used with pandoc to generate an HTML
                                 report. Due to potentially very large report
                                 sizes, this is set to False by default.
      --help                     Show this message and exit.



**policy-file subcommand**:

.. code-block:: text

    Usage: policy_sentry analyze policy-file [OPTIONS]

      Analyze a *single* policy file and generate a report

    Options:
      --policy PATH              The policy file to analyze.  [required]
      --report-config PATH       Custom report configuration file. Contains policy
                                 name exclusions and custom risk score weighting.
                                 Defaults to ~/.policy_sentry/report-config.yml
      --report-path PATH         *Path* to the directory of the final report.
                                 Defaults to current directory.
      --account-id TEXT          Account ID for the policy. If you want the report
                                 to include the account ID, provide it here.
                                 Defaults to a placeholder value.
      --include-markdown-report  Use this flag to enable a Markdown report, which
                                 can be used with pandoc to generate an HTML
                                 report. Due to potentially very large report
                                 sizes, this is set to False by default.
      --quiet                    Set the logging level to WARNING instead of INFO.
      --help                     Show this message and exit.


Instructions
^^^^^^^^^^^^

* Don't forget to build the database first:

.. code-block:: bash

   policy_sentry initialize


Risk Categories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  #. **Privilege Escalation**: This is based off of `Rhino Security Labs research <https://github.com/RhinoSecurityLabs/AWS-IAM-Privilege-Escalation>`_

  #. **Resource Exposure**: This contains all IAM Actions at the "Permissions Management" resource level. Essentially - if your policy can (1) write IAM Trust Policies, (2) write to the RAM service, or (3) write Resource-based Policies, then the action has the potential to result in resource exposure if an IAM principal with that policy was compromised.

  #. **Network Exposure**: This highlights IAM actions that indicate an IAM principal possessing these actions could create resources that could be exposed to the public at the network level. For example, public RDS clusters, public EC2 instances. While possession of these privileges does not constitute a security vulnerability, it is important to know exactly who has these permissions.

  #. **Credentials Exposure**: This includes IAM actions that grant some kind of credential, where if exposed, it could grant access to sensitive information. For example, ``ecr:GetAuthorizationToken`` creates a token that is valid for 12 hours, which you can use to authenticate to Elastic Container Registries and download Docker images that are private to the account.


Audit all downloaded policies and generate a report
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Command:

.. code-block:: bash

    # 1. Use a tool like Gossamer (https://github.com/GESkunkworks/gossamer) to update your AWS credentials profile all at once
    # 2. Recursively download all IAM policies from accounts in your credentials file
    # Note: alternatively, you can just place them there yourself.
    policy_sentry download --recursive

    # Audit all JSON policies under the path ~/.policy_sentry/analysis/account_id/customer-managed
    policy_sentry analyze --downloaded-policies

    # Use a custom report configuration. This is typically used for excluding role names. Defaults to ~/.policy_sentry/report-config.yml
    policy_sentry analyze --downloaded-policies --report-config custom-config.yml

* Output:

.. code-block:: text

    Analyzing...
    /Users/kmcquade/.policy_sentry/analysis/0123456789012/
    /Users/kmcquade/.policy_sentry/analysis/9876543210123/
    ...

    Reports saved to:
    -/Users/kmcquade/.policy_sentry/analysis/overall.json
    -/Users/kmcquade/.policy_sentry/analysis/overall.csv

    The JSON Report contains the raw data. The CSV report shows a report summary.


* The raw JSON data will look like this:

.. code-block:: json

    {
        "some-risky-policy": {
            "account_id": "0123456789012",
            "resource_exposure": [
                "iam:createaccesskey",
                "iam:deleteaccesskey"
            ],
            "privilege_escalation": [
                "iam:createaccesskey"
            ]
        },
        "another-risky-policy": {
            "account_id": "9876543210123",
            "resource_exposure": [
                "iam:updateassumerolepolicy",
                "iam:updaterole"
            ],
            "privilege_escalation": [
                "iam:updateassumerolepolicy"
            ],
            "credentials_exposure": [
                "ecr:getauthorizationtoken"
            ],
            "network_exposure": [
                "ec2:authorizesecuritygroupingress",
                "ec2:authorizesecuritygroupegress"
            ]
        },
    }


Audit a single IAM policy and generate a report
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


* Command:

.. code-block:: bash

    # Analyze a single IAM policy
    policy_sentry analyze policy-file --policy examples/explicit-actions.json


* This will create a CSV file that looks like this:

+--------------+-------------------+-------------------+----------------------+------------------+----------------------+
| Account ID   | Policy Name       | Resource Exposure | Privilege Escalation | Network Exposure | Credentials Exposure |
+--------------+-------------------+-------------------+----------------------+------------------+----------------------+
| 000000000000 | explicit\-actions | 9                 | 0                    | 0                | 1                    |
+--------------+-------------------+-------------------+----------------------+------------------+----------------------+


* ... and a JSON data file that looks like this:


.. code-block:: json

    {
        "explicit-actions": {
            "resource_exposure": [
                "ecr:setrepositorypolicy",
                "s3:deletebucketpolicy",
                "s3:objectowneroverridetobucketowner",
                "s3:putaccountpublicaccessblock",
                "s3:putbucketacl",
                "s3:putbucketpolicy",
                "s3:putbucketpublicaccessblock",
                "s3:putobjectacl",
                "s3:putobjectversionacl"
            ],
            "account_id": "000000000000",
            "credentials_exposure": [
                "ecr:getauthorizationtoken"
            ]
        }
    }


Custom Config file
~~~~~~~~~~~~~~~~~~~~

* Quite often, organizations may have customer-managed policies that are in every account, or are very permissive by design. Rather than having a very large report every time you run this tool, you can specify a custom config file with this command. Just make sure you format it correctly, as shown below.

.. code-block:: yaml

    report-config:
        excluded-role-patterns:
            - "Administrator*"

**Note**: This probably will eventually support:
- Action-specific exclusions per-account and per-role
- Turning risk categories on and off
