resource "google_cloud_run_v2_job" "gcp-upload-to-bucket" {
  project             = var.project_name
  name                = var.img_to_bucket
  location            = "europe-west4"
  deletion_protection = false



  template {
    template {
      containers {
        image = local.img_to_bucket
      }
    }
  }
}

resource "google_cloud_run_v2_job" "gcp-upload-to-sql" {
  project             = var.project_name
  name                = var.img_to_db
  location            = "europe-west4"
  deletion_protection = false

  template {
    template {
      containers {
        image = local.img_to_db
      }
    }
  }
}
