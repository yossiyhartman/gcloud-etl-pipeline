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
  image_name         = "${var.region}-docker.pkg.dev/${var.project_name}/${var.artifact_repo_id}/${var.elt_image_name}"
  service_image_name = "${var.region}-docker.pkg.dev/${var.project_name}/${var.artifact_repo_id}/${var.api_image_name}"
}
