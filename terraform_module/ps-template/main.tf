# ---------------------------------------------------------------------------------------------------------------------
# Locals to create the policies
# ---------------------------------------------------------------------------------------------------------------------

locals {
  file = "${var.name}.json"
  policy_sentry_template = {
    "mode" : "crud",
    "read" : var.read_access_level,
    "write" : var.write_access_level,
    "list" : var.list_access_level,
    "tagging" : var.tagging_access_level
    "permissions-management" : var.permissions_management_access_level,
    "wildcard-only" : {
      "single-actions" : var.wildcard_only_single_actions,
      "service-read" : var.wildcard_only_read_service,
      "service-write" : var.wildcard_only_write_service,
      "service-list" : var.wildcard_only_list_service,
      "service-tagging" : var.wildcard_only_tagging_service,
      "service-permissions-management" : var.wildcard_only_permissions_management_service,
    },
    "exclude-actions" : var.exclude_actions,
    "skip-resource-constraints" : var.skip_resource_constraints
  }
  rendered_template = jsonencode(local.policy_sentry_template)
  decoded_template  = jsondecode(jsonencode(local.policy_sentry_template))
  policy_sentry     = ["policy_sentry", "write-policy", "--fmt", "terraform"]
  command           = var.minimize ? concat(local.policy_sentry, ["--minimize"]) : local.policy_sentry
}

resource "local_file" "template" {
  filename = "template.json"
  content  = local.rendered_template
}

data "external" "policy" {
  program    = concat(local.command, ["--input-file", local_file.template.filename])
  depends_on = [local_file.template]
}

