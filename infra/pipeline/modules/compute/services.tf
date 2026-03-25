
resource "google_cloud_run_v2_service" "api_service" {
  project             = var.project_name
  location            = var.region
  name                = "api"
  deletion_protection = false
  ingress             = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = "terraform@yossi-infra-ci-project.iam.gserviceaccount.com"
    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_name}/${var.artifact_repo}/${var.api_image_name}"

      env {
        name  = "INSTANCE_NAME"
        value = var.instance_name
      }
      env {
        name  = "DB_NAME"
        value = var.db_name
      }
      env {
        name  = "DB_USER"
        value = var.db_user
      }
      env {
        name = "DB_PASS"
        value_source {
          secret_key_ref {
            secret  = var.db_password
            version = "latest"
          }
        }
      }
    }
  }
}
