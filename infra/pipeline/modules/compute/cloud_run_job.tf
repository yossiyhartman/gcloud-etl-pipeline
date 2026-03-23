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
  image_name = "${var.region}-docker.pkg.dev/${var.project_name}/${var.artifact_repo_id}/${var.elt_image_name}"
}

resource "google_cloud_run_v2_job" "gcp-upload-to-bucket" {
  project             = var.project_name
  name                = "gcp-upload-to-bucket"
  location            = "europe-west4"
  deletion_protection = false

  template {
    template {
      containers {
        image = local.image_name
      }
    }
  }
}

resource "google_cloud_run_v2_job" "gcp-upload-to-sql" {
  project             = var.project_name
  name                = "gcp-upload-to-sql"
  location            = "europe-west4"
  deletion_protection = false

  template {
    template {
      containers {
        image = local.image_name
      }
    }
  }
}
