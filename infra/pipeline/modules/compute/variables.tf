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

variable "elt_image_name" {
  description = "Name of the image"
  type        = string
}
