Policy Sentry Documentation
==========================================================

Policy Sentry is an AWS IAM Least Privilege Policy Generator, auditor, and analysis database. It compiles database tables based on the AWS IAM Documentation on `Actions, Resources, and Condition Keys <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html>`__ and leverages that data to create least-privilege IAM policies.

Organizations can use Policy Sentry to:

* **Limit the blast radius in the event of a breach**\: If an attacker gains access to user credentials or Instance Profile credentials, access levels and resource access should be limited to the least amount needed to function. This can help avoid situations such as the Capital One breach, where after an SSRF attack, data was accessible from the compromised instance because the role allowed access to all S3 buckets in the account. In this case, Policy Sentry would only allow the role access to the buckets necessary to perform its duties.
* **Scale creation of secure IAM Policies**\: Rather than dedicating specialized and talented human resources to manual IAM reviews and creating IAM policies by hand, organizations can leverage Policy Sentry to write the policies for them in an automated fashion.

Policy Sentry's policy writing templates are expressed in YAML and include the following:

* Name and Justification for why the privileges are needed
* CRUD levels (Read/Write/List/Tagging/Permissions management)
* Amazon Resource Names (ARNs), so the resulting policy only points to specific resources and does not grant access to `*` resources.

Policy Sentry can also be used to:

* `Audit IAM Policies <https://policy-sentry.readthedocs.io/en/latest/user-guide/analyze-policy.html>`__ based on access levels
* `Query the IAM database <https://policy-sentry.readthedocs.io/en/latest/user-guide/querying-the-database.html>`__ to reduce manual search time
* `Download live policies <https://policy-sentry.readthedocs.io/en/latest/user-guide/downloading-policies.html>`__ from an AWS account auditing purposes
* `Generate IAM Policies based on Terraform output <https://policy-sentry.readthedocs.io/en/latest/terraform/terraform-demo.html>`__
* `Write least-privilege IAM Policies <https://policy-sentry.readthedocs.io/en/latest/user-guide/write-policy.html>`__ based on a list of IAM actions (or CRUD levels)


Navigate below to get started with Policy Sentry!


.. toctree::
   :maxdepth: 1
   :caption: Introduction

   introduction/home
   introduction/comparison-to-similar-tools

.. toctree::
   :maxdepth: 1
   :caption: User Guide

   user-guide/installation
   user-guide/initialize
   user-guide/write-policy
   user-guide/downloading-policies
   user-guide/analyze-policy
   user-guide/querying-the-database
   user-guide/usage-as-a-python-package
   user-guide/docker
   user-guide/command-cheat-sheet

.. toctree::
   :maxdepth: 1
   :caption: Terraform

   terraform/terraform-demo
   terraform/terraform-modules


.. toctree::
   :maxdepth: 1
   :caption: Contributing

   contributing/index.rst

..
    .. toctree::
       :maxdepth: 1
       :caption: Module Index
       module-index/modules.rst


.. toctree::
   :maxdepth: 1
   :caption: Appendix

   appendix/implementation-strategy


.. toctree::
   :maxdepth: 1
   :caption: IAM Background

   iam-knowledge/iam-policies
   iam-knowledge/minimization


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

