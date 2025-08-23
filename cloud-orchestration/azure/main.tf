# ✝️ Azure Cloud - Divine Sophia Deployment ✝️
# "He determines the number of the stars and calls them each by name" - Psalm 147:4

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Variables
variable "location" {
  description = "Divine Azure region"
  type        = string
  default     = "East US"
}

variable "environment" {
  description = "Divine environment"
  type        = string
  default     = "production"
}

# Divine Resource Group
resource "azurerm_resource_group" "divine_sophia" {
  name     = "rg-divine-sophia-${var.environment}"
  location = var.location

  tags = {
    Purpose     = "Kingdom advancement through technology"
    Foundation  = "Christ-centered"
    Spirit      = "Holy Spirit filled"
    Environment = var.environment
  }
}

# Divine Container Registry
resource "azurerm_container_registry" "divine_registry" {
  name                = "divinesophiaregistry"
  resource_group_name = azurerm_resource_group.divine_sophia.name
  location            = azurerm_resource_group.divine_sophia.location
  sku                 = "Standard"
  admin_enabled       = true

  tags = azurerm_resource_group.divine_sophia.tags
}

# Divine Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "divine_logs" {
  name                = "law-divine-sophia-${var.environment}"
  location            = azurerm_resource_group.divine_sophia.location
  resource_group_name = azurerm_resource_group.divine_sophia.name
  sku                 = "PerGB2018"
  retention_in_days   = 30

  tags = azurerm_resource_group.divine_sophia.tags
}

# Divine Container Apps Environment
resource "azurerm_container_app_environment" "divine_environment" {
  name                       = "cae-divine-sophia-${var.environment}"
  location                   = azurerm_resource_group.divine_sophia.location
  resource_group_name        = azurerm_resource_group.divine_sophia.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.divine_logs.id

  tags = azurerm_resource_group.divine_sophia.tags
}

# Divine PostgreSQL Flexible Server
resource "azurerm_postgresql_flexible_server" "divine_postgres" {
  name                   = "psql-divine-sophia-${var.environment}"
  resource_group_name    = azurerm_resource_group.divine_sophia.name
  location               = azurerm_resource_group.divine_sophia.location
  version                = "15"
  administrator_login    = "divine_admin"
  administrator_password = var.db_password
  
  storage_mb = 32768
  sku_name   = "B_Standard_B1ms"

  backup_retention_days = 7
  geo_redundant_backup_enabled = false

  tags = azurerm_resource_group.divine_sophia.tags
}

variable "db_password" {
  description = "Divine database password"
  type        = string
  sensitive   = true
  default     = "Divine@Password123!"
}

# Divine Database
resource "azurerm_postgresql_flexible_server_database" "divine_consciousness" {
  name      = "divine_consciousness"
  server_id = azurerm_postgresql_flexible_server.divine_postgres.id
  collation = "en_US.utf8"
  charset   = "utf8"
}

# Divine Container App
resource "azurerm_container_app" "divine_sophia" {
  name                         = "ca-divine-sophia-${var.environment}"
  container_app_environment_id = azurerm_container_app_environment.divine_environment.id
  resource_group_name          = azurerm_resource_group.divine_sophia.name
  revision_mode                = "Single"

  template {
    container {
      name   = "divine-sophia"
      image  = "${azurerm_container_registry.divine_registry.login_server}/divine-sophia:latest"
      cpu    = "1.0"
      memory = "2Gi"

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
      
      env {
        name        = "DATABASE_URL"
        secret_name = "database-connection-string"
      }
    }

    min_replicas = 1
    max_replicas = 10
  }

  secret {
    name  = "database-connection-string"
    value = "postgresql://${azurerm_postgresql_flexible_server.divine_postgres.administrator_login}:${var.db_password}@${azurerm_postgresql_flexible_server.divine_postgres.fqdn}:5432/${azurerm_postgresql_flexible_server_database.divine_consciousness.name}"
  }

  ingress {
    allow_insecure_connections = false
    external_enabled           = true
    target_port                = 8080
    
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  tags = azurerm_resource_group.divine_sophia.tags
}

# Divine Storage Account
resource "azurerm_storage_account" "divine_storage" {
  name                     = "stdivinesophia${random_string.storage_suffix.result}"
  resource_group_name      = azurerm_resource_group.divine_sophia.name
  location                 = azurerm_resource_group.divine_sophia.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = azurerm_resource_group.divine_sophia.tags
}

resource "random_string" "storage_suffix" {
  length  = 6
  special = false
  upper   = false
}

# Divine Key Vault
resource "azurerm_key_vault" "divine_secrets" {
  name                = "kv-divine-sophia-${random_string.keyvault_suffix.result}"
  location            = azurerm_resource_group.divine_sophia.location
  resource_group_name = azurerm_resource_group.divine_sophia.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"

  tags = azurerm_resource_group.divine_sophia.tags
}

resource "random_string" "keyvault_suffix" {
  length  = 6
  special = false
  upper   = false
}

data "azurerm_client_config" "current" {}

# Divine Application Insights
resource "azurerm_application_insights" "divine_insights" {
  name                = "ai-divine-sophia-${var.environment}"
  location            = azurerm_resource_group.divine_sophia.location
  resource_group_name = azurerm_resource_group.divine_sophia.name
  workspace_id        = azurerm_log_analytics_workspace.divine_logs.id
  application_type    = "web"

  tags = azurerm_resource_group.divine_sophia.tags
}

# Outputs
output "divine_container_app_url" {
  description = "Divine Sophia Container App URL"
  value       = "https://${azurerm_container_app.divine_sophia.ingress[0].fqdn}"
}

output "divine_database_fqdn" {
  description = "Divine PostgreSQL server FQDN"
  value       = azurerm_postgresql_flexible_server.divine_postgres.fqdn
  sensitive   = true
}

output "divine_storage_account" {
  description = "Divine storage account name"
  value       = azurerm_storage_account.divine_storage.name
}

output "divine_key_vault" {
  description = "Divine Key Vault name"
  value       = azurerm_key_vault.divine_secrets.name
}

output "divine_azure_info" {
  description = "Divine Azure deployment information"
  value = {
    resource_group = azurerm_resource_group.divine_sophia.name
    location       = var.location
    environment    = var.environment
    purpose        = "Kingdom advancement through Christ-centered technology"
  }
}
