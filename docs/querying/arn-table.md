ARN Table
=========

```bash
# Get a list of all RAW ARN formats available through the SSM service.
policy_sentry query arn-table --service ssm

# Get the raw ARN format for the `cloud9` ARN with the short name `environment`
policy_sentry query arn-table --service cloud9 --name environment

# Get key/value pairs of all RAW ARN formats plus their short names
policy_sentry query arn-table --service cloud9 --list-arn-types
```

Options
-------

```text
Usage: policy_sentry query arn-table [OPTIONS]

  Query the ARN Table from the Policy Sentry database

Options:
  --service TEXT     Filter according to AWS service.  [required]
  --name TEXT        The short name of the resource ARN type. For example,
                     `bucket` under service `s3`.
  --list-arn-types   Show the short names of ARN Types. If empty, this will
                     show RAW ARNs only.
  --fmt [yaml|json]  Format output as YAML or JSON. Defaults to "yaml"
    -v, LVL          Either CRITICAL, ERROR, WARNING, INFO or DEBUG
  --help             Show this message and exit.
```


## Examples

### Get a list of all RAW ARN formats available through the service

<details open>
<summary>policy_sentry query arn-table --service ssm</summary>
<br>
<pre>
<code>
arn:${Partition}:ssm:${Region}:${Account}:association/${AssociationId}
arn:${Partition}:ssm:${Region}:${Account}:automation-execution/${AutomationExecutionId}
arn:${Partition}:ssm:${Region}:${Account}:automation-definition/${AutomationDefinitionName:VersionId}
arn:${Partition}:ssm:${Region}:${Account}:document/${DocumentName}
arn:${Partition}:ec2:${Region}:${Account}:instance/${InstanceId}
arn:${Partition}:ssm:${Region}:${Account}:maintenancewindow/${ResourceId}
arn:${Partition}:ssm:${Region}:${Account}:managed-instance/${ManagedInstanceName}
arn:${Partition}:ssm:${Region}:${Account}:managed-instance-inventory/${InstanceId}
arn:${Partition}:ssm:${Region}:${Account}:opsitem/${ResourceId}
arn:${Partition}:ssm:${Region}:${Account}:parameter/${FullyQualifiedParameterName}
arn:${Partition}:ssm:${Region}:${Account}:patchbaseline/${PatchBaselineIdResourceId}
arn:${Partition}:ssm:${Region}:${Account}:session/${SessionId}
arn:${Partition}:ssm:${Region}:${Account}:resource-data-sync/${SyncName}
arn:${Partition}:ssm:${Region}:${Account}:servicesetting/${ResourceId}
arn:${Partition}:ssm:${Region}:${Account}:windowtarget/${WindowTargetId}
arn:${Partition}:ssm:${Region}:${Account}:windowtask/${WindowTaskId}
</code>
</pre>
</details>

### Get a list of all the ARN type names per service, paired with the Raw ARN format

<details open>
<summary>policy_sentry query arn-table --service ssm --list-arn-types</summary>
<br>
<pre>
<code>
{
    "association": "arn:${Partition}:ssm:${Region}:${Account}:association/${AssociationId}",
    "automation-execution": "arn:${Partition}:ssm:${Region}:${Account}:automation-execution/${AutomationExecutionId}",
    "automation-definition": "arn:${Partition}:ssm:${Region}:${Account}:automation-definition/${AutomationDefinitionName:VersionId}",
    "document": "arn:${Partition}:ssm:${Region}:${Account}:document/${DocumentName}",
    "instance": "arn:${Partition}:ec2:${Region}:${Account}:instance/${InstanceId}",
    "maintenancewindow": "arn:${Partition}:ssm:${Region}:${Account}:maintenancewindow/${ResourceId}",
    "managed-instance": "arn:${Partition}:ssm:${Region}:${Account}:managed-instance/${ManagedInstanceName}",
    "managed-instance-inventory": "arn:${Partition}:ssm:${Region}:${Account}:managed-instance-inventory/${InstanceId}",
    "opsitem": "arn:${Partition}:ssm:${Region}:${Account}:opsitem/${ResourceId}",
    "parameter": "arn:${Partition}:ssm:${Region}:${Account}:parameter/${FullyQualifiedParameterName}",
    "patchbaseline": "arn:${Partition}:ssm:${Region}:${Account}:patchbaseline/${PatchBaselineIdResourceId}",
    "session": "arn:${Partition}:ssm:${Region}:${Account}:session/${SessionId}",
    "resourcedatasync": "arn:${Partition}:ssm:${Region}:${Account}:resource-data-sync/${SyncName}",
    "servicesetting": "arn:${Partition}:ssm:${Region}:${Account}:servicesetting/${ResourceId}",
    "windowtarget": "arn:${Partition}:ssm:${Region}:${Account}:windowtarget/${WindowTargetId}",
    "windowtask": "arn:${Partition}:ssm:${Region}:${Account}:windowtask/${WindowTaskId}"
}
</code>
</pre>
</details>

### Get the raw ARN format for the `cloud9` service with the short name `environment`

<details open>
<summary>policy_sentry query arn-table --service cloud9 --name environment</summary>
<br>
<pre>
<code>
{
    "resource_type_name": "environment",
    "raw_arn": "arn:${Partition}:cloud9:${Region}:${Account}:environment:${ResourceId}",
    "condition_keys": [
        "aws:ResourceTag/${TagKey}"
    ]
}
</code>
</pre>
</details>
