variable "project_name" {
  description = "Name of the GCP Project"
  type        = string
}

variable "region" {
  description = "The region to store resources"
  type        = string
}

variable "artifact_repo_id" {
  description = "the name of the repo in the Artifact Repository"
  type        = string
}

variable "img_to_bucket" {
  type = string
}

variable "img_to_db" {
  type = string
}

variable "img_api" {
  type = string
}
