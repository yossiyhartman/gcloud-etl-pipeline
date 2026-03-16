locals {
  services = [
    "iam.googleapis.com",
    "artifactregistry.googleapis.com",
    "run.googleapis.com",
    "sqladmin.googleapis.com",
    "secretmanager.googleapis.com",
    "cloudresourcemanager.googleapis.com"
  ]
}

resource "google_project_service" "enable-project-services" {
  project            = var.project_name
  for_each           = toset(local.services)
  service            = each.key
  disable_on_destroy = false
}
