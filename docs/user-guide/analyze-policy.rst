Analyzing Policies
##################

``analyze-iam-policy``: Reads a policy from a JSON file, expands the wildcards (like ``s3:List*`` if necessary, and audits them to see if certain IAM actions are permitted.

Motivation
^^^^^^^^^^

Let's say you are a developer that handles creation of IAM policies.


* An internal customer asks you to create an IAM policy.
* You haven't been tasked with auditing IAM policies yourself, as that's not your area of expertise, and until this point there is no automation to do it for you.
* However, you want to make sure that the customers aren't asking for permissions that they don't need, since we need to have *some* guardrails in place to prevent unnecessary exposure of attack surfaces.
* This is made more difficult by the fact that sometimes, the customer will give you IAM policies that include ``*`` in the actions. Not only do you want to restrict actions to the specific ARNs, but you want to know what actions they actually need!

You can solve this with policy_sentry too, by auditing for IAM actions in a given policy. Tell them to supply the policy to you in JSON format, and feed it into the ``analyze_iam_policy`` command, as shown below.

Options
^^^^^^^

.. code-block:: text

   Usage: policy_sentry analyze-iam-policy [OPTIONS]

     Analyze IAM Actions given a JSON policy file

   Options:
     --from-audit-file TEXT          The file containing AWS actions to audit. Default path is $HOME/.policy_sentry/audit/permissions-access-level.txt.
     --from-access-level [read|write|list|tagging|permissions-management]
                                     Show CRUD levels. Acceptable values are read, write, list, tagging, permissions-management
     --policy TEXT                   Supply the requester's IAM policy as a JSON file. Accepts relative path.  [required]
     --help                          Show this message and exit.


Instructions
^^^^^^^^^^^^


* Build the database:

.. code-block:: bash

   policy_sentry initialize

Audit for custom list of actions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


* You can specify your own audit file.

.. code-block:: bash

   policy_sentry analyze-iam-policy --from-audit-file ~/.policy_sentry/audit/privilege-escalation.txt --policy examples/analyze/wildcards.json


* ``policy_sentry`` comes bundled with two different audit files, which are located in the ``~/.policy_sentry/audit`` directory. 

  #. privilege-escalation.txt: This is based off of `Rhino Security Labs research <https://github.com/RhinoSecurityLabs/AWS-IAM-Privilege-Escalation>`_
  #. resource-exposure.txt: This is a list of all "Permissions management" actions from the ``policy_sentry`` database.

We plan on supporting more pre-bundled audit files in the future

Audit a policy file for permissions with specific access levels
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


* Command:

.. code-block:: bash

   policy_sentry analyze-iam-policy --from-access-level permissions-management --policy examples/analyze/wildcards.json


* Output:

.. code-block:: text

   Evaluating: examples/analyze/wildcards.json
   Access level: permissions-management
   [   'ecr:setrepositorypolicy',
       's3:objectowneroverridetobucketowner',
       's3:putbucketpolicy',
       's3:putbucketacl',
       's3:putobjectacl',
       's3:putobjectversionacl',
       's3:putaccountpublicaccessblock',
       's3:putbucketpublicaccessblock',
       's3:deletebucketpolicy']

Audit entire folders
~~~~~~~~~~~~~~~~~~~~


* ``policy_sentry`` will detect folders vs. files automatically. Just run the command as usual:

.. code-block:: bash

   policy_sentry analyze-iam-policy --from-access-level permissions-management --policy /Users/username/.policy_sentry/policy-analysis/0123456789012/aws-managed

.. code-block:: text

   Evaluating policy files in /Users/username/.policy_sentry/policy-analysis/0123456789012/aws-managed

   Policy: AmazonSageMakerFullAccess.json
   [   'ec2:createnetworkinterfacepermission',
       'ec2:deletenetworkinterfacepermission',
       'ecr:setrepositorypolicy',
       'iam:createservicelinkedrole',
       'iam:createservicelinkedrole',
       'iam:passrole']

   Policy: AmazonEC2RoleforDataPipelineRole.json
   [   's3:putobjectacl',
       's3:putbucketpolicy',
       's3:putbucketacl',
       's3:objectowneroverridetobucketowner',
       's3:putobjectversionacl',
       's3:putbucketpublicaccessblock',
       's3:deletebucketpolicy',
       's3:putaccountpublicaccessblock',
       'sns:removepermission',
       'sns:addpermission',
       'sqs:addpermission',
       'sqs:removepermission']

   Policy: AWSDataPipelineRole.json
   [   'elasticmapreduce:putblockpublicaccessconfiguration',
       'iam:createservicelinkedrole',
       'iam:passrole',
       's3:putobjectacl',
       's3:putbucketpolicy',
       's3:putbucketacl',
       's3:putobjectversionacl',
       's3:putbucketpublicaccessblock',
       's3:putaccountpublicaccessblock']

   Policy: AWSSupportServiceRolePolicy.json
   ['iam:deleterole', 'lightsail:getinstanceaccessdetails']
