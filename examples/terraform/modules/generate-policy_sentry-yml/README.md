# generate-policy_sentry-yml

Generates 

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| list\_access\_level | Provide a list of Amazon Resource Names \(ARNs\) that your role needs LIST access to. | list | n/a | yes |
| permissions\_management\_access\_level | Provide a list of Amazon Resource Names \(ARNs\) that your role needs PERMISSIONS MANAGEMENT access to. | list | n/a | yes |
| read\_access\_level | Provide a list of Amazon Resource Names \(ARNs\) that your role needs READ access to. | list | n/a | yes |
| role\_arn | The ARN of your role. | string | n/a | yes |
| role\_description | Description of why you need these privileges. | string | n/a | yes |
| role\_name | Name of the Role that will have this policy attached. | string | n/a | yes |
| tagging\_access\_level | Provide a list of Amazon Resource Names \(ARNs\) that your role needs TAGGING access to. | list | n/a | yes |
| write\_access\_level | Provide a list of Amazon Resource Names \(ARNs\) that your role needs WRITE access to. | list | n/a | yes |
| yml\_file\_destination\_folder | The path where your policy_sentry YML file will be stored. | string | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| file\_name | The path of the file. |

<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
