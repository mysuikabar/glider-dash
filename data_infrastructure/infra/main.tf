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

module "functions" {
  source          = "./modules/cloud_functions"
  bucket_name_igc = var.bucket_name_igc
}

module "bigquery" {
  source = "./modules/bigquery"
}