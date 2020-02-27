CRUD Mode
=============

* **TLDR**: Building IAM policies with resource constraints and access levels.

This is the flagship feature of this tool. You can just specify the CRUD levels (Read, Write, List, Tagging, or Permissions management) for each action in a
YAML File. The policy will be generated for you. You might need to fiddle with the results for your use in Terraform, but it significantly reduces the level of effort to build least privilege into your policies.


Command options
----------------


* ``--input-file``\ : YAML file containing the CRUD levels + Resource ARNs. Required.
* ``--minimize``\ : Whether or not to minimize the resulting statement with *safe* usage of wildcards to reduce policy length. Set this to the character length you want. This can be extended for readability. I suggest setting it to ``0``.
* ``-v``\: Set the logging level. Choices are critical, error, warning, info, or debug. Defaults to info


Example:

.. code-block:: bash

   policy_sentry write-policy --input-file examples/crud.yml

Instructions
------------


* To generate a policy according to resources and access levels, start by creating a template with this command so you can just fill out the ARNs:

.. code-block:: bash

    policy_sentry create-template --name myRole --output-file crud.yml --template-type crud

* It will generate a file like this:

.. code-block:: yaml

    mode: crud
    name: myRole
    # Specify resource ARNs
    read:
    - ''
    write:
    - ''
    list:
    - ''
    tagging:
    - ''
    permissions-management:
    - ''
    # Actions that do not support resource constraints
    wildcard-only:
      single-actions: # standalone actions
      - ''
      # Service-wide, per access level - like 's3' or 'ec2'
      service-read:
      - ''
      service-write:
      - ''
      service-list:
      - ''
      service-tagging:
      - ''
      service-permissions-management:
      - ''

* Then just fill it out:

.. code-block:: yaml

    mode: crud
    name: myRole
    description: 'Justification for privileges'
    role_arn: 'arn:aws:iam::123456789102:role/myRole'
    read:
    - 'arn:aws:ssm:us-east-1:123456789012:parameter/myparameter'
    write:
    - 'arn:aws:ssm:us-east-1:123456789012:parameter/myparameter'
    list:
    - 'arn:aws:ssm:us-east-1:123456789012:parameter/myparameter'
    tagging:
    - 'arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret'
    permissions-management:
    - 'arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret'


* Run the command:

.. code-block:: bash

   policy_sentry write-policy --input-file crud.yml


* It will generate an IAM Policy containing an IAM policy with the actions restricted to the ARNs specified above.
* The resulting policy (without the ``--minimize command``\ ) will look like this:

.. code-block:: json

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "SsmReadParameter",
                "Effect": "Allow",
                "Action": [
                    "ssm:getparameter",
                    "ssm:getparameterhistory",
                    "ssm:getparameters",
                    "ssm:getparametersbypath",
                    "ssm:listtagsforresource"
                ],
                "Resource": [
                    "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter"
                ]
            },
            {
                "Sid": "SsmWriteParameter",
                "Effect": "Allow",
                "Action": [
                    "ssm:deleteparameter",
                    "ssm:deleteparameters",
                    "ssm:putparameter",
                    "ssm:labelparameterversion"
                ],
                "Resource": [
                    "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter"
                ]
            },
            {
                "Sid": "SecretsmanagerPermissionsmanagementSecret",
                "Effect": "Allow",
                "Action": [
                    "secretsmanager:deleteresourcepolicy",
                    "secretsmanager:putresourcepolicy"
                ],
                "Resource": [
                    "arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"
                ]
            },
            {
                "Sid": "SecretsmanagerTaggingSecret",
                "Effect": "Allow",
                "Action": [
                    "secretsmanager:tagresource",
                    "secretsmanager:untagresource"
                ],
                "Resource": [
                    "arn:aws:secretsmanager:us-east-1:123456789012:secret:mysecret"
                ]
            }
        ]
    }


Wildcard-only section
---------------------

You'll notice that as of release 0.7.1, there is a new section for `wildcard-only`:

.. code-block:: yaml

    mode: crud
    name: myRole
    # Specify resource ARNs
    read:
    - ''
    # Actions that do not support resource constraints
    wildcard-only:
      single-actions: # standalone actions
      - ''
      # Service-wide, per access level - like 's3' or 'ec2'
      service-read:
      - ''
      service-write:
      - ''
      service-list:
      - ''
      service-tagging:
      - ''
      service-permissions-management:
      - ''

The `wildcard-only` section is meant to hold IAM actions that do not support resource constraints. Most IAM actions do support resource constraints - for instance, `s3:GetObject` can be restricted according to a specific object or path within an S3 bucket ARN , like `arn:aws:s3:::mybucket/path/*`. However, some IAM actions do **not** support resource constraints.

Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For example, run a query against the IAM database to determine "which S3 actions at the LIST access level do not support resource constraints":

.. code-block:: bash

    policy_sentry query action-table --service s3 --access-level list --wildcard-only

The output will be:

