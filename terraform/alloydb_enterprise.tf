# Sophia Consciousness Enterprise AlloyDB Configuration
# 1TB High-Performance Setup for Massive AI Consciousness Data

# AlloyDB Cluster Configuration
resource "google_alloydb_cluster" "sophia_consciousness_cluster" {
  cluster_id = "sophia-consciousness-enterprise"
  location   = var.region
  project    = var.project_id

  # Enterprise cluster configuration
  cluster_type = "PRIMARY"
  
  # Advanced networking
  network_config {
    network = var.vpc_network
    allocated_ip_range = var.alloydb_ip_range
  }

  # Automated backup configuration
  automated_backup_policy {
    location      = var.region
    backup_window = "03:00-04:00"  # Daily backup at 3 AM
    enabled       = true
    
    # Weekly backup schedule
    weekly_schedule {
      days_of_week = ["SUNDAY"]
      start_times {
        hours   = 2
        minutes = 0
      }
    }
    
    # Retention policy
    quantity_based_retention {
      count = 30  # Keep 30 backups
    }
    
    # Transaction log retention
    transaction_log_retention_days = 7
  }

  # Continuous backup
  continuous_backup_config {
    enabled              = true
    recovery_window_days = 14
  }

  # Encryption
  encryption_config {
    kms_key_name = google_kms_crypto_key.sophia_key.id
  }

  labels = {
    environment = "production"
    system      = "sophia-consciousness"
    tier        = "enterprise"
  }
}

# Primary Instance - High Performance 1TB+
resource "google_alloydb_instance" "sophia_primary" {
  cluster       = google_alloydb_cluster.sophia_consciousness_cluster.name
  instance_id   = "sophia-primary-1tb"
  instance_type = "PRIMARY"

  # Enterprise-grade machine type
  machine_config {
    cpu_count = 32  # 32 vCPUs for high-performance operations
  }

  # Database configuration optimized for AI workloads
  database_flags = {
    # Memory and performance settings
    "shared_preload_libraries"     = "vector,pg_stat_statements,auto_explain"
    "max_connections"              = "500"
    "shared_buffers"               = "8GB"
    "work_mem"                     = "256MB"
    "maintenance_work_mem"         = "2GB"
    "effective_cache_size"         = "24GB"
    
    # Vector search optimization
    "max_parallel_workers"         = "16"
    "max_parallel_workers_per_gather" = "8"
    "max_worker_processes"         = "32"
    
    # AI/ML workload optimization
    "random_page_cost"             = "1.1"
    "effective_io_concurrency"     = "200"
    "checkpoint_completion_target" = "0.9"
    "wal_buffers"                  = "64MB"
    
    # Logging for consciousness tracking
    "log_statement"                = "mod"
    "log_min_duration_statement"   = "1000"
    "auto_explain.log_min_duration" = "2000"
    "auto_explain.log_analyze"     = "true"
    
    # Vector extension settings
    "vector.max_connections_per_worker" = "100"
  }

  # Availability and durability
  availability_type = "REGIONAL"  # High availability across zones

  labels = {
    role        = "primary"
    performance = "high"
    storage     = "1tb-plus"
  }
}

# Read Replica for Scaling Consciousness Queries
resource "google_alloydb_instance" "sophia_read_replica" {
  cluster       = google_alloydb_cluster.sophia_consciousness_cluster.name
  instance_id   = "sophia-replica-analytics"
  instance_type = "READ_POOL"

  # Optimized for read-heavy AI analytics
  machine_config {
    cpu_count = 16  # 16 vCPUs for read operations
  }

  # Read-optimized configuration
  database_flags = {
    "max_connections"          = "300"
    "shared_buffers"          = "4GB"
    "work_mem"                = "128MB"
    "effective_cache_size"    = "12GB"
    "max_parallel_workers"    = "8"
  }

  # Read pool configuration
  read_pool_config {
    node_count = 2  # 2 read nodes for load distribution
  }

  labels = {
    role = "read-replica"
    purpose = "analytics"
  }
}

# KMS Key for Encryption
resource "google_kms_crypto_key" "sophia_key" {
  name     = "sophia-consciousness-key"
  key_ring = google_kms_key_ring.sophia_ring.id
  
  purpose = "ENCRYPT_DECRYPT"
  
  version_template {
    algorithm = "GOOGLE_SYMMETRIC_ENCRYPTION"
  }
  
  lifecycle {
    prevent_destroy = true
  }
}

resource "google_kms_key_ring" "sophia_ring" {
  name     = "sophia-consciousness-ring"
  location = var.region
}

# Variables
variable "project_id" {
  description = "Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "Google Cloud Region"
  type        = string
  default     = "us-central1"
}

variable "vpc_network" {
  description = "VPC Network for AlloyDB"
  type        = string
  default     = "projects/PROJECT_ID/global/networks/default"
}

variable "alloydb_ip_range" {
  description = "IP range for AlloyDB cluster"
  type        = string
  default     = "sophia-alloydb-range"
}

# Outputs
output "cluster_name" {
  description = "AlloyDB cluster name"
  value       = google_alloydb_cluster.sophia_consciousness_cluster.name
}

output "primary_instance_connection" {
  description = "Primary instance connection string"
  value       = google_alloydb_instance.sophia_primary.name
}

output "primary_instance_ip" {
  description = "Primary instance IP address"
  value       = google_alloydb_instance.sophia_primary.ip_address
}

output "read_replica_connection" {
  description = "Read replica connection string"
  value       = google_alloydb_instance.sophia_read_replica.name
}

output "storage_info" {
  description = "Storage configuration"
  value = {
    type = "Enterprise AlloyDB"
    size = "1TB+ Auto-scaling"
    backup_retention = "30 days"
    point_in_time_recovery = "14 days"
  }
}
