module "policy_sentry_demo" {
  source                              = "../"
  name                                = var.name
  read_access_level                   = var.read_access_level
  write_access_level                  = var.write_access_level
  list_access_level                   = var.list_access_level
  tagging_access_level                = var.tagging_access_level
  permissions_management_access_level = var.permissions_management_access_level
  wildcard_only_single_actions        = var.wildcard_only_single_actions
  minimize                            = var.minimize
}

terraform {
  required_version = "~> 0.12.8"
}
