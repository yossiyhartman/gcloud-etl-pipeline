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

# variable "artifact_repo" {
#   type        = string
#   description = "Name of the repo in the Artifact Repository"
#   default     = "yossi-repo"
# }
