# ps-template

This generates the JSON policy file with Policy Sentry.

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Requirements

| Name | Version |
|------|---------|
| terraform | >= 0.12.8 |
| local | ~> 1.3 |

## Providers

| Name | Version |
|------|---------|
| external | n/a |
| local | ~> 1.3 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| exclude\_actions | Exclude actions from the output by specifying them here. Accepts wildcards, like kms:Delete\* | `list(string)` | `[]` | no |
| list\_access\_level | Provide a list of Amazon Resource Names (ARNs) that your role needs LIST access to. | `list(string)` | `[]` | no |
| minimize | If set to true, it will minimize the size of the IAM Policy file. Defaults to false. | `bool` | `false` | no |
| name | The name of the rendered policy file (no file extension). | `string` | n/a | yes |
| permissions\_management\_access\_level | Provide a list of Amazon Resource Names (ARNs) that your role needs PERMISSIONS MANAGEMENT access to. | `list(string)` | `[]` | no |
| read\_access\_level | Provide a list of Amazon Resource Names (ARNs) that your role needs READ access to. | `list(string)` | `[]` | no |
| skip\_resource\_constraints | Skip resource constraint requirements by listing individual actions here, like s3:GetObject. | `list(string)` | `[]` | no |
| tagging\_access\_level | Provide a list of Amazon Resource Names (ARNs) that your role needs TAGGING access to. | `list(string)` | `[]` | no |
| wildcard\_only\_list\_service | To generate a list of AWS service actions that (1) are at the LIST access level and (2) do not support resource constraints, list the service prefix here. | `list(string)` | `[]` | no |
| wildcard\_only\_permissions\_management\_service | To generate a list of AWS service actions that (1) are at the PERMISSIONS MANAGEMENT access level and (2) do not support resource constraints, list the service prefix here. | `list(string)` | `[]` | no |
| wildcard\_only\_read\_service | To generate a list of AWS service actions that (1) are at the READ access level and (2) do not support resource constraints, list the service prefix here. | `list(string)` | `[]` | no |
| wildcard\_only\_single\_actions | Individual actions that do not support resource constraints. For example, s3:ListAllMyBuckets | `list(string)` | `[]` | no |
| wildcard\_only\_tagging\_service | To generate a list of AWS service actions that (1) are at the TAGGING access level and (2) do not support resource constraints, list the service prefix here. | `list(string)` | `[]` | no |
| wildcard\_only\_write\_service | To generate a list of AWS service actions that (1) are at the WRITE access level and (2) do not support resource constraints, list the service prefix here. | `list(string)` | `[]` | no |
| write\_access\_level | Provide a list of Amazon Resource Names (ARNs) that your role needs WRITE access to. | `list(string)` | `[]` | no |

## Outputs

| Name | Description |
|------|-------------|
| file\_name | The path of the file. |
| policy\_json | The contents of the policy |
| policy\_sentry\_template\_contents | The contents of the Policy Sentry template |

<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
