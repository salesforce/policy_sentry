output "file_names" {
  description = "The names of the YML policy files. Used for debugging"
  value       = module.policies.file_names
}

output "iam_policy_arn" {
  description = "The ARN assigned by AWS to this policy."
  value       = module.policies.iam_policy_arn
}

output "iam_policy_name" {
  description = "The name of the policy."
  value       = module.policies.iam_policy_name
}

//
//output "iam_policy_id" {
//  description = "The policy's ID."
//  value       = module.policies.iam_policy_id
//}

//output "iam_policy_policy" {
//  description = "The policy document."
//  value       = aws_iam_policy.policy.*.policy
//}