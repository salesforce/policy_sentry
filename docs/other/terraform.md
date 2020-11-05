Terraform
=========

The Terraform module is published
[here](https://github.com/kmcquade/terraform-aws-policy-sentry).

Prerequisites
-------------

1.  You must have Policy Sentry (at least version 0.7.0.2) installed beforehand and it must be executable from your `$PATH]`. Installation instructions are [here](https://policy-sentry.readthedocs.io/en/latest/user-guide/installation.html).
2.  You must have at least Terraform 0.12.8 installed.

Note
----

-   **Note**: You will have to run `terraform apply` **twice**. This is because Policy Sentry has to create the template JSON file in the first run (executing python as part of the Terraform build), and it will create the actual IAM policy in the second run. While it is not as transparent as other Terraform modules in this way, it is still fairly transparent to the user.

Follow the rest of the demo for more context and details.

Example
-------

1.  In your example directory, create a file titled `main.tf` with the following contents:

    ```hcl
    module "policy_sentry_demo" {
    source                              = "github.com/kmcquade/terraform-aws-policy-sentry"
    name                                = var.name
    read_access_level                   = var.read_access_level
    write_access_level                  = var.write_access_level
    list_access_level                   = var.list_access_level
    tagging_access_level                = var.tagging_access_level
    permissions_management_access_level = var.permissions_management_access_level
    wildcard_only_actions               = var.wildcard_only_actions
    minimize                            = var.minimize
    }
    ```

2.  Create a file titled `variables.tf` with the following
    contents:

    ```hcl
    variable "name" {
    description = "The name of the rendered policy file (no file extension)."
    type        = "string"
    }

    variable "create_policy" {
    description = "Set to true to create the actual IAM policies. Defaults to true."
    default     = true
    type        = bool
    }

    variable "read_access_level" {
    description = "Provide a list of Amazon Resource Names (ARNs) that your role needs READ access to."
    type        = "list"
    default     = [""]
    }

    variable "write_access_level" {
    description = "Provide a list of Amazon Resource Names (ARNs) that your role needs WRITE access to."
    type        = "list"
    default     = [""]
    }

    variable "list_access_level" {
    description = "Provide a list of Amazon Resource Names (ARNs) that your role needs LIST access to."
    type        = "list"
    default     = [""]
    }

    variable "tagging_access_level" {
    description = "Provide a list of Amazon Resource Names (ARNs) that your role needs TAGGING access to."
    type        = "list"
    default     = [""]
    }

    variable "permissions_management_access_level" {
    description = "Provide a list of Amazon Resource Names (ARNs) that your role needs PERMISSIONS MANAGEMENT access to."
    type        = "list"
    default     = [""]
    }

    variable "wildcard_only_actions" {
    description = "Only actions that do not support resource constraints"
    type        = "list"
    default     = [""]
    }

    variable "minimize" {
    description = "If set to true, it will minimize the size of the IAM Policy file. Defaults to false."
    default     = false
    type        = bool
    }
    ```

3.  Then fill out the parameters appropriately in `terraform.tfvars`. Note that the `name` parameter will equal the name of your new IAM policy. `list_access_level`,
    `read_access_level`, etc. correspond to the values
    that you would normally pass in with the YML file in Policy Sentry.

    ```hcl
    name = "PolicySentryTest"

    list_access_level = [
    "arn:aws:s3:::my-bucket",
    "arn:aws:s3:::my-other-bucket",
    ]
    read_access_level = [
    "arn:aws:s3:::my-other-bucket",
    ]
    write_access_level = [
    "arn:aws:kms:us-east-1:123456789012:key/shaq"
    ]
    ```

4.  Run `terraform apply]` once to create the JSON policy file.

    ![](https://i.imgur.com/dn80hE0.gif)

5.  Run `terraform apply` **again** to create the IAM policy

    ![](https://i.imgur.com/ndIXTQb.gif)

6.  Don't forget to cleanup

    ```bash
    terraform destroy -auto-approve
    ```
