
variable "project_name" {
  description = "Name of the GCP Project"
  type        = string
  default     = "yossi-infra-ci-project"
}

variable "service_acount_email" {
  description = "Name of the serviea account"
  type        = string
  default     = "terraform@yossi-infra-ci-project.iam.gserviceaccount.com"
}

variable "artifact_repo_id" {
  description = "the name of the repo in the Artifact Repository"
  type        = string
  default     = "yossi-repo"
}

variable "instance_name" {
  description = "Name of the instance"
  type        = string
  default     = "yossi-db-instance"
}

variable "db_name" {
  description = "Name of the database"
  type        = string
  sensitive   = false
}

variable "db_user" {
  description = "Name of the database user"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Name of the database user"
  type        = string
  sensitive   = true
}
