module "policies" {
  source                             = "../../modules/generate-iam-policies"
  relative_path_to_json_policy_files = "files"
}