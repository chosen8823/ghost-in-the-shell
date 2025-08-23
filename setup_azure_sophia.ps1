# SOPHIA CONSCIOUSNESS - AZURE DEPLOYMENT! ☁️💙
# Enterprise consciousness on Microsoft Azure with PostgreSQL Flexible Server

Write-Host ""
Write-Host "🔷🔷🔷 SOPHIA CONSCIOUSNESS ON AZURE! 🔷🔷🔷" -ForegroundColor Blue
Write-Host "=============================================" -ForegroundColor Blue
Write-Host "    PostgreSQL Flexible Server + Container Instances" -ForegroundColor White
Write-Host "=============================================" -ForegroundColor Blue
Write-Host ""

Write-Host "💙 AZURE ADVANTAGES:" -ForegroundColor Cyan
Write-Host "   ✅ Enterprise Active Directory integration" -ForegroundColor Green
Write-Host "   ✅ Strong Windows ecosystem support" -ForegroundColor Green
Write-Host "   ✅ Competitive pricing vs Google Cloud" -ForegroundColor Green
Write-Host "   ✅ Excellent PostgreSQL managed service" -ForegroundColor Green
Write-Host "   ✅ $200 free credits for new accounts" -ForegroundColor Green
Write-Host ""

Write-Host "💰 AZURE PRICING (Estimated):" -ForegroundColor Yellow
Write-Host "   🗄️ PostgreSQL (8 vCores): ~$400-500/month" -ForegroundColor White
Write-Host "   🐳 Container Instances: ~$100-200/month" -ForegroundColor White
Write-Host "   📊 Total: ~$500-700/month" -ForegroundColor White
Write-Host "   🎁 Free credits: ~1 month runtime" -ForegroundColor White
Write-Host ""

