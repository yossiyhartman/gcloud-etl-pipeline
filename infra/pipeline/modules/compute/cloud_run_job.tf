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
