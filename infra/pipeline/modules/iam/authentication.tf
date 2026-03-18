# NAME

resource "google_secret_manager_secret" "db-name-secret-name" {
  secret_id = "db-name-secret"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "db-name-secret-value" {
  secret      = google_secret_manager_secret.db-name-secret-name.secret_id
  secret_data = var.db_name
}


# USER

resource "google_secret_manager_secret" "db-user-secret-name" {
  secret_id = "db-user-secret"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "db-user-secret-value" {
  secret      = google_secret_manager_secret.db-user-secret-name.secret_id
  secret_data = var.db_user
}

# PASSWORD

resource "google_secret_manager_secret" "db-password-secret-name" {
  secret_id = "db-password-secret"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "db-password-secret-value" {
  secret      = google_secret_manager_secret.db-password-secret-name.secret_id
  secret_data = var.db_password
}
