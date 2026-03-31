terraform {
  required_version = "v1.14.6"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.8.0"
    }
  }
}

data "google_compute_default_service_account" "default_sa" {
}

locals {
  service_account = var.service_account != null ? var.service_account : data.google_compute_default_service_account.default_sa.email
}

resource "google_cloud_run_v2_service" "api_service" {
  location            = var.region
  name                = var.service_name
  deletion_protection = false
  ingress             = "INGRESS_TRAFFIC_ALL"


  template {
    service_account = local.service_account

    containers {
      image = var.image
      args  = var.cmd_override

      dynamic "env" {
        for_each = var.env_variables

        content {
          name  = env.key
          value = env.value
        }
      }

      dynamic "env" {
        for_each = var.env_secrets

        content {
          name = env.key

          value_source {
            secret_key_ref {
              secret  = env.value
              version = "latest"
            }
          }
        }
      }
    }
  }
}

# resource "google_cloud_run_v2_job" "gcp-ingest-in-database" {
#   project             = var.project_name
#   name                = "ingest-in-db"
#   location            = var.region
#   deletion_protection = false


#   template {
#     template {
#       service_account = "terraform@yossi-infra-ci-project.iam.gserviceaccount.com"
#       containers {
#         image = "${var.region}-docker.pkg.dev/${var.project_name}/${var.artifact_repo}/${var.pipeline_image_name}"

#         args = ["gcp_pipeline.ingest.upload_to_database"]

#         env {
#           name  = "BUCKET_NAME"
#           value = var.bucket_name
#         }
#         env {
#           name  = "INSTANCE_NAME"
#           value = var.instance_name
#         }
#         env {
#           name  = "DB_NAME"
#           value = var.db_name
#         }
#         env {
#           name  = "DB_USER"
#           value = var.db_user
#         }
#         env {
#           name = "DB_PASS"
#           value_source {
#             secret_key_ref {
#               secret  = var.db_password
#               version = "latest"
#             }
#           }
#         }
#       }
#     }
#   }
# }
