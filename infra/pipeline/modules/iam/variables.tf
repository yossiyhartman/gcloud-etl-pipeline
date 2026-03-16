variable "project_name" {
  description = "Name of the GCP Project"
  type        = string
}

variable "service_account_email" {
  description = "the email of the service account"
  type        = string
}

variable "db_name" {
  description = "Name of the database"
  type        = string
  sensitive   = false
}

variable "db_user" {
  description = "Name of the database user"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Name of the database password"
  type        = string
  sensitive   = true
}
