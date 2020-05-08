Querying the IAM Database
=========================

The following are examples of how to leverage some of the functions
available from Policy Sentry. The functions selected are likely to be of
most interest to other developers.

These ones relate to querying the IAM database.

All
---

### querying.all.get_all_services

::: {.literalinclude language="python" emphasize-lines="8"}
../../../examples/library-usage/querying/all/get_all_service_prefixes.py
:::

### querying.all.get_all_actions

::: {.literalinclude language="python" emphasize-lines="8"}
../../../examples/library-usage/querying/all/get_all_actions.py
:::

Actions
-------

### querying.actions.get_action_data

::: {.literalinclude language="python" emphasize-lines="8"}
../../../examples/library-usage/querying/actions/get_action_data.py
:::

### querying.actions.get_actions_for_service

::: {.literalinclude language="python" emphasize-lines="8"}
../../../examples/library-usage/querying/actions/get_actions_for_service.py
:::

### querying.actions.get_actions_matching_condition_key

::: {.literalinclude language="python" emphasize-lines="8"}
../../../examples/library-usage/querying/actions/get_actions_matching_condition_key.py
:::

### querying.actions.get_actions_supporting_wilcards_only

::: {.literalinclude language="python" emphasize-lines="8"}
../../../examples/library-usage/querying/actions/get_actions_matching_condition_key.py
:::

### querying.actions.get_actions_with_access_levels

::: {.literalinclude language="python" emphasize-lines="8"}
../../../examples/library-usage/querying/actions/get_actions_with_access_level.py
:::

### querying.actions.get_actions_with_arn_type_and_access_level

::: {.literalinclude language="python" emphasize-lines="8"}
../../../examples/library-usage/querying/actions/get_actions_with_arn_type_and_access_level.py
:::

### querying.actions.get_dependent_actions

::: {.literalinclude language="python" emphasize-lines="8"}
../../../examples/library-usage/querying/actions/get_dependent_actions.py
:::

ARNs
----

### querying.arns.get_arn_type_details

::: {.literalinclude language="python" emphasize-lines="8"}
../../../examples/library-usage/querying/arns/get_arn_type_details.py
:::

### querying.arns.get_arn_types_for_service

::: {.literalinclude language="python" emphasize-lines="8"}
../../../examples/library-usage/querying/arns/get_arn_types_for_service.py
:::

### querying.arns.get_raw_arns_for_service

::: {.literalinclude language="python" emphasize-lines="8"}
../../../examples/library-usage/querying/arns/get_raw_arns_for_service.py
:::

Conditions
----------

### querying.conditions.get_condition_key_details

::: {.literalinclude language="python" emphasize-lines="8"}
../../../examples/library-usage/querying/conditions/get_condition_key_details.py
:::

### querying.conditions.get_condition_keys_for_service

::: {.literalinclude language="python" emphasize-lines="8"}
../../../examples/library-usage/querying/conditions/get_condition_keys_for_service.py
:::
