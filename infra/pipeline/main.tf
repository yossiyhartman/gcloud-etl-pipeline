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
  source     = "./modules/iam"
  depends_on = [module.project]
}

module "artifact" {
  source           = "./modules/artifact"
  project_name     = var.project_name
  artifact_repo_id = var.artifact_repo_id
  region           = var.region
  depends_on       = [module.project, module.iam]
}

module "storage" {
  source       = "./modules/storage"
  project_name = var.project_name
  bucket_name  = var.bucket_name
  depends_on   = [module.project, module.iam]
}

module "database" {
  source        = "./modules/database"
  project_name  = var.project_name
  region        = var.region
  instance_name = var.instance_name
  db_name       = var.db_name
  db_user       = var.db_user
  db_password   = var.db_password
  depends_on    = [module.project, module.iam]
}

module "compute" {
  source     = "./modules/compute"
  depends_on = [module.project, module.iam]
}
