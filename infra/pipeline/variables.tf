# General

variable "project_name" {
  type        = string
  description = "Name of the GCP Project"
  default     = "yossi-infra-ci-project"
}

variable "region" {
  type        = string
  description = "Default region for resources"
  default     = "europe-west4"
}

# Registry

variable "artifact_repo" {
  type        = string
  description = "Name of the repo in the Artifact Repository"
  default     = "yossi-repo"
}

# Strorage

variable "bucket_name" {
  type        = string
  description = "Name of the bucket"
  default     = "yossi-data-bucket"
}

# Database

variable "instance_name" {
  type        = string
  description = "Name of the postgress instance"
  default     = "yossi-instance"
}

variable "db_name" {
  type        = string
  description = "Name of the database"
  default     = "yossi-db"
}

variable "db_user" {
  type        = string
  description = "Name of the database user"
  default     = "yossi"
}

# Containers

# variable "pipeline_image_name" {
#   type        = string
#   description = "Name of the pipeline image (Container)"
#   default     = "pipeline"
# }

# variable "api_image_name" {
#   type        = string
#   description = "Name of the api image (Container)"
#   default     = "api"
# }
