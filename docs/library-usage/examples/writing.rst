Writing Policies
================

The following are examples of how to leverage some of the functions available from Policy Sentry. The functions selected are likely to be of most interest to other developers.

These ones refer to leveraging Policy Sentry as a library to write IAM policies.

Actions Mode: Writing Policies by providing a list of Actions
-------------------------------------------------------------


.. literalinclude:: ../../../examples/library-usage/writing/write_policy_with_actions.py
   :language: python
   :emphasize-lines: 15-18


CRUD Mode: Writing Policies by Access Levels and ARNs
-----------------------------------------------------

.. literalinclude:: ../../../examples/library-usage/writing/write_policy_with_access_levels.py
   :language: python
   :emphasize-lines: 13-26
