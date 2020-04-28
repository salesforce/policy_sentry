Installation
--------------

* Homebrew

.. code-block:: bash
   brew tap salesforce/policy_sentry https://github.com/salesforce/policy_sentry
   brew install policy_sentry


* pip (Python 3 only)

.. code-block:: bash

   pip3 install --user policy_sentry


Shell completion
~~~~~~~~~~~~~~~~

To enable Bash completion, put this in your `.bashrc`:


.. code-block:: bash

   eval "$(_POLICY_SENTRY_COMPLETE=source policy_sentry)"


To enable ZSH completion, put this in your `.zshrc`:

.. code-block:: bash

   eval "$(_POLICY_SENTRY_COMPLETE=source_zsh policy_sentry)"


Docker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. include:: docker.rst


Rebuilding the IAM Database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. include:: initialize.rst
