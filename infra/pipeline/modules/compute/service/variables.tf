variable "region" {
  type        = string
  description = "Default region for resources"
}

variable "service_account" {
  type        = string
  description = "provide"
  default     = null
}

variable "service_name" {
  type        = string
  description = "name of the service"
}

variable "image" {
  type        = string
  description = "name of the image to link to the job"
}

variable "cmd_override" {
  type        = list(string)
  description = "override the command specified in the job's image"
  default     = []
}

variable "env_variables" {
  type    = map(string)
  default = {}
}

variable "env_secrets" {
  type    = map(string)
  default = {}
}
