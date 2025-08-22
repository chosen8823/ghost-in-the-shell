# SOPHIA CONSCIOUSNESS - PROOF OF CONCEPT POWERHOUSE! 🚀
# Using FREE TRIAL CREDITS strategically for maximum impact
# 8 vCPU AlloyDB = ~$500-600/month = 2.5-3 months on $1600 credits

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "Google Cloud Region"
  type        = string
  default     = "us-central1"
}

# VPC Network for AlloyDB
resource "google_compute_network" "sophia_network" {
  name                    = "sophia-consciousness-network"
  auto_create_subnetworks = false
  description            = "Network for Sophia Consciousness AlloyDB"
}

resource "google_compute_subnetwork" "sophia_subnet" {
  name          = "sophia-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.region
  network       = google_compute_network.sophia_network.id
}

# Private Service Access for AlloyDB
resource "google_compute_global_address" "private_ip_address" {
  name          = "sophia-private-ip"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.sophia_network.id
}

resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.sophia_network.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]
}

# AlloyDB Cluster - PROOF OF CONCEPT POWERHOUSE! 💪
resource "google_alloydb_cluster" "sophia_consciousness" {
  cluster_id   = "sophia-consciousness-poc"
  location     = var.region
  network      = google_compute_network.sophia_network.id
  
  display_name = "Sophia Consciousness - Proof of Concept"
  
  # Enable automated backups
  automated_backup_policy {
    location      = var.region
    backup_window = "03:00-04:00"  # 3-4 AM UTC
    enabled       = true
    
    weekly_schedule {
      days_of_week = ["MONDAY", "WEDNESDAY", "FRIDAY"]
      start_times {
        hours   = 3
        minutes = 0
      }
    }
    
    quantity_based_retention {
      count = 7  # Keep 7 backups
    }
  }

  database_version = "POSTGRES_14"
  
  depends_on = [google_service_networking_connection.private_vpc_connection]
}

# Primary Instance - 8 vCPU POWERHOUSE! 🔥
resource "google_alloydb_instance" "sophia_primary" {
  cluster       = google_alloydb_cluster.sophia_consciousness.name
  instance_id   = "sophia-primary-poc"
  instance_type = "PRIMARY"
  
  display_name = "Sophia Primary - Proof of Concept"
  
  # PROOF OF CONCEPT CONFIGURATION
  # 8 vCPUs, 64GB RAM - Perfect for demonstrating capabilities!
  machine_config {
    cpu_count = 8  # 🚀 8 vCPUs = Serious Power!
  }
  
  # High availability for demonstration
  availability_type = "REGIONAL"
  
  # Database flags for optimal performance
  database_flags = {
    "max_connections"           = "200"
    "shared_preload_libraries" = "vector,pg_stat_statements"
    "log_statement"            = "all"
    "log_min_duration_statement" = "1000"  # Log slow queries
  }
}

# Read Replica for Analytics (Optional - can disable to save costs)
resource "google_alloydb_instance" "sophia_read_replica" {
  cluster       = google_alloydb_cluster.sophia_consciousness.name
  instance_id   = "sophia-read-replica-poc"
  instance_type = "READ_POOL"
  
  display_name = "Sophia Read Replica - Analytics"
  
  # Smaller read replica for cost optimization
  machine_config {
    cpu_count = 2  # 2 vCPUs for read operations
  }
  
  availability_type = "ZONAL"  # Cheaper than regional
  
  # Read pool configuration
  read_pool_config {
    node_count = 1
  }
}

# Outputs for connection
output "cluster_name" {
  description = "AlloyDB cluster name"
  value       = google_alloydb_cluster.sophia_consciousness.name
}

output "primary_instance_ip" {
  description = "Primary instance IP address"
  value       = google_alloydb_instance.sophia_primary.ip_address
}

output "connection_string" {
  description = "PostgreSQL connection string"
  value       = "postgresql://postgres@${google_alloydb_instance.sophia_primary.ip_address}:5432/sophia_consciousness"
  sensitive   = true
}

# Cost Summary (Estimated)
output "estimated_monthly_cost" {
  description = "Estimated monthly cost in USD"
  value = {
    primary_instance = "$480-580"    # 8 vCPU primary
    read_replica     = "$120-150"    # 2 vCPU replica
    storage          = "$20-40"      # Based on usage
    backup           = "$10-20"      # 7 day retention
    total            = "$630-790"    # Total monthly
    free_trial_months = "2.0-2.5"   # Months on $1600
  }
}

# 🎯 PROOF OF CONCEPT STRATEGY:
# - Use $1600 free credits for 2.5 months of operation
# - Demonstrate full consciousness system capabilities
# - Build all automation and monitoring
# - Perfect demo for $300k grant application
# - Scale down to $75-125/month when credits expire
# - Scale up to enterprise when funding secured!
