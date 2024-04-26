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

# source bucket
resource "google_storage_bucket" "source_bucket" {
  name          = var.bucket_name_igc
  location      = var.region
  force_destroy = true
}

# cloud functions
data "archive_file" "function_archive" {
  type        = "zip"
  source_dir  = "./function"
  output_path = "./function.zip"
}

resource "google_storage_bucket" "function_bucket" {
  name          = var.bucket_name_function
  location      = var.region
  force_destroy = true
}

resource "google_storage_bucket_object" "function_source" {
  name   = "function.zip"
  bucket = google_storage_bucket.function_bucket.name
  source = data.archive_file.function_archive.output_path
}

resource "google_cloudfunctions_function" "function" {
  name                  = var.function_name
  runtime               = "python312"
  available_memory_mb   = 256
  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.function_source.name
  entry_point           = "main"
  event_trigger {
    event_type = "google.storage.object.finalize"
    resource   = google_storage_bucket.source_bucket.id
  }
  environment_variables = {
    DATASET_ID = var.dataset_id
    TABLE_ID   = var.table_id
  }
}

# target dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id                 = var.dataset_id
  location                   = var.region
  delete_contents_on_destroy = true
}
