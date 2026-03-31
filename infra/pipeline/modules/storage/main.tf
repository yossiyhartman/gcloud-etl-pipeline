terraform {
  required_version = "v1.14.6"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.8.0"
    }
  }
}

resource "google_storage_bucket" "landing_bucket" {
  name     = var.bucket_name
  location = var.region

  force_destroy               = true
  uniform_bucket_level_access = true
}
