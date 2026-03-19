terraform {
  required_version = "v1.14.6"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.8.0"
    }
  }
}

resource "google_storage_bucket" "data_bucket" {
  project  = var.project_name
  name     = var.bucket_name
  location = "EU"

  uniform_bucket_level_access = true
}
