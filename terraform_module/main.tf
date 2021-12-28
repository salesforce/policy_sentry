module "create_template" {
  source                              = "./ps-template/"
  name                                = var.name
  read_access_level                   = var.read_access_level
  write_access_level                  = var.write_access_level
  list_access_level                   = var.list_access_level
  tagging_access_level                = var.tagging_access_level
  permissions_management_access_level = var.permissions_management_access_level

  wildcard_only_single_actions                 = var.wildcard_only_single_actions
  wildcard_only_read_service                   = var.wildcard_only_read_service
  wildcard_only_write_service                  = var.wildcard_only_write_service
  wildcard_only_list_service                   = var.wildcard_only_list_service
  wildcard_only_tagging_service                = var.wildcard_only_tagging_service
  wildcard_only_permissions_management_service = var.wildcard_only_permissions_management_service

  minimize                  = var.minimize
  skip_resource_constraints = var.skip_resource_constraints
  exclude_actions           = var.exclude_actions
}

module "create_iam" {
  source      = "./iam-policies/"
  region      = var.region
  name        = var.name
  description = var.description
  policy_json = module.create_template.policy_json
}
