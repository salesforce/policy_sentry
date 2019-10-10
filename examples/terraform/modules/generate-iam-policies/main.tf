locals {
  # Since policy_sentry already ran and sent its output to the policies-json directory,
  #   let's read all the files from that directory that end in .json
  policy_sentry_filenames = tolist(fileset("${var.relative_path_to_json_policy_files}/", "*.json"))
}

data "local_file" "foo" {
  count    = length(local.policy_sentry_filenames)
  filename = format("%s/%s", var.relative_path_to_json_policy_files, local.policy_sentry_filenames[count.index])
}

# Takes the relative path to the .json policy; remove the folder name and the extension. This will be our policy name
resource "aws_iam_policy" "policy" {
  count       = length(data.local_file.foo)
  name        = replace(replace(data.local_file.foo.*.filename[count.index], "${var.relative_path_to_json_policy_files}/", ""), ".json", "")
  path        = "/"
  description = "policy_sentry generated policy"
  policy      = data.local_file.foo.*.content[count.index]
}
