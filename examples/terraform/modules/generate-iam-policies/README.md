# generate-iam-policies

This generates IAM policies based on JSON files in a specified folder. This is ideal for usage with policy_sentry-generated IAM Policies.

## Usage

From the `environments/iam-resources/` directory, which shows the example usage of this.

```hcl-terraform
module "policies" {
  source                             = "../../modules/generate-iam-policies"
  relative_path_to_json_policy_files = "files"
}
```

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| relative\_path\_to\_json\_policy\_files | Path to the folder containing your policy_sentry-generated JSON policy files. | string | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| file\_names | The .json files loaded |
| iam\_policy\_arn | The ARN assigned by AWS to this policy. |
| iam\_policy\_id | The policy's ID. |
| iam\_policy\_name | The name of the policy. |
| iam\_policy\_path | The path of the policy in IAM |
| iam\_policy\_policy | The policy document. |

<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
