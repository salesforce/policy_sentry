output "iam_policy_id" {
  description = "The policy's ID."
  value       = aws_iam_policy.policy.id
}

output "iam_policy_arn" {
  description = "The ARN assigned by AWS to this policy."
  value       = aws_iam_policy.policy.arn
}

output "iam_policy_name" {
  description = "The name of the policy."
  value       = aws_iam_policy.policy.name
}

output "iam_policy_path" {
  description = "The path of the policy in IAM"
  value       = aws_iam_policy.policy.path
}

output "iam_policy_document" {
  description = "The policy document."
  value       = aws_iam_policy.policy.policy
}
