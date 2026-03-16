locals {
  service_account_roles = [
    "roles/storage.admin",
    "roles/run.admin",
    "roles/cloudsql.admin",
    "roles/artifactregistry.admin"
  ]
}

resource "google_project_iam_member" "sa_project_roles" {
  project  = var.project_name
  for_each = toset(local.service_account_roles)
  role     = each.value
  member   = "serviceAccount:${var.service_account_email}"
}
