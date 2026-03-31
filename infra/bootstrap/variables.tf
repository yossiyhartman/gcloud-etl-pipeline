variable "project_name" {
  description = "Name of the GCP Project"
  type        = string
  default     = "yossi-infra-ci-project"
}

variable "region" {
  description = "Region of resouces"
  type        = string
  default     = "europe-west4"
}
