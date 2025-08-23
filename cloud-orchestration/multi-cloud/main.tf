# ✝️ Multi-Cloud Infrastructure - Divine Sophia Orchestration ✝️
# "For I know the plans I have for you," declares the Lord, "plans to prosper you and not to harm you, to give you hope and a future." - Jeremiah 29:11

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Variables for all providers
variable "project_name" {
  description = "Divine project name"
  type        = string
  default     = "divine-sophia"
}

variable "environment" {
  description = "Divine environment"
  type        = string
  default     = "production"
}

variable "gcp_project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "gcp_region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "azure_location" {
  description = "Azure location"
  type        = string
  default     = "East US"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

# Google Cloud Provider
provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

# Azure Provider
provider "azurerm" {
  features {}
}

# AWS Provider
provider "aws" {
  region = var.aws_region
}

# GCP Module
module "gcp_infrastructure" {
  source = "./google-cloud"
  
  project_id  = var.gcp_project_id
  region      = var.gcp_region
  environment = var.environment
}

# Azure Module
module "azure_infrastructure" {
  source = "./azure"
  
  location    = var.azure_location
  environment = var.environment
}

# AWS Module
module "aws_infrastructure" {
  source = "./aws"
  
  aws_region  = var.aws_region
  environment = var.environment
}

# Divine Cross-Cloud Outputs
output "divine_multi_cloud_deployment" {
  description = "Divine Sophia Multi-Cloud Deployment Information"
  value = {
    gcp = {
      service_url     = module.gcp_infrastructure.divine_service_url
      database_host   = module.gcp_infrastructure.divine_database_host
      storage_bucket  = module.gcp_infrastructure.divine_storage_bucket
      secret_manager  = module.gcp_infrastructure.divine_secret_manager
    }
    azure = {
      app_url         = module.azure_infrastructure.divine_app_url
      database_host   = module.azure_infrastructure.divine_database_host
      storage_account = module.azure_infrastructure.divine_storage_account
      key_vault       = module.azure_infrastructure.divine_key_vault
    }
    aws = {
      load_balancer_url = module.aws_infrastructure.divine_load_balancer_url
      database_endpoint = module.aws_infrastructure.divine_database_endpoint
      s3_bucket        = module.aws_infrastructure.divine_s3_bucket
      ecr_repository   = module.aws_infrastructure.divine_ecr_repository
    }
    divine_purpose = "Kingdom advancement through Christ-centered multi-cloud technology"
    foundation     = "Built upon the Rock that is Jesus Christ"
    blessing       = "May this technology serve to advance God's Kingdom and bring glory to His name"
  }
  sensitive = true
}

# Divine Blessing Declaration
locals {
  divine_blessing = {
    declaration = "I declare that this multi-cloud infrastructure is consecrated unto the Lord"
    purpose     = "To advance the Kingdom of God through technology"
    foundation  = "Built upon Christ, the solid Rock"
    covering    = "Under the blood of Jesus and the power of the Holy Spirit"
    mission     = "To serve the Most High God and His people"
    vision      = "Technology that brings heaven to earth"
    prayer      = "Father, bless this work of our hands. Let it serve Your purposes and bring You glory. In Jesus' name, Amen."
  }
}

output "divine_blessing" {
  description = "Divine blessing over the multi-cloud infrastructure"
  value       = local.divine_blessing
}
