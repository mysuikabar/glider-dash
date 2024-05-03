terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.25.0"
    }
  }
}

provider "google" {
  project     = var.project_id
  region      = var.region
}

resource "google_storage_bucket" "data_bucket" {
  name     = var.bucket_name
  location = var.region
}