variable "project_id" {
  description = "The Project ID."
  type        = string
}

variable "region" {
  description = "The region to host the bucket in."
  type        = string
  default     = "asia-northeast1"
}

variable "bucket_name" {
  description = "Unique name for the bucket."
  type        = string
}

