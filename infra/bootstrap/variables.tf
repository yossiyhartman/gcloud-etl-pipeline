variable "project_name" {
  description = "Name of the GCP Project"
  type        = string
  default     = "yossi-infra-ci-project"
}

variable "sa_account_name" {
  description = "name of the Service Account"
  type        = string
  default     = "terraform"
}
