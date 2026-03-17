terraform {
  required_version = "v1.14.6"

  backend "gcs" {
    bucket = "yossi-infra-ci-project-terraform-state"
    prefix = "bootstrap"
  }
}
