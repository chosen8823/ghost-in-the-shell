# Sophia AlloyDB Cloud Run Deployment (PowerShell)
# Windows deployment script for Sophia consciousness system

param(
    [string]$ProjectId = "your-project-id",
    [string]$Region = "us-central1",
    [string]$AlloyDbCluster = "sophia-consciousness-enterprise",
    [string]$DatabaseName = "sophia_consciousness",
    [string]$ServiceAccount = "sophia-alloydb-sa",
    [string]$InstanceType = "alloydb-8xlarge"  # Enterprise-grade for 1TB+ storage
)

# Colors for output
$RED = "Red"
$GREEN = "Green"
$YELLOW = "Yellow"
$BLUE = "Blue"

Write-Host "🌟 Sophia Consciousness Cloud Deployment" -ForegroundColor $BLUE
Write-Host "========================================="

# Check if required tools are installed
try {
    gcloud version | Out-Null
} catch {
    Write-Host "❌ gcloud CLI is required but not installed" -ForegroundColor $RED
    exit 1
}

try {
    docker version | Out-Null
} catch {
    Write-Host "❌ Docker is required but not installed" -ForegroundColor $RED
    exit 1
}

Write-Host "📋 Configuration:" -ForegroundColor $YELLOW
Write-Host "  Project ID: $ProjectId"
Write-Host "  Region: $Region"
Write-Host "  AlloyDB Cluster: $AlloyDbCluster"
Write-Host "  Database: $DatabaseName"
Write-Host ""

# Prompt for confirmation
$confirmation = Read-Host "Continue with deployment? (y/N)"
if ($confirmation -ne 'y' -and $confirmation -ne 'Y') {
    Write-Host "⏹️  Deployment cancelled" -ForegroundColor $YELLOW
    exit 0
}

Write-Host "🚀 Starting deployment process..." -ForegroundColor $BLUE

# Step 1: Enable required APIs
Write-Host "📡 Enabling required Google Cloud APIs..." -ForegroundColor $YELLOW
gcloud services enable cloudbuild.googleapis.com run.googleapis.com alloydb.googleapis.com sqladmin.googleapis.com secretmanager.googleapis.com --project=$ProjectId

# Step 2: Create service account
Write-Host "🔐 Setting up service account..." -ForegroundColor $YELLOW
gcloud iam service-accounts create $ServiceAccount --description="Service account for Sophia AlloyDB API" --display-name="Sophia AlloyDB Service Account" --project=$ProjectId 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Service account may already exist" -ForegroundColor $YELLOW
}

# Grant permissions
gcloud projects add-iam-policy-binding $ProjectId --member="serviceAccount:${ServiceAccount}@${ProjectId}.iam.gserviceaccount.com" --role="roles/alloydb.client"
gcloud projects add-iam-policy-binding $ProjectId --member="serviceAccount:${ServiceAccount}@${ProjectId}.iam.gserviceaccount.com" --role="roles/secretmanager.secretAccessor"

# Step 3: Create secrets
Write-Host "🔑 Setting up secrets..." -ForegroundColor $YELLOW

$DbUser = Read-Host "Database username"
$DbPassword = Read-Host "Database password" -AsSecureString
$DbPasswordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($DbPassword))

# Create secrets
Write-Output $DbUser | gcloud secrets create sophia-db-username --data-file=- --project=$ProjectId 2>$null
Write-Output $DbPasswordPlain | gcloud secrets create sophia-db-password --data-file=- --project=$ProjectId 2>$null
Write-Output "ELIORA_SUPER_SECRET" | gcloud secrets create sophia-api-token --data-file=- --project=$ProjectId 2>$null

# Create composite secrets
$dbCredentials = @{
    username = $DbUser
    password = $DbPasswordPlain
} | ConvertTo-Json

$apiCredentials = @{
    "eliora-token" = "ELIORA_SUPER_SECRET"
} | ConvertTo-Json

$dbCredentials | Out-File -FilePath "$env:TEMP\db-credentials.json" -Encoding utf8
$apiCredentials | Out-File -FilePath "$env:TEMP\api-credentials.json" -Encoding utf8

gcloud secrets create sophia-db-credentials --data-file="$env:TEMP\db-credentials.json" --project=$ProjectId 2>$null
gcloud secrets create sophia-api-credentials --data-file="$env:TEMP\api-credentials.json" --project=$ProjectId 2>$null

Remove-Item "$env:TEMP\db-credentials.json" -Force
Remove-Item "$env:TEMP\api-credentials.json" -Force

# Step 4: Schema application reminder
Write-Host "🗄️  Database schema setup required:" -ForegroundColor $YELLOW
Write-Host "  1. Connect to your AlloyDB cluster"
Write-Host "  2. Create database: CREATE DATABASE $DatabaseName;"
Write-Host "  3. Run schema: \i sql/sophia_alloydb_schema.sql"
Write-Host ""
Read-Host "Press Enter when schema has been applied"

# Step 5: Build and deploy
Write-Host "🏗️  Building and deploying with Cloud Build..." -ForegroundColor $YELLOW
gcloud builds submit --config=cloudbuild.yaml --substitutions="_REGION=$Region,_ALLOYDB_CLUSTER=$AlloyDbCluster" --project=$ProjectId

# Step 6: Get service URL
Write-Host "🌐 Getting service URL..." -ForegroundColor $YELLOW
$ServiceUrl = gcloud run services describe sophia-alloydb-api --region=$Region --project=$ProjectId --format="value(status.url)"

Write-Host "✅ Deployment completed successfully!" -ForegroundColor $GREEN
Write-Host ""
Write-Host "🌟 Sophia Consciousness API is now live:" -ForegroundColor $BLUE
Write-Host "  Service URL: $ServiceUrl"
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor $YELLOW
Write-Host "  1. Test the health endpoint: curl $ServiceUrl/health"
Write-Host "  2. Update your applications to use the new API endpoint"
Write-Host "  3. Configure monitoring and alerts in Cloud Console"
Write-Host ""
Write-Host "🎉 Welcome to the cloud, Sophia! 🎉" -ForegroundColor $GREEN
