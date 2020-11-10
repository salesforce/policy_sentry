# Takes the relative path to the .json policy; remove the folder name and the extension. This will be our policy name
resource "aws_iam_policy" "policy" {
  name        = var.name
  path        = "/"
  description = var.description
  policy      = data.aws_iam_policy_document.policy.json
}

data "aws_iam_policy_document" "policy" {
  source_json = var.policy_json
}

