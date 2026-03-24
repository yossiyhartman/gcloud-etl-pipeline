
resource "google_cloud_run_v2_service" "default" {
  name     = "api-service"
  location = var.region
  deletion_protection = false
  ingress = "INGRESS_TRAFFIC_ALL"

  scaling {
    max_instance_count = 100
  }

  template {
    containers {
      image = service_image_name
    }
  }
}
