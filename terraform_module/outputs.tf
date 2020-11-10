output "iam_policy_id" {
  description = "The policy's ID."
  value       = module.create_iam.iam_policy_id
}

output "iam_policy_arn" {
  description = "The ARN assigned by AWS to this policy."
  value       = module.create_iam.iam_policy_arn
}

output "iam_policy_name" {
  description = "The name of the policy."
  value       = module.create_iam.iam_policy_name
}

output "iam_policy_path" {
  description = "The path of the policy in IAM"
  value       = module.create_iam.iam_policy_path
}

output "iam_policy_document" {
  description = "The policy document."
  value       = jsondecode(module.create_iam.iam_policy_document)
}
