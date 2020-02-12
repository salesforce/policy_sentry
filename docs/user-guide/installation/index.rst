Installation
--------------

* ``policy_sentry`` is available via pip (Python 3 only). To install, run:

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
