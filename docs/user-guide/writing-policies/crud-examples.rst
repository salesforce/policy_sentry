CRUD Mode Examples
==================

This will show valid template inputs and their outputs for CRUD mode. CRUD mode may appear to be complicated, but in reality it is quite simple. This page will avoid being overly explanatory and will just show the input and output as a reference.


Example 1: Basic CRUD
---------------------

The basic CRUD mode gives you actions at the specified access level, constrained to the specific resource ARNs supplied.

**Input**:

.. code-block:: yaml

    mode: crud
    read:
    - 'arn:aws:ssm:us-east-1:123456789012:parameter/myparameter'

**Output**:

.. code-block:: json

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "SsmReadParameter",
                "Effect": "Allow",
                "Action": [
                    "ssm:GetParameter",
                    "ssm:GetParameterHistory",
                    "ssm:GetParameters",
                    "ssm:GetParametersByPath",
                    "ssm:ListTagsForResource"
                ],
                "Resource": [
                    "arn:aws:ssm:us-east-1:123456789012:parameter/myparameter"
                ]
            }
        ]
    }


Example 2: Skipping Resource Constraints
------------------------------------------

In basic CRUD mode, Policy Sentry forces you to use resource constraints, but perhaps you do want to allow `kms:Decrypt` to `*` and there are mitigating circumstances that mean it is not a security risk to your organization. For example - let's say that given the context of your organization and its AWS security strategy, you can’t know the KMS Key Alias or Key ID beforehand. However, all of the KMS  keys are tightly controlled via resource based policies and provisioned via Terraform/Cloudformation, therefore `kms:Decrypt` is ok. And in order to use Policy Sentry you’d need a way to handle exceptions/overrides.

The `skip-resource-constraints` section allows you to do this.

We avoid abuse by requiring that if you list actions under the skip-resource-constraints section, then you should have to list the actions out individually (I.e., don’t allow S3:*)

**Input**:

.. code-block:: yaml

    mode: crud
    skip-resource-constraints:
    - s3:GetObject
    - s3:PutObject
    - ssm:GetParameter
    - ssm:GetParameters


**Output**:

.. code-block:: json

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "SkipResourceConstraints",
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject",
                    "ssm:GetParameter",
                    "ssm:GetParameters"
                ],
                "Resource": [
                    "*"
                ]
            }
        ]
    }


Example 3: Wildcard-only - Single Actions
-----------------------------------------

This is for actions that do not support resource ARN constraints, such as `secretsmanager:CreateSecret`.

**Input**:

.. code-block:: yaml

    mode: crud
    wildcard-only:
        single-actions:
        - secretsmanager:CreateSecret

**Output**:

.. code-block:: json

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "MultMultNone",
                "Effect": "Allow",
                "Action": [
                    "secretsmanager:CreateSecret"
                ],
                "Resource": [
                    "*"
                ]
            }
        ]
    }


Example 4: Wildcard only - Bulk Selection Service-Wide
------------------------------------------------------

As mentioned before, there are some actions that do not support resource constraints - but all of those actions have access levels. You can use this strategy to "bulk select" wildcard-only actions at different access levels. It improves the user experience so you don't have to actually know the details of individual IAM Actions, just the service prefixes and access levels.

**Input**:

.. code-block:: yaml

    mode: crud
    wildcard-only:
        service-list:
        - s3


**Output**:

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
