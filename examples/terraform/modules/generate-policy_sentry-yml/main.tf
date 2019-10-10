# ---------------------------------------------------------------------------------------------------------------------
# Locals to create the policies
# ---------------------------------------------------------------------------------------------------------------------

locals {
  # This makes it in the yaml format
  //  policy_sentry_yaml_role_name                   = format("    - %s", var.role_name)
  //  policy_sentry_yaml_role_description            = format("    - %s", var.role_description)
  //  policy_sentry_yaml_role_arn                    = format("    - %s", var.role_arn)/**/
  policy_sentry_yaml_read                   = formatlist("    - %s", var.read_access_level)
  policy_sentry_yaml_write                  = formatlist("    - %s", var.write_access_level)
  policy_sentry_yaml_list                   = formatlist("    - %s", var.list_access_level)
  policy_sentry_yaml_tag                    = formatlist("    - %s", var.tagging_access_level)
  policy_sentry_yaml_permissions_management = formatlist("    - %s", var.permissions_management_access_level)
}

resource "local_file" "policy_sentry_acl_yml_file" {
  //  filename = "${path.module}/${var.yml_file_destination_folder}/${var.role_name}.yml"
  filename = "${var.yml_file_destination_folder}/${var.role_name}.yml"

  content = templatefile(
    "${path.module}/templates/policy_sentry-template.yml", {
      //      policy_sentry_role_name                   = yamlencode(local.policy_sentry_yaml_role_name)
      //      policy_sentry_role_description            = yamlencode(local.policy_sentry_yaml_role_description)
      //      policy_sentry_role_arn                    = yamlencode(local.policy_sentry_yaml_role_name)
      policy_sentry_role_name                   = var.role_name
      policy_sentry_role_description            = var.role_description
      policy_sentry_role_arn                    = var.role_arn
      policy_sentry_yaml_write                  = join("\n", local.policy_sentry_yaml_write)
      policy_sentry_yaml_read                   = join("\n", local.policy_sentry_yaml_read)
      policy_sentry_yaml_list                   = join("\n", local.policy_sentry_yaml_list)
      policy_sentry_yaml_permissions_management = join("\n", local.policy_sentry_yaml_permissions_management)
      policy_sentry_yaml_tag                    = join("\n", local.policy_sentry_yaml_tag)
    }
  )
}
