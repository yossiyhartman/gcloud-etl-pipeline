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

module "authorization" {
  source       = "./modules/authorization"
  project_name = var.project_name
}

module "artifact" {
  source        = "./modules/artifact"
  project_name  = var.project_name
  region        = var.region
  artifact_repo = var.artifact_repo
  depends_on    = [module.project]
}

module "storage" {
  source       = "./modules/storage"
  project_name = var.project_name
  bucket_name  = var.bucket_name
  region       = var.region
  depends_on   = [module.project]
}

module "database" {
  source        = "./modules/database"
  project_name  = var.project_name
  region        = var.region
  instance_name = var.instance_name
  db_name       = var.db_name
  db_user       = var.db_user
  db_password   = module.authorization.password_val
  depends_on    = [module.project, module.authorization]
}

module "compute" {
  source              = "./modules/compute"
  project_name        = var.project_name
  region              = var.region
  artifact_repo       = var.artifact_repo
  bucket_name         = var.bucket_name
  db_name             = var.db_name
  db_user             = var.db_user
  db_password         = module.authorization.password_ref
  instance_name       = module.database.instance_name
  pipeline_image_name = var.pipeline_image_name
  api_image_name      = var.api_image_name
  depends_on          = [module.database]
}
