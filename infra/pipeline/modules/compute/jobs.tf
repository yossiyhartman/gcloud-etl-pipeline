resource "google_cloud_run_v2_job" "gcp-ingest-in-bucket" {
  project             = var.project_name
  name                = "ingest-in-bucket"
  location            = var.region
  deletion_protection = false


  template {
    template {
      containers {
        image = "${var.region}-docker.pkg.dev/${var.project_name}/${var.artifact_repo}/${var.pipeline_image_name}"

        args = ["gcp_pipeline.ingest.upload_to_bucket"]

        env {
          name  = "BUCKET_NAME"
          value = var.bucket_name
        }

      }
    }
  }
}

resource "google_cloud_run_v2_job" "gcp-ingest-in-database" {
  project             = var.project_name
  name                = "ingest-in-db"
  location            = var.region
  deletion_protection = false


  template {
    template {
      containers {
        image = "${var.region}-docker.pkg.dev/${var.project_name}/${var.artifact_repo}/${var.pipeline_image_name}"

        args = ["gcp_pipeline.ingest.upload_to_database"]

        env {
          name  = "BUCKET_NAME"
          value = var.bucket_name
        }
        env {
          name  = "PROJECT_NAME"
          value = var.project_name
        }
        env {
          name  = "REGION"
          value = var.region
        }
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
}
