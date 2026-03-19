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

variable "bucket_name" {
  description = "name of the bucket"
  type        = string
}

variable "instance_name" {
  description = "Name of the instance"
  type        = string
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
