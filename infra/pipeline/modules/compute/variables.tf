variable "project_name" {
  description = "Name of the GCP Project"
  type        = string
}

variable "service_acount_email" {
  description = "Name of the serviea account"
  type        = string
  default     = "terraform@yossi-infra-ci-project.iam.gserviceaccount.com"
}
