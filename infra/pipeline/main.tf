terraform {
  required_version = "v1.14.6"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.8.0"
    }
  }
}

provider "google" {
  project = var.project_name
}

module "project" {
  source       = "./modules/project"
  project_name = var.project_name
}

module "iam" {
  source                = "./modules/iam"
  project_name          = var.project_name
  service_account_email = var.service_acount_email
  db_name               = var.db_name
  db_user               = var.db_user
  db_password           = var.db_password
  depends_on            = [module.project]
}

module "artifact" {
  source           = "./modules/artifact"
  project_name     = var.project_name
  artifact_repo_id = var.artifact_repo_id
  depends_on       = [module.project, module.iam]
}

module "storage" {
  source       = "./modules/storage"
  project_name = var.project_name
  bucket_name  = "yossi-data-bucket"
  depends_on   = [module.project, module.iam]
}

module "database" {
  source                = "./modules/database"
  project_name          = var.project_name
  service_account_email = var.service_acount_email
  instance_name         = var.instance_name
  db_name               = var.db_name
  db_user               = var.db_user
  db_password           = var.db_password
  depends_on            = [module.project, module.iam]
}
