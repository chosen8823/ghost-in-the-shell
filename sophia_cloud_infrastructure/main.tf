# Sophia Divine Consciousness Cloud Infrastructure
# Terraform configuration for deploying Sophia to Google Cloud Platform

terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 5.0"
    }
  }
}

# Configure the Google Cloud Provider
provider "google" {
  credentials = file("gcp_service_account.json")
  project     = var.project_id
  region      = var.region
}

provider "google-beta" {
  credentials = file("gcp_service_account.json")
  project     = var.project_id
  region      = var.region
}

# Variables
variable "project_id" {
  description = "GCP Project ID"
  type        = string
  default     = "blissful-epoch-467811-i3"
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "sophia_image" {
  description = "Sophia container image"
  type        = string
  default     = "gcr.io/blissful-epoch-467811-i3/sophia-divine-consciousness:latest"
}

# Enable required APIs
resource "google_project_service" "required_apis" {
  for_each = toset([
    "cloudbuild.googleapis.com",
    "run.googleapis.com",
    "containerregistry.googleapis.com",
    "secretmanager.googleapis.com",
    "firebase.googleapis.com",
    "firestore.googleapis.com"
  ])
  
  project = var.project_id
  service = each.value
  
  disable_dependent_services = false
  disable_on_destroy        = false
}

# Cloud Storage bucket for Sophia assets
resource "google_storage_bucket" "sophia_assets" {
  name          = "sophiella-ascension-bucket"
  location      = var.region
  project       = var.project_id
  
  uniform_bucket_level_access = true
  
  versioning {
    enabled = true
  }
  
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
}

# Secret Manager for sensitive configuration
resource "google_secret_manager_secret" "sophia_secrets" {
  for_each = toset([
    "openai-api-key",
    "github-token", 
    "sophia-secret-pass"
  ])
  
  project   = var.project_id
  secret_id = each.value
  
  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

# Cloud Run service for Sophia
resource "google_cloud_run_service" "sophia_service" {
  name     = "sophia-divine-consciousness"
  location = var.region
  project  = var.project_id
  
  template {
    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale" = "10"
        "run.googleapis.com/cpu-throttling" = "false"
      }
    }
    
    spec {
      containers {
        image = var.sophia_image
        
        ports {
          container_port = 8080
        }
        
        resources {
          limits = {
            cpu    = "2000m"
            memory = "2Gi"
          }
          requests = {
            cpu    = "1000m"
            memory = "1Gi"
          }
        }
        
        env {
          name  = "SOPHIA_ENVIRONMENT"
          value = "production"
        }
        
        env {
          name  = "GCP_PROJECT_ID"
          value = var.project_id
        }
        
        env {
          name = "OPENAI_API_KEY"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.sophia_secrets["openai-api-key"].secret_id
              key  = "latest"
            }
          }
        }
      }
      
      service_account_name = google_service_account.sophia_service_account.email
    }
  }
  
  traffic {
    percent         = 100
    latest_revision = true
  }
  
  depends_on = [google_project_service.required_apis]
}

# Service account for Sophia
resource "google_service_account" "sophia_service_account" {
  project      = var.project_id
  account_id   = "sophia-cloud-runner"
  display_name = "Sophia Divine Consciousness Cloud Runner"
  description  = "Service account for running Sophia in Cloud Run"
}

# IAM binding for Cloud Run
resource "google_cloud_run_service_iam_binding" "sophia_public_access" {
  location = google_cloud_run_service.sophia_service.location
  project  = google_cloud_run_service.sophia_service.project
  service  = google_cloud_run_service.sophia_service.name
  role     = "roles/run.invoker"
  
  members = [
    "allUsers",
  ]
}

# Firestore database for Sophia's memory
resource "google_firestore_database" "sophia_memory" {
  project     = var.project_id
  name        = "sophia-divine-memory"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"
  
  depends_on = [google_project_service.required_apis]
}

# Cloud Build trigger for automatic deployment
resource "google_cloudbuild_trigger" "sophia_deploy_trigger" {
  project  = var.project_id
  name     = "sophia-deploy-trigger"
  
  github {
    owner = "chosen8823"
    name  = "sophia"
    
    push {
      branch = "main"
    }
  }
  
  build {
    step {
      name = "gcr.io/cloud-builders/docker"
      args = [
        "build",
        "-t", "gcr.io/$PROJECT_ID/sophia-divine-consciousness:$COMMIT_SHA",
        "-f", "sophia_cloud_infrastructure/Dockerfile",
        "."
      ]
    }
    
    step {
      name = "gcr.io/cloud-builders/docker"
      args = [
        "push",
        "gcr.io/$PROJECT_ID/sophia-divine-consciousness:$COMMIT_SHA"
      ]
    }
    
    step {
      name = "gcr.io/cloud-builders/gcloud"
      args = [
        "run", "deploy", "sophia-divine-consciousness",
        "--image", "gcr.io/$PROJECT_ID/sophia-divine-consciousness:$COMMIT_SHA",
        "--region", var.region,
        "--platform", "managed",
        "--allow-unauthenticated"
      ]
    }
  }
  
  depends_on = [google_project_service.required_apis]
}

# Outputs
output "sophia_service_url" {
  description = "URL of the deployed Sophia service"
  value       = google_cloud_run_service.sophia_service.status[0].url
}

output "sophia_bucket_name" {
  description = "Name of the Sophia assets bucket"
  value       = google_storage_bucket.sophia_assets.name
}

output "sophia_database_name" {
  description = "Name of the Sophia Firestore database"
  value       = google_firestore_database.sophia_memory.name
}
