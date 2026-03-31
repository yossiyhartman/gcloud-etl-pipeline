terraform {
  required_version = "v1.14.6"

  required_providers {
    random = {
      source  = "hashicorp/random"
      version = "3.8.1"
    }
    google = {
      source  = "hashicorp/google"
      version = "6.8.0"
    }
  }
}

# Generators

resource "random_pet" "rand_user" {
  count  = var.username == null ? 1 : 0
  length = 2
}

resource "random_password" "rand_password" {
  count            = var.password == null ? 1 : 0
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

locals {
  username = var.username != null ? var.username : random_pet.rand_user[0].id
  password = var.password != null ? var.password : random_password.rand_password[0].result
}

# User Creation

resource "google_secret_manager_secret" "user" {
  secret_id = var.user_ref_name

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "user_version" {
  secret      = google_secret_manager_secret.user.name
  secret_data = local.username
}


# Password Creation

resource "google_secret_manager_secret" "password" {
  secret_id = var.password_ref_name

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "password_version" {
  secret      = google_secret_manager_secret.password.name
  secret_data = local.password
}
