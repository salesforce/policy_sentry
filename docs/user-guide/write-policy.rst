Writing IAM Policies
#####################


CRUD Mode
----------

* **TLDR**: Building IAM policies with resource constraints and access levels.

This is the flagship feature of this tool. You can just specify the CRUD levels (Read, Write, List, Tagging, or Permissions management) for each action in a
YAML File. The policy will be generated for you. You might need to fiddle with the results for your use in Terraform, but it significantly reduces the level of effort to build least privilege into your policies.


Command options
~~~~~~~~~~~~~~~


* ``--input-file``\ : YAML file containing the CRUD levels + Resource ARNs. Required.
* ``--minimize``\ : Whether or not to minimize the resulting statement with *safe* usage of wildcards to reduce policy length. Set this to the character length you want. This can be extended for readability. I suggest setting it to ``0``.
* ``--log-level``\: Set the logging level. Choices are CRITICAL, ERROR, WARNING, INFO, or DEBUG. Defaults to INFO


Example:

.. code-block:: bash

   policy_sentry write-policy --input-file examples/crud.yml

Instructions
~~~~~~~~~~~~~~~


* To generate a policy according to resources and access levels, start by creating a template with this command so you can just fill out the ARNs:

.. code-block:: bash

    policy_sentry create-template --name myRole --output-file crud.yml --template-type crud

* It will generate a file like this:

.. code-block:: yaml

    mode: crud
    name: myRole
    description: ''
    role_arn: ''
    # Insert ARNs below
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
    # Provide a list of IAM actions that cannot be restricted to ARNs
    wildcard:
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

   policy_sentry write-policy --input-file examples/crud.yml


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


Actions Mode
-------------

* **TLDR**: Supply a list of actions in a YAML file and generate the policy accordingly.

Command options
~~~~~~~~~~~~~~~

* ``--input-file``\ : YAML file containing the list of actions
* ``--minimize``\ : Whether or not to minimize the resulting statement with *safe* usage of wildcards to reduce policy length. Set this to the character lengh you want - for example, 4
* ``--log-level``\: Set the logging level. Choices are CRITICAL, ERROR, WARNING, INFO, or DEBUG. Defaults to INFO

Example:

.. code-block:: bash

   policy_sentry write-policy --input-file examples/actions.yml

Instructions
~~~~~~~~~~~~

* If you already know the IAM actions, you can just run this command to create a template to fill out:

.. code-block:: bash

    policy_sentry create-template --name myRole --output-file actions.yml --template-type actions

* It will generate a file with contents like this:

.. code-block:: yaml

    mode: actions
    name: myRole
    description: '' # Insert value here
    role_arn: '' # Insert value here
    actions:
    - ''  # Fill in your IAM actions here

* Create a yaml file with the following contents:

.. code-block:: yaml

    mode: actions
    name: 'RoleNameWithActions'
    description: 'Justification for privileges' # for auditability
    role_arn: 'arn:aws:iam::123456789102:role/myRole' # for auditability
    actions:
    - kms:CreateGrant
    - kms:CreateCustomKeyStore
    - ec2:AuthorizeSecurityGroupEgress
    - ec2:AuthorizeSecurityGroupIngress


* Then run this command:

.. code-block:: bash

   policy_sentry write-policy --input-file actions.yml


* The output will look like this:

.. code-block:: json


    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "KmsPermissionsmanagementKey",
                "Effect": "Allow",
                "Action": [
                    "kms:creategrant"
                ],
                "Resource": [
                    "arn:aws:kms:${Region}:${Account}:key/${KeyId}"
                ]
            },
            {
                "Sid": "Ec2WriteSecuritygroup",
                "Effect": "Allow",
                "Action": [
                    "ec2:authorizesecuritygroupegress",
                    "ec2:authorizesecuritygroupingress"
                ],
                "Resource": [
                    "arn:aws:ec2:${Region}:${Account}:security-group/${SecurityGroupId}"
                ]
            },
            {
                "Sid": "MultMultNone",
                "Effect": "Allow",
                "Action": [
                    "kms:createcustomkeystore",
                    "cloudhsm:describeclusters"
                ],
                "Resource": [
                    "*"
                ]
            }
        ]
    }


Folder Mode
------------

* **TLDR**: Write Multiple Policies from CRUD mode templates

This command provides the same function as `write-policy`'s CRUD mode, but it can execute all the CRUD mode files in a folder. This is particularly useful in the Terraform use case, where the Terraform module can export a number of Policy Sentry template files into a folder, which can then be consumed using this command.

See the Terraform demo for more details.

.. code-block:: text

   Usage: policy_sentry write-policy-dir [OPTIONS]

   Options:
     --input-dir TEXT    Relative path to Input directory that contains policy_sentry .yml files (CRUD mode only)  [required]
     --output-dir TEXT   Relative path to directory to store AWS JSON policies [required]
     --minimize INTEGER  Minimize the resulting statement with *safe* usage of wildcards to reduce policy length. Set this to the character length you want - for example, 4
     --log-level         Set the logging level. Choices are CRITICAL, ERROR, WARNING, INFO, or DEBUG. Defaults to INFO
     --help              Show this message and exit.
