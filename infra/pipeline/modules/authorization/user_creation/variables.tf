variable "user_ref_name" {
  type        = string
  description = "The reference identifies where this user is stored in Secret Manager"
}

variable "username" {
  type        = string
  description = "Provide a specific username. If no username is set, a random name will be generated"
  default     = null
}

variable "password_ref_name" {
  type        = string
  description = "The reference identifies where this password is stored in Secret Manager"
}

variable "password" {
  type        = string
  description = "Provide a specific password. If no password is set, a random password will be generated"
  default     = null
  sensitive   = true
}
