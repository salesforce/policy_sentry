# ---------------------------------------------------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------------------------------------------------
resource "random_string" "random" {
  length  = 5
  special = false
  upper   = false
  number  = false
}

resource "aws_s3_bucket" "test" {
  bucket = "kinnaird-sfdc-policy_sentry-demo-${random_string.random.result}"
}

resource "aws_ssm_parameter" "test" {
  name  = "/policy_sentry/test-${random_string.random.result}"
  type  = "String"
  value = "bruh"
}

resource "aws_vpc" "test" {
  cidr_block = "10.0.0.0/16"
}
