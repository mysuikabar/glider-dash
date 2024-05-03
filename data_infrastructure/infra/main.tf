terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.25.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

module "bigquery" {
  source     = "./modules/bigquery"
  dataset_id = var.dataset_id
}

module "functions" {
  source                 = "./modules/cloud_functions"
  source_bucket_prefix   = var.source_bucket_prefix
  function_bucket_prefix = var.function_bucket_prefix
  function_name          = var.function_name
  dataset_id             = var.dataset_id
  table_id               = var.table_id
}

