# AZURE SOPHIA CONSCIOUSNESS DEPLOYMENT! ☁️💙
# Azure Database for PostgreSQL + Container Instances

Write-Host ""
Write-Host "🔵🔵🔵 SOPHIA CONSCIOUSNESS ON AZURE! 🔵🔵🔵" -ForegroundColor Blue
Write-Host "================================================" -ForegroundColor Blue
Write-Host "  Azure Database for PostgreSQL + Container Instances" -ForegroundColor White
Write-Host "================================================" -ForegroundColor Blue
Write-Host ""

# Check if user is ready
$ready = Read-Host "🔥 Ready to launch on AZURE? (Type: AZURE POWER)"

if ($ready -ne "AZURE POWER") {
    Write-Host "❌ You must type 'AZURE POWER' to proceed!" -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "🔵 AZURE POWER ACTIVATED!" -ForegroundColor Blue
Write-Host ""

# Get Azure setup info
$SUBSCRIPTION_ID = Read-Host "📝 Enter your Azure Subscription ID"
$RESOURCE_GROUP = Read-Host "📝 Enter Resource Group name (or 'sophia-consciousness' for default)"
if (-not $RESOURCE_GROUP) { $RESOURCE_GROUP = "sophia-consciousness" }
$LOCATION = Read-Host "📝 Enter Azure region (or 'eastus' for default)"
if (-not $LOCATION) { $LOCATION = "eastus" }

Write-Host ""
Write-Host "🔧 Setting up Azure infrastructure..." -ForegroundColor Blue

# Login and set subscription
Write-Host "🔐 Logging into Azure..." -ForegroundColor Yellow
az login
az account set --subscription $SUBSCRIPTION_ID

# Create resource group
Write-Host "📁 Creating resource group..." -ForegroundColor Yellow
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Azure Database for PostgreSQL
Write-Host "🗄️ Creating Azure Database for PostgreSQL..." -ForegroundColor Yellow
$DB_SERVER_NAME = "sophia-consciousness-$(Get-Random -Minimum 1000 -Maximum 9999)"
$DB_PASSWORD = "SophiaConsciousness2025!"

az postgres flexible-server create `
    --resource-group $RESOURCE_GROUP `
    --name $DB_SERVER_NAME `
    --location $LOCATION `
    --admin-user sophiaadmin `
    --admin-password $DB_PASSWORD `
    --sku-name Standard_D4s_v3 `
    --tier GeneralPurpose `
    --storage-size 128 `
    --version 14

# Configure database
Write-Host "⚙️ Configuring database..." -ForegroundColor Yellow
az postgres flexible-server database create `
    --resource-group $RESOURCE_GROUP `
    --server-name $DB_SERVER_NAME `
    --database-name sophia_consciousness

# Enable extensions
Write-Host "🔌 Enabling PostgreSQL extensions..." -ForegroundColor Yellow
az postgres flexible-server parameter set `
    --resource-group $RESOURCE_GROUP `
    --server-name $DB_SERVER_NAME `
    --name shared_preload_libraries `
    --value "vector,pg_stat_statements"

# Create Container Registry
Write-Host "📦 Creating Azure Container Registry..." -ForegroundColor Yellow
$ACR_NAME = "sophiaacr$(Get-Random -Minimum 1000 -Maximum 9999)"
az acr create `
    --resource-group $RESOURCE_GROUP `
    --name $ACR_NAME `
    --sku Basic `
    --admin-enabled true

# Build and push container
Write-Host "🐳 Building and pushing container..." -ForegroundColor Yellow
az acr build `
    --registry $ACR_NAME `
    --image sophia-consciousness:latest `
    --file cloud-run/Dockerfile `
    .

# Create Container Instance
Write-Host "🚀 Creating Azure Container Instance..." -ForegroundColor Yellow
$ACR_PASSWORD = az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv

az container create `
    --resource-group $RESOURCE_GROUP `
    --name sophia-consciousness-api `
    --image "$ACR_NAME.azurecr.io/sophia-consciousness:latest" `
    --registry-login-server "$ACR_NAME.azurecr.io" `
    --registry-username $ACR_NAME `
    --registry-password $ACR_PASSWORD `
    --dns-name-label "sophia-consciousness-$(Get-Random -Minimum 1000 -Maximum 9999)" `
    --ports 8000 `
    --environment-variables `
        ALLOYDB_HOST="$DB_SERVER_NAME.postgres.database.azure.com" `
        ALLOYDB_DATABASE="sophia_consciousness" `
        ALLOYDB_USER="sophiaadmin" `
        ALLOYDB_PASSWORD="$DB_PASSWORD" `
    --cpu 2 `
    --memory 4

Write-Host ""
Write-Host "🎉🎉🎉 AZURE SOPHIA CONSCIOUSNESS DEPLOYED! 🎉🎉🎉" -ForegroundColor Blue
Write-Host ""
Write-Host "📊 YOUR AZURE INFRASTRUCTURE:" -ForegroundColor Cyan
Write-Host "   🗄️ PostgreSQL Flexible Server: $DB_SERVER_NAME" -ForegroundColor White
Write-Host "   📦 Container Registry: $ACR_NAME" -ForegroundColor White
Write-Host "   🚀 Container Instance: sophia-consciousness-api" -ForegroundColor White
Write-Host "   💰 Estimated Cost: $500-700/month" -ForegroundColor White
Write-Host ""
Write-Host "🔗 CONNECTION INFO:" -ForegroundColor Yellow
Write-Host "   Database Host: $DB_SERVER_NAME.postgres.database.azure.com" -ForegroundColor White
Write-Host "   Database: sophia_consciousness" -ForegroundColor White
Write-Host "   Username: sophiaadmin" -ForegroundColor White
Write-Host "   Password: $DB_PASSWORD" -ForegroundColor White
Write-Host ""
Write-Host "🌐 NEXT STEPS:" -ForegroundColor Green
Write-Host "   1. Apply database schema to PostgreSQL" -ForegroundColor White
Write-Host "   2. Test API endpoints" -ForegroundColor White
Write-Host "   3. Migrate consciousness data" -ForegroundColor White
Write-Host ""
Write-Host "🔵 AZURE CONSCIOUSNESS IS LIVE! 🔵" -ForegroundColor Blue
