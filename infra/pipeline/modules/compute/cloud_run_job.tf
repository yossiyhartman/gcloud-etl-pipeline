resource "google_cloud_run_v2_job" "upload_to_bucket" {
  project             = var.project_name
  name                = "gcp-upload"
  location            = "europe-west4"
  deletion_protection = false

  template {
    template {
      service_account = var.service_acount_email
    }
  }
}
