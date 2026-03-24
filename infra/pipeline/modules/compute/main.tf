terraform {
  required_version = "v1.14.6"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.8.0"
    }
  }
}

locals {
  img_to_bucket = "${var.region}-docker.pkg.dev/${var.project_name}/${var.artifact_repo_id}/${var.img_to_bucket}"
  img_to_db     = "${var.region}-docker.pkg.dev/${var.project_name}/${var.artifact_repo_id}/${var.img_to_db}"
  img_api       = "${var.region}-docker.pkg.dev/${var.project_name}/${var.artifact_repo_id}/${var.img_api}"
}
