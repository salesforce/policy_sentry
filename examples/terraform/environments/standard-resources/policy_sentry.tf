module "policy_sentry_yml" {
  source           = "../../modules/generate-policy_sentry-yml"
  role_name        = "example-role-${random_string.random.result}"
  role_description = "bruh"
  role_arn         = "arn:aws:iam::123456789012:role/example-role-${random_string.random.result}"

  list_access_level = [
    aws_s3_bucket.test.arn,
    aws_ssm_parameter.test.arn,
    aws_vpc.test.arn,
  ]
  permissions_management_access_level = [
    aws_ssm_parameter.test.arn,
  ]
  read_access_level = [
    aws_s3_bucket.test.arn,
    aws_ssm_parameter.test.arn,
    aws_vpc.test.arn
  ]
  tagging_access_level = [
    aws_vpc.test.arn
  ]
  write_access_level = [
    aws_vpc.test.arn,
    "${aws_s3_bucket.test.arn}/my-path",
  ]
  yml_file_destination_folder = "../iam-resources/files"
}
