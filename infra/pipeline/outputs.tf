output "repo_id" {
  description = "artifact registry id"
  value       = module.artifact.repo_id
}

output "password_ref" {
  value     = module.authorization.password_ref
  sensitive = true
}

output "password_val" {
  value     = module.authorization.password_val
  sensitive = true
}

output "instance_name" {
  value = module.database.instance_name
}

output "bucket_name" {
  value = module.storage.bucket_name
}
