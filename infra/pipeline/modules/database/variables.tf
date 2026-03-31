variable "region" {
  description = "The region to store resources"
  type        = string
}

variable "instance_name" {
  description = "name of the CloudSQL instance"
  type        = string
}

variable "db_name" {
  description = "Name of the database"
  type        = string
}

variable "db_user" {
  description = "Name of the database user"
  type        = string
}

variable "db_password" {
  description = "Name of the database password"
  type        = string
}
