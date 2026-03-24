
resource "google_cloud_run_v2_service" "api_service" {
  name                = "api-service"
  location            = var.region
  deletion_protection = false
  ingress             = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = local.service_image_name
    }
  }
}
