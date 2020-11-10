output "file_name" {
  value       = "${var.name}.json"
  description = "The path of the file."
}

output "policy_sentry_template_contents" {
  description = "The contents of the Policy Sentry template"
  value       = local.rendered_template
}

output "policy_json" {
  description = "The contents of the policy"
  value       = data.external.policy.result.policy
}
