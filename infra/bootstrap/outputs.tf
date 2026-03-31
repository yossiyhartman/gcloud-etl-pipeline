output "sa_email" {
  description = "Email of the service account"
  value       = google_service_account.terraform_sa.email
}

output "artifact_registry_name" {
  description = "Name of the Artifact Registry Repo"
  value       = google_artifact_registry_repository.artifact_repo.id
}
