variable "project_name" {
  description = "Name of the GCP Project"
  type        = string
}

variable "service_account_email" {
  description = "Email of the service account"
  type        = string
}

variable "instance_name" {
  description = "name of the CloudSQL instance"
  type        = string
}
