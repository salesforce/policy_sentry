Condition Table
===============

```bash
# Get a list of all condition keys available to the Cloud9 service
policy_sentry query condition-table --service cloud9

# Get details on the condition key titled `cloud9:Permissions`
policy_sentry query condition-table --service cloud9 --name cloud9:Permissions
```

Options
-------

```text
Usage: policy_sentry query condition-table [OPTIONS]

  Query the condition keys table from the Policy Sentry database

Options:
  --name TEXT        Get details on a specific condition key. Leave this blank
                     to get a list of all condition keys available to the
                     service.
  --service TEXT     Filter according to AWS service.  [required]
  --fmt [yaml|json]  Format output as YAML or JSON. Defaults to "yaml"
    -v, LVL          Either CRITICAL, ERROR, WARNING, INFO or DEBUG
  --help             Show this message and exit.
```
