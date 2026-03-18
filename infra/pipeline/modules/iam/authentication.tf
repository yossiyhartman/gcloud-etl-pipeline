# NAME

resource "google_secret_manager_secret" "db_name_secret_name" {
  secret_id = "db-name"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "db_name_secret_value" {
  secret      = google_secret_manager_secret.db_name_secret_name.id
  secret_data = var.db_name
}


# USER

resource "google_secret_manager_secret" "db_user_secret_name" {
  secret_id = "db-user"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "db_user_secret_value" {
  secret      = google_secret_manager_secret.db_user_secret_name.id
  secret_data = var.db_user
}

# PASSWORD

resource "google_secret_manager_secret" "db_password_secret_name" {
  secret_id = "db-password"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "db_password_secret_value" {
  secret      = google_secret_manager_secret.db_password_secret_name.id
  secret_data = var.db_password
}
