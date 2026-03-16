resource "google_storage_bucket" "data_bucket" {
  project  = var.project_name
  name     = var.bucket_name
  location = "EU"

  uniform_bucket_level_access = true
}
