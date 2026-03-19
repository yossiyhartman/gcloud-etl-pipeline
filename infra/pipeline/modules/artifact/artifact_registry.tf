terraform {
  required_version = "v1.14.6"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.8.0"
    }
  }
}

resource "google_artifact_registry_repository" "artifact-repo" {
  project       = var.project_name
  repository_id = var.artifact_repo_id
  description   = ""
  format        = "DOCKER"
  location      = "europe-west4"
}
