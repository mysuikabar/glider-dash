variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "asia-northeast1"
}

variable "bucket_name_igc" {
  type = string
}

variable "bucket_name_function" {
  type = string
}

variable "function_name" {
  type    = string
  default = "igc_file_processor"
}

variable "dataset_id" {
  type    = string
  default = "flight_log"
}

variable "table_id" {
  type    = string
  default = "ds_flight_log"
}