.. code-block:: text
    s3 LIST actions that must use wildcards in the resources block:
    [
        "s3:ListAllMyBuckets"
    ]

Similarly, S3 has a few actions that at the "Read" access level that do not support resource constraints. Run this query against the IAM database to discover those actions:


.. code-block:: bash

    policy_sentry query action-table --service s3 --access-level read --wildcard-only

The output will be:

.. code-block:: text

    s3 READ actions that must use wildcards in the resources block:
    [
        "s3:GetAccessPoint",
        "s3:GetAccountPublicAccessBlock",
        "s3:ListAccessPoints"
    ]


Basic support for Wildcard-only Actions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As you can see from the previous example, there are definitely valid use cases for providing access to IAM Actions that do not support resource constraints (i.e., where the Action must be set to `Resource=*`).

**Single IAM Actions**

Previous to version 0.7.1, the user still had to provide specific IAM actions in that section. That is still supported, using the `single-actions` array under the `wildcard-only` map, as shown in the example `crud.yml` below.

.. code-block:: yaml

    mode: crud
    name: myRole
    wildcard-only:
      single-actions:
      - 's3:ListAllMyBuckets'

The resulting policy would look like this:

.. code-block:: json

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "MultMultNone",
                "Effect": "Allow",
                "Action": [
                    "s3:ListAllMyBuckets"
                ],
                "Resource": [
                    "*"
                ]
            }
        ]
    }

And what's really cool about that - if the user tries to bypass it by supplying an action that supports resource constraints (like `secretsmanager:DeleteSecret`), Policy Sentry will ignore the user's request. Consider a file titled `crud.yml` with the contents below:

.. code-block:: yaml

    mode: crud
    name: myRole
    wildcard-only:
      single-actions:
      - 's3:ListAllMyBuckets'
      - 'secretsmanager:DeleteSecret'  # Policy Sentry will ignore this!

Now run the command:

.. code-block:: bash

    policy_sentry write-policy crud.yml

Notice how the output does not include `secretsmanager:DeleteSecret`:

.. code-block:: json

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "MultMultNone",
                "Effect": "Allow",
                "Action": [
                    "s3:ListAllMyBuckets"
                ],
                "Resource": [
                    "*"
                ]
            }
        ]
    }



CRUD-based support for Wildcard-only Actions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


That previous example is very cool - but it's not terribly fast for users to have to run the CLI queries. We decided that it should be even easier than this. If you're using the `Terraform module <https://github.com/kmcquade/terraform-aws-policy-sentry>`__, then *you should never, ever have to query the IAM database*.

Now bear witness to the latest feature addition to Policy Sentry: wildcard-only, CRUD-based, service-specific actions.

.. code-block:: yaml

    mode: crud
    wildcard-only:
        service-read:
        - ecr           # This will add ecr:GetAuthorizationToken to the policy
        - s3            # This adds s3:GetAccessPoint, s3:GetAccountPublicAccessBlock, s3:ListAccessPoints


As shown above, the input only required the user to supply `s3` and `ecr` under the `service-read` array in the `wildcard-only` map.

Now run the command:

.. code-block:: bash

    policy_sentry write-policy crud.yml

Notice how the output includes *wildcard-only* actions at the *read* access level for the `ecr` and `s3` services:

.. code-block:: json

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "MultMultNone",
                "Effect": "Allow",
                "Action": [
                    "ecr:GetAuthorizationToken",
                    "s3:GetAccessPoint",
                    "s3:GetAccountPublicAccessBlock",
                    "s3:ListAccessPoints"
                ],
                "Resource": [
                    "*"
                ]
            }
        ]
    }


Combining approaches
~~~~~~~~~~~~~~~~~~~~~

Here's a slightly more complex policy. See the input file `crud.yml` below:

.. code-block:: yaml

    mode: crud
    read:
    - arn:aws:s3:::example-org-s3-access-logs
    wildcard-only:
        service-read:
        - ecr           # This will add ecr:GetAuthorizationToken to the policy
        - s3            # This adds s3:GetAccessPoint, s3:GetAccountPublicAccessBlock, s3:ListAccessPoints

After running the command:

.. code-block:: bash

    policy_sentry write-policy crud.yml

.. code-block:: json

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "MultMultNone",
                "Effect": "Allow",
                "Action": [
                    "ecr:GetAuthorizationToken",
                    "s3:GetAccessPoint",
                    "s3:GetAccountPublicAccessBlock",
                    "s3:ListAccessPoints"
                ],
                "Resource": [
                    "*"
                ]
            },
            {
                "Sid": "S3PermissionsmanagementBucket",
                "Effect": "Allow",
                "Action": [
                    "s3:DeleteBucketPolicy",
                    "s3:PutBucketAcl",
                    "s3:PutBucketPolicy",
                    "s3:PutBucketPublicAccessBlock"
                ],
                "Resource": [
                    "arn:aws:s3:::example-org-s3-access-logs"
                ]
            }
        ]
    }

And yes, it's all available in the Terraform module :)
