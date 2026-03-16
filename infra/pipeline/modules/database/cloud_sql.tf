resource "google_sql_database_instance" "instance" {
  project          = var.project_name
  name             = var.instance_name
  region           = "europe-west4"
  database_version = "POSTGRES_17"

  settings {
    tier = "db-f1-micro"
  }

  deletion_protection = false
}
