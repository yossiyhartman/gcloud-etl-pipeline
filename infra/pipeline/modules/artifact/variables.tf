variable "project_name" {
  type        = string
  description = "Name of the GCP Project"
}

variable "region" {
  type        = string
  description = "Default region for resources"
}

variable "artifact_repo" {
  type        = string
  description = "Name of the repo in the Artifact Repository"
}
