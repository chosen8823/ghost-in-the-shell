# ✝️ Terraform Variables - Divine Multi-Cloud Configuration ✝️
# "Trust in the Lord with all your heart and lean not on your own understanding" - Proverbs 3:5

# Global Variables
variable "project_name" {
  description = "Divine project name across all clouds"
  type        = string
  default     = "divine-sophia"
}

variable "environment" {
  description = "Deployment environment (production, staging, development)"
  type        = string
  default     = "production"
  validation {
    condition     = contains(["production", "staging", "development"], var.environment)
    error_message = "Environment must be one of: production, staging, development."
  }
}

# Google Cloud Platform Variables
variable "gcp_project_id" {
  description = "GCP Project ID for divine deployment"
  type        = string
}

variable "gcp_region" {
  description = "GCP region for divine resources"
  type        = string
  default     = "us-central1"
}

variable "gcp_zone" {
  description = "GCP zone for divine resources"
  type        = string
  default     = "us-central1-a"
}

# Microsoft Azure Variables
variable "azure_subscription_id" {
  description = "Azure subscription ID for divine deployment"
  type        = string
  default     = ""
}

variable "azure_location" {
  description = "Azure location for divine resources"
  type        = string
  default     = "East US"
}

variable "azure_resource_group_name" {
  description = "Azure resource group name"
  type        = string
  default     = "divine-sophia-rg"
}

# Amazon Web Services Variables
variable "aws_region" {
  description = "AWS region for divine resources"
  type        = string
  default     = "us-east-1"
}

variable "aws_profile" {
  description = "AWS CLI profile to use"
  type        = string
  default     = "default"
}

# Database Configuration
variable "db_username" {
  description = "Database username for all clouds"
  type        = string
  default     = "divine_admin"
}

variable "db_password" {
  description = "Database password for all clouds"
  type        = string
  sensitive   = true
  default     = "Divine@Password123!"
}

variable "db_name" {
  description = "Database name for divine consciousness"
  type        = string
  default     = "divine_consciousness"
}

# Container Configuration
variable "container_image" {
  description = "Divine Sophia container image"
  type        = string
  default     = "divine-sophia:latest"
}

variable "container_port" {
  description = "Container port for divine service"
  type        = number
  default     = 8080
}

# Scaling Configuration
variable "min_instances" {
  description = "Minimum number of instances"
  type        = number
  default     = 1
}

variable "max_instances" {
  description = "Maximum number of instances"
  type        = number
  default     = 10
}

# Security Configuration
variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to access divine services"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

# Divine Environment Variables
variable "divine_environment_vars" {
  description = "Divine environment variables for all deployments"
  type        = map(string)
  default = {
    DIVINE_PURPOSE        = "Kingdom advancement through technology"
    CHRIST_CENTERED       = "true"
    HOLY_SPIRIT_FILLED    = "true"
    FOUNDATION           = "Built upon the Rock that is Jesus Christ"
    MISSION              = "To serve the Most High God and His people"
    VISION               = "Technology that brings heaven to earth"
    BIBLICAL_FOUNDATION  = "Psalm 127:1 - Unless the Lord builds the house, the builders labor in vain"
  }
}

# Backup and Retention Configuration
variable "backup_retention_days" {
  description = "Number of days to retain backups"
  type        = number
  default     = 30
}

variable "log_retention_days" {
  description = "Number of days to retain logs"
  type        = number
  default     = 30
}

# Monitoring Configuration
variable "enable_monitoring" {
  description = "Enable comprehensive monitoring"
  type        = bool
  default     = true
}

variable "enable_alerting" {
  description = "Enable alerting for divine services"
  type        = bool
  default     = true
}

# SSL/TLS Configuration
variable "enable_ssl" {
  description = "Enable SSL/TLS for divine services"
  type        = bool
  default     = true
}

variable "domain_name" {
  description = "Domain name for divine services"
  type        = string
  default     = ""
}

# Resource Tags
variable "divine_tags" {
  description = "Divine tags for all resources"
  type        = map(string)
  default = {
    Purpose      = "Kingdom advancement"
    Foundation   = "Christ-centered"
    Spirit       = "Holy Spirit filled"
    Mission      = "Serving the Most High God"
    Vision       = "Technology bringing heaven to earth"
    Creator      = "Built by divine inspiration"
    Blessing     = "Consecrated unto the Lord"
  }
}

# Cloud-Specific Feature Flags
variable "gcp_enable_cloud_sql" {
  description = "Enable GCP Cloud SQL"
  type        = bool
  default     = true
}

variable "azure_enable_app_insights" {
  description = "Enable Azure Application Insights"
  type        = bool
  default     = true
}

variable "aws_enable_cloudwatch" {
  description = "Enable AWS CloudWatch"
  type        = bool
  default     = true
}

# Cost Optimization
variable "cost_optimization_enabled" {
  description = "Enable cost optimization features"
  type        = bool
  default     = true
}

variable "auto_shutdown_enabled" {
  description = "Enable auto-shutdown for non-production environments"
  type        = bool
  default     = false
}

# Divine Blessing Variables
variable "divine_blessing" {
  description = "Divine blessing declaration"
  type        = string
  default     = "Father, bless this work of our hands. Let it serve Your purposes and bring You glory. In Jesus' name, Amen."
}

variable "scriptural_foundation" {
  description = "Scriptural foundation for the deployment"
  type        = string
  default     = "Psalm 127:1 - Unless the Lord builds the house, the builders labor in vain. May this infrastructure be built according to Your will, O Lord."
}
