Analyzing Policies
==================

The following are examples of how to leverage some of the functions
available from Policy Sentry. The functions selected are likely to be of
most interest to other developers.

These ones relate to the analysis features.

Analyzing by access level
-------------------------

Determine if a policy has any actions with a given access level. This is
particularly useful when determining who has 'Permissions management'
level access.

### analysis.analyze_by_access_level

::: {.literalinclude language="python" emphasize-lines="28"}
../../../examples/library-usage/analysis/analyze_by_access_level.py
:::

Expanding actions from a policy file
------------------------------------

::: {.literalinclude language="python" emphasize-lines="28"}
../../../examples/library-usage/analysis/expand_actions_from_policy.py
:::
