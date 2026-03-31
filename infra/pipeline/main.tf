terraform {
  required_version = "v1.14.6"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.8.0"
    }
  }
}

locals {
  database_name = "moods"
}


# Project

module "project_services" {
  source = "./modules/project_services"

  providers = {
    google = google
  }
}

# Authorization

module "db_user" {
  source = "./modules/authorization/user_creation"

  providers = {
    google = google
  }

  user_ref_name     = "db-username"
  password_ref_name = "db-password"
  username          = null
  password          = null
  depends_on        = [module.project_services]
}

# Storage

module "landing_bucket" {
  source = "./modules/storage"

  providers = {
    google = google
  }

  bucket_name = "yossi-landing-bucket"
  region      = var.region
  depends_on  = [module.project_services]
}

module "raw_bucket" {
  source = "./modules/storage"

  providers = {
    google = google
  }

  bucket_name = "yossi-raw-bucket"
  region      = var.region
  depends_on  = [module.project_services]
}

# Database

# module "database" {
#   source = "./modules/database"

#   providers = {
#     google = google
#   }

#   region        = var.region
#   instance_name = "yossi-db-instance"
#   db_name       = local.database_name
#   db_user       = module.db_user.username
#   db_password   = module.db_user.password
#   depends_on    = [module.project_services, module.db_user]
# }

# # Compute (Jobs)

# module "job_ingest_in_landing" {
#   source = "./modules/compute/jobs"

#   providers = {
#     google = google
#   }

#   region       = var.region
#   job_name     = "ingest-in-landing"
#   image        = "${var.region}-docker.pkg.dev/${var.project_name}/${var.artifact_repo}/<changeme>"
#   cmd_override = ["gcp_pipeline.ingest.ingest_in_landing"]
#   env_secrets  = {}
#   env_variables = {
#     BUCKET_NAME_LANDING = module.landing_bucket.bucket_name
#   }
# }

# module "job_ingest_in_raw" {
#   source = "./modules/compute/jobs"

#   providers = {
#     google = google
#   }

#   region       = var.region
#   job_name     = "ingest-in-raw"
#   image        = "${var.region}-docker.pkg.dev/${var.project_name}/${var.artifact_repo}/<changeme>"
#   cmd_override = ["gcp_pipeline.ingest.ingest_in_raw"]
#   env_secrets = {
#   }
#   env_variables = {
#     BUCKET_NAME_LANDING = module.landing_bucket.bucket_name
#     BUCKET_NAME_RAW     = module.raw_bucket.bucket_name
#   }
# }

# module "job_ingest_in_db" {
#   source = "./modules/compute/jobs"

#   providers = {
#     google = google
#   }

#   region       = var.region
#   job_name     = "ingest-in-db"
#   image        = "${var.region}-docker.pkg.dev/${var.project_name}/${var.artifact_repo}/<changeme>"
#   cmd_override = ["gcp_pipeline.ingest.ingest_in_dbs"]

#   env_secrets = {
#     DB_CONNECTION_NAME = module.database.connection_name
#     DB_USER            = module.db_user.username
#     DB_PASSWORD        = module.db_user.password
#   }

#   env_variables = {
#     BUCKET_NAME_LANDING = module.landing_bucket.bucket_name
#     BUCKET_NAME_RAW     = module.raw_bucket.bucket_name
#     DB_NAME             = local.database_name
#   }
# }


# # Compute (Service)

# module "service_api" {
#   count  = 0
#   source = "./modules/compute/service"

#   providers = {
#     google = google
#   }

#   region       = var.region
#   service_name = "api"
#   image        = "${var.region}-docker.pkg.dev/${var.project_name}/${var.artifact_repo}/<changeme>"
#   cmd_override = []

#   env_secrets = {
#     DB_CONNECTION_NAME = module.database.connection_name
#     DB_USER            = module.db-user.username
#     DB_PASSWORD        = module.db-user.password
#   }

#   env_variables = {
#     BUCKET_NAME_LANDING = module.landing_bucket.bucket_name
#     BUCKET_NAME_RAW     = module.raw_bucket.bucket_name
#     DB_NAME             = local.database_name
#   }
# }
