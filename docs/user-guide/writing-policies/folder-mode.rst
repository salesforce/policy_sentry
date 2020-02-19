
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
