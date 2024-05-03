variable "location" {
  type    = string
  default = "asia-northeast1"
}

variable "source_bucket_prefix" {
  type = string
}

variable "function_bucket_prefix" {
  type = string
}

variable "function_name" {
  type = string
}

variable "dataset_id" {
  type = string
}

variable "table_id" {
  type = string
}
