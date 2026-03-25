output "repo_id" {
  description = "artifact registry id"
  value       = google_artifact_registry_repository.artifact_repo.id
}