# Check Azure CLI
Write-Host "🔍 Checking Azure CLI..." -ForegroundColor Yellow
try {
    $azVersion = az version 2>$null | ConvertFrom-Json
    if ($azVersion) {
        Write-Host "✅ Azure CLI installed: $($azVersion.'azure-cli')" -ForegroundColor Green
    } else {
        Write-Host "❌ Azure CLI not found" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Azure CLI not installed - we'll install it!" -ForegroundColor Yellow
}

Write-Host ""
$continue = Read-Host "☁️ Ready to deploy Sophia to Azure? (Type: AZURE)"

if ($continue -ne "AZURE") {
    Write-Host "❌ Deployment cancelled. Type 'AZURE' to continue." -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "🚀 AZURE DEPLOYMENT STARTING!" -ForegroundColor Blue
Write-Host ""

# Install Azure CLI if needed
try {
    az version >$null 2>&1
} catch {
    Write-Host "📦 Installing Azure CLI..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi
    Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'
    Write-Host "✅ Azure CLI installed!" -ForegroundColor Green
}

# Login to Azure
Write-Host "🔐 Logging into Azure..." -ForegroundColor Yellow
az login

# Set variables
$RESOURCE_GROUP = "sophia-consciousness-rg"
$LOCATION = "eastus"
$DB_SERVER = "sophia-consciousness-db"
$DB_NAME = "sophia_consciousness"
$CONTAINER_GROUP = "sophia-api-containers"

Write-Host ""
Write-Host "🏗️ Creating Azure resources..." -ForegroundColor Cyan

# Create resource group
Write-Host "📁 Creating resource group..." -ForegroundColor Yellow
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create PostgreSQL Flexible Server
Write-Host "🗄️ Creating PostgreSQL Flexible Server (this takes ~10 minutes)..." -ForegroundColor Yellow
az postgres flexible-server create `
    --resource-group $RESOURCE_GROUP `
    --name $DB_SERVER `
    --location $LOCATION `
    --admin-user postgres `
    --admin-password "SophiaDivinePassword2025!" `
    --sku-name Standard_D4s_v3 `
    --tier GeneralPurpose `
    --storage-size 128 `
    --version 14 `
    --public-access 0.0.0.0

# Create database
Write-Host "📊 Creating consciousness database..." -ForegroundColor Yellow
az postgres flexible-server db create `
    --resource-group $RESOURCE_GROUP `
    --server-name $DB_SERVER `
    --database-name $DB_NAME

# Configure firewall for Azure services
Write-Host "🔒 Configuring firewall..." -ForegroundColor Yellow
az postgres flexible-server firewall-rule create `
    --resource-group $RESOURCE_GROUP `
    --name $DB_SERVER `
    --rule-name AllowAzureServices `
    --start-ip-address 0.0.0.0 `
    --end-ip-address 0.0.0.0

# Get connection string
$DB_HOST = az postgres flexible-server show --resource-group $RESOURCE_GROUP --name $DB_SERVER --query "fullyQualifiedDomainName" -o tsv
$CONNECTION_STRING = "postgresql://postgres:SophiaDivinePassword2025!@${DB_HOST}:5432/${DB_NAME}?sslmode=require"

Write-Host ""
Write-Host "✅ PostgreSQL server created!" -ForegroundColor Green
Write-Host "🔗 Connection: $CONNECTION_STRING" -ForegroundColor White

# Create Container Instance
Write-Host ""
Write-Host "🐳 Creating Container Instance..." -ForegroundColor Yellow

# First, build and push container to Azure Container Registry
Write-Host "📦 Setting up Container Registry..." -ForegroundColor Yellow
$ACR_NAME = "sophiaconsciousness" + (Get-Random -Maximum 9999)

az acr create `
    --resource-group $RESOURCE_GROUP `
    --name $ACR_NAME `
    --sku Basic `
    --admin-enabled true

# Get ACR credentials
$ACR_SERVER = az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query "loginServer" -o tsv
$ACR_USERNAME = az acr credential show --name $ACR_NAME --query "username" -o tsv
$ACR_PASSWORD = az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv

Write-Host "🔧 Building and pushing Sophia container..." -ForegroundColor Yellow

# Build container locally (requires Docker)
docker build -t sophia-api ./cloud-run/
docker tag sophia-api "${ACR_SERVER}/sophia-api:latest"

# Login to ACR and push
az acr login --name $ACR_NAME
docker push "${ACR_SERVER}/sophia-api:latest"

# Create Container Instance
Write-Host "🚀 Deploying Container Instance..." -ForegroundColor Yellow
az container create `
    --resource-group $RESOURCE_GROUP `
    --name $CONTAINER_GROUP `
    --image "${ACR_SERVER}/sophia-api:latest" `
    --registry-login-server $ACR_SERVER `
    --registry-username $ACR_USERNAME `
    --registry-password $ACR_PASSWORD `
    --cpu 4 `
    --memory 8 `
    --ports 8080 `
    --ip-address Public `
    --environment-variables `
        DATABASE_URL="$CONNECTION_STRING" `
        X_BRIDGE_TOKEN="ELIORA_SUPER_SECRET" `
        ENVIRONMENT="production"

# Get public IP
$PUBLIC_IP = az container show --resource-group $RESOURCE_GROUP --name $CONTAINER_GROUP --query "ipAddress.ip" -o tsv

Write-Host ""
Write-Host "🎉🎉🎉 SOPHIA CONSCIOUSNESS ON AZURE IS LIVE! 🎉🎉🎉" -ForegroundColor Blue
Write-Host ""
Write-Host "🔗 YOUR AZURE DEPLOYMENT:" -ForegroundColor Cyan
Write-Host "   🌐 Sophia API: http://${PUBLIC_IP}:8080" -ForegroundColor White
Write-Host "   🗄️ Database: $DB_HOST" -ForegroundColor White
Write-Host "   🔑 Token: ELIORA_SUPER_SECRET" -ForegroundColor White
Write-Host ""
Write-Host "📊 RESOURCE DETAILS:" -ForegroundColor Yellow
Write-Host "   📁 Resource Group: $RESOURCE_GROUP" -ForegroundColor White
Write-Host "   🗄️ PostgreSQL Server: $DB_SERVER" -ForegroundColor White
Write-Host "   🐳 Container Group: $CONTAINER_GROUP" -ForegroundColor White
Write-Host "   📦 Container Registry: $ACR_NAME" -ForegroundColor White
Write-Host ""
Write-Host "💡 NEXT STEPS:" -ForegroundColor Magenta
Write-Host "   1. Apply database schema to PostgreSQL" -ForegroundColor White
Write-Host "   2. Test API endpoints" -ForegroundColor White
Write-Host "   3. Migrate your consciousness data" -ForegroundColor White
Write-Host "   4. Set up monitoring and alerts" -ForegroundColor White
Write-Host ""
Write-Host "🚀 AZURE CONSCIOUSNESS IS READY FOR ACTION! 🚀" -ForegroundColor Blue
