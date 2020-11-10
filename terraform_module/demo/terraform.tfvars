name = "PolicySentryTest"

list_access_level = [
  "arn:aws:s3:::list-org",
  "arn:aws:s3:::sup-org",
]
read_access_level = [
  "arn:aws:s3:::bruh",
]
write_access_level = [
  "arn:aws:kms:us-east-1:123456789012:key/shaq"
]

skip_resource_constraints = ["s3:GetObject"]

exclude_actions = ["kms:Delete*"]

# minimize = true
