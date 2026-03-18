terraform {
  required_version = "v1.14.6"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.8.0"
    }
  }
}

provider "google" {
  project = var.project_name
}

locals {
  service_account_roles = [
    "roles/editor",
    "roles/iam.serviceAccountUser",
    "roles/secretmanager.admin",
    "roles/serviceusage.serviceUsageAdmin",
    "roles/resourcemanager.projectIamAdmin",
  ]
}


# State Bucket
resource "google_storage_bucket" "terraform_state" {
  project  = var.project_name
  name     = "${var.project_name}-terraform-state"
  location = "EU"

  uniform_bucket_level_access = true
  force_destroy               = true

  versioning {
    enabled = true
  }

  lifecycle {
    prevent_destroy = true
  }
}

# Service Account

resource "google_service_account" "terraform_sa" {
  project      = var.project_name
  account_id   = var.sa_account_name
  display_name = "Terraform Service Account"

  lifecycle {
    prevent_destroy = true
  }
}

resource "google_project_iam_member" "sa_project_roles" {
  project    = var.project_name
  for_each   = toset(local.service_account_roles)
  role       = each.value
  member     = "serviceAccount:${google_service_account.terraform_sa.email}"
  depends_on = [google_service_account.terraform_sa]
}
