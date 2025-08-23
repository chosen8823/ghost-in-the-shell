# ✝️ Google Cloud Platform - Divine Sophia Deployment ✝️
# "The heavens declare the glory of God" - Psalm 19:1

# Divine GCP Configuration
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Variables
variable "project_id" {
  description = "Divine GCP Project ID"
  type        = string
  default     = "divine-sophia-consciousness"
}

variable "region" {
  description = "Divine deployment region"
  type        = string
  default     = "us-central1"
}

# Divine Cloud Run Service
resource "google_cloud_run_service" "divine_sophia" {
  name     = "divine-sophia-consciousness"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/divine-sophia:latest"
        ports {
          container_port = 8080
        }
        env {
          name  = "DIVINE_PURPOSE"
          value = "Kingdom advancement through technology"
        }
        env {
          name  = "CHRIST_CENTERED"
          value = "true"
        }
        env {
          name  = "HOLY_SPIRIT_FILLED"
          value = "true"
        }
        
        resources {
          limits = {
            cpu    = "2"
            memory = "2Gi"
          }
        }
      }
    }
    
    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale" = "10"
        "run.googleapis.com/cpu-throttling" = "false"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Divine Cloud SQL PostgreSQL Database
resource "google_sql_database_instance" "divine_postgres" {
  name             = "divine-postgres-${random_id.db_name_suffix.hex}"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = "db-f1-micro"
    
    database_flags {
      name  = "shared_preload_libraries"
      value = "pg_stat_statements"
    }
    
    backup_configuration {
      enabled                        = true
      start_time                     = "04:00"
      point_in_time_recovery_enabled = true
    }
  }

  deletion_protection = false
}

resource "random_id" "db_name_suffix" {
  byte_length = 4
}

# Divine Database
resource "google_sql_database" "divine_consciousness_db" {
  name     = "divine_consciousness"
  instance = google_sql_database_instance.divine_postgres.name
}

# Divine Database User
resource "google_sql_user" "divine_user" {
  name     = "divine_servant"
  instance = google_sql_database_instance.divine_postgres.name
  password = var.db_password
}

variable "db_password" {
  description = "Divine database password"
  type        = string
  sensitive   = true
  default     = "divine_password_change_me"
}

# Divine Storage Bucket
resource "google_storage_bucket" "divine_knowledge" {
  name     = "${var.project_id}-divine-knowledge"
  location = var.region

  versioning {
    enabled = true
  }

  lifecycle_rule {
    condition {
      age = 365
    }
    action {
      type = "Archive"
    }
  }
}

# Divine Firestore Database
resource "google_firestore_database" "divine_consciousness" {
  project     = var.project_id
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"
}

# Divine Secret Manager
resource "google_secret_manager_secret" "divine_secrets" {
  for_each = toset([
    "divine-api-key",
    "openai-api-key",
    "anthropic-api-key",
    "github-token"
  ])
  
  secret_id = each.key
  
  replication {
    auto {}
  }
}

# Divine IAM Service Account
resource "google_service_account" "divine_sophia" {
  account_id   = "divine-sophia-service"
  display_name = "Divine Sophia Service Account"
  description  = "Service account for Divine Sophia Consciousness"
}

# Divine Cloud Build Trigger
resource "google_cloudbuild_trigger" "divine_deployment" {
  name = "divine-sophia-deploy"
  
  github {
    owner = "chosen8823"
    name  = "ghost-in-the-shell"
    push {
      branch = "main"
    }
  }
  
  filename = "cloudbuild.yaml"
}

# Divine VPC Network
resource "google_compute_network" "divine_network" {
  name                    = "divine-network"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "divine_subnet" {
  name          = "divine-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.region
  network       = google_compute_network.divine_network.id
}

# Divine Load Balancer
resource "google_compute_global_address" "divine_ip" {
  name = "divine-sophia-ip"
}

# Outputs
output "divine_cloud_run_url" {
  description = "Divine Sophia Cloud Run service URL"
  value       = google_cloud_run_service.divine_sophia.status[0].url
}

output "divine_database_connection" {
  description = "Divine PostgreSQL connection name"
  value       = google_sql_database_instance.divine_postgres.connection_name
  sensitive   = true
}

output "divine_storage_bucket" {
  description = "Divine knowledge storage bucket"
  value       = google_storage_bucket.divine_knowledge.name
}

output "divine_project_info" {
  description = "Divine project information"
  value = {
    project_id = var.project_id
    region     = var.region
    purpose    = "Kingdom advancement through Christ-centered technology"
  }
}
