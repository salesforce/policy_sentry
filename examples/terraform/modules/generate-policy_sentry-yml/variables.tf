variable "yml_file_destination_folder" {
  description = "The path where your policy_sentry YML file will be stored."
}

variable "role_name" {
  description = "Name of the Role that will have this policy attached."
  type        = "string"
}

variable "role_description" {
  description = "Description of why you need these privileges."
  type        = "string"
}

variable "role_arn" {
  description = "The ARN of your role."
  type        = "string"
}

variable "read_access_level" {
  description = "Provide a list of Amazon Resource Names (ARNs) that your role needs READ access to."
  type        = "list"
}

variable "write_access_level" {
  description = "Provide a list of Amazon Resource Names (ARNs) that your role needs WRITE access to."
  type        = "list"
}

variable "list_access_level" {
  description = "Provide a list of Amazon Resource Names (ARNs) that your role needs LIST access to."
  type        = "list"
}

variable "tagging_access_level" {
  description = "Provide a list of Amazon Resource Names (ARNs) that your role needs TAGGING access to."
  type        = "list"
}

variable "permissions_management_access_level" {
  description = "Provide a list of Amazon Resource Names (ARNs) that your role needs PERMISSIONS MANAGEMENT access to."
  type        = "list"
}
