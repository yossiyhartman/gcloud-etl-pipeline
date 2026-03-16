output "sa_email" {
  description = "Email of the service account"
  value       = google_service_account.terraform_sa.email
}
