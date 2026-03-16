terraform {
  backend "gcs" {
    bucket = "yossi-infra-ci-project-terraform-state"
    prefix = "pipeline"
  }
}
