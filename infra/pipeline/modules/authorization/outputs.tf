output "password_ref" {
  value     = google_secret_manager_secret.db_password.id
  sensitive = true
}

output "password_val" {
  value     = google_secret_manager_secret_version.db_password_version.secret_data
  sensitive = true
}
