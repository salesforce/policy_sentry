variable "name" {
  description = "The name of the rendered policy file (no file extension)."
  type        = string
}

variable "minimize" {
  description = "If set to true, it will minimize the size of the IAM Policy file. Defaults to false."
  default     = false
  type        = bool
}

variable "read_access_level" {
  description = "Provide a list of Amazon Resource Names (ARNs) that your role needs READ access to."
  type        = list(string)
  default     = []
}

variable "write_access_level" {
  description = "Provide a list of Amazon Resource Names (ARNs) that your role needs WRITE access to."
  type        = list(string)
  default     = []
}

variable "list_access_level" {
  description = "Provide a list of Amazon Resource Names (ARNs) that your role needs LIST access to."
  type        = list(string)
  default     = []
}

variable "tagging_access_level" {
  description = "Provide a list of Amazon Resource Names (ARNs) that your role needs TAGGING access to."
  type        = list(string)
  default     = []
}

variable "permissions_management_access_level" {
  description = "Provide a list of Amazon Resource Names (ARNs) that your role needs PERMISSIONS MANAGEMENT access to."
  type        = list(string)
  default     = []
}

variable "wildcard_only_single_actions" {
  description = "Individual actions that do not support resource constraints. For example, s3:ListAllMyBuckets"
  type        = list(string)
  default     = []
}

variable "wildcard_only_read_service" {
  description = "To generate a list of AWS service actions that (1) are at the READ access level and (2) do not support resource constraints, list the service prefix here."
  type        = list(string)
  default     = []
}

variable "wildcard_only_write_service" {
  description = "To generate a list of AWS service actions that (1) are at the WRITE access level and (2) do not support resource constraints, list the service prefix here."
  type        = list(string)
  default     = []
}

variable "wildcard_only_list_service" {
  description = "To generate a list of AWS service actions that (1) are at the LIST access level and (2) do not support resource constraints, list the service prefix here."
  type        = list(string)
  default     = []
}

variable "wildcard_only_tagging_service" {
  description = "To generate a list of AWS service actions that (1) are at the TAGGING access level and (2) do not support resource constraints, list the service prefix here."
  type        = list(string)
  default     = []
}

variable "wildcard_only_permissions_management_service" {
  description = "To generate a list of AWS service actions that (1) are at the PERMISSIONS MANAGEMENT access level and (2) do not support resource constraints, list the service prefix here."
  type        = list(string)
  default     = []
}

variable "skip_resource_constraints" {
  description = "Skip resource constraint requirements by listing individual actions here, like s3:GetObject."
  type        = list(string)
  default     = []
}

variable "exclude_actions" {
  description = "Exclude actions from the output by specifying them here. Accepts wildcards, like kms:Delete*"
  type        = list(string)
  default     = []
}
