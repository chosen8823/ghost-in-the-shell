# SOPHIA CONSCIOUSNESS - BUDGET STARTER PLAN! 💰
# Perfect for $75-125/month until you get that $300k grant! 🚀

Write-Host ""
Write-Host "💰💰💰 SOPHIA BUDGET STARTER DEPLOYMENT 💰💰💰" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green
Write-Host "         Smart Cloud • Full Features • Budget Price" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Green
Write-Host ""

Write-Host "💡 BUDGET PLAN SPECS:" -ForegroundColor Cyan
Write-Host "   🗄️  Cloud SQL PostgreSQL (2 vCPUs, 8GB RAM)" -ForegroundColor White
Write-Host "   🚀 Cloud Run (Basic scaling, 2GB RAM)" -ForegroundColor White
Write-Host "   💾 100GB SSD Storage" -ForegroundColor White
Write-Host "   📊 Basic monitoring included" -ForegroundColor White
Write-Host "   💰 Total: $75-125/month" -ForegroundColor Yellow
Write-Host ""

Write-Host "🎯 UPGRADE PATH READY:" -ForegroundColor Magenta
Write-Host "   When you get the $300k grant, instant upgrade to:" -ForegroundColor White
Write-Host "   🔥 32 vCPU AlloyDB Enterprise" -ForegroundColor White
Write-Host "   🚀 50x Cloud Run scaling" -ForegroundColor White
Write-Host "   📊 Enterprise monitoring dashboard" -ForegroundColor White
Write-Host ""

# Get project setup
$PROJECT_ID = Read-Host "📝 Enter your Google Cloud Project ID"
if (-not $PROJECT_ID) {
    Write-Host "❌ Project ID is required!" -ForegroundColor Red
    exit 1
}

$REGION = Read-Host "🌍 Enter region (default: us-central1)"
if (-not $REGION) { $REGION = "us-central1" }

Write-Host ""
Write-Host "🎯 Creating BUDGET Sophia infrastructure..." -ForegroundColor Cyan

# Set project
Write-Host "🔧 Setting up project..." -ForegroundColor Yellow
gcloud config set project $PROJECT_ID

# Enable APIs
Write-Host "🔌 Enabling required APIs..." -ForegroundColor Yellow
gcloud services enable sqladmin.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Create Cloud SQL instance (BUDGET VERSION)
Write-Host "🗄️ Creating Cloud SQL PostgreSQL instance..." -ForegroundColor Cyan
Write-Host "   💰 Cost: ~$40-60/month" -ForegroundColor Yellow

gcloud sql instances create sophia-consciousness-db `
    --database-version=POSTGRES_15 `
    --tier=db-custom-2-8192 `
    --region=$REGION `
    --storage-type=SSD `
    --storage-size=100GB `
    --storage-auto-increase `
    --backup-start-time=02:00 `
    --enable-bin-log `
    --deletion-protection

# Create database
Write-Host "📊 Creating consciousness database..." -ForegroundColor Cyan
gcloud sql databases create sophia_consciousness --instance=sophia-consciousness-db

# Set password for postgres user
Write-Host "🔐 Setting database password..." -ForegroundColor Yellow
$DB_PASSWORD = [System.Web.Security.Membership]::GeneratePassword(16, 4)
gcloud sql users set-password postgres --instance=sophia-consciousness-db --password=$DB_PASSWORD

# Get connection details
$CONNECTION_NAME = gcloud sql instances describe sophia-consciousness-db --format="value(connectionName)"

Write-Host ""
Write-Host "✅ BUDGET SOPHIA DATABASE CREATED!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 CONNECTION INFO:" -ForegroundColor Cyan
Write-Host "   Instance: sophia-consciousness-db" -ForegroundColor White
Write-Host "   Database: sophia_consciousness" -ForegroundColor White
Write-Host "   Connection: $CONNECTION_NAME" -ForegroundColor White
Write-Host "   Password: $DB_PASSWORD" -ForegroundColor Yellow
Write-Host ""

# Save connection info
$connectionInfo = @"
# SOPHIA BUDGET DATABASE CONNECTION
PROJECT_ID=$PROJECT_ID
INSTANCE_ID=sophia-consciousness-db
DATABASE_NAME=sophia_consciousness
CONNECTION_NAME=$CONNECTION_NAME
DB_PASSWORD=$DB_PASSWORD
REGION=$REGION
"@

$connectionInfo | Out-File -FilePath "budget_connection_info.txt" -Encoding UTF8

Write-Host "💾 Connection info saved to: budget_connection_info.txt" -ForegroundColor Green
Write-Host ""

Write-Host "🎉 NEXT STEPS:" -ForegroundColor Magenta
Write-Host "1. Apply database schema: Use Cloud Shell or local psql" -ForegroundColor White
Write-Host "2. Deploy Cloud Run API (budget version)" -ForegroundColor White
Write-Host "3. Migrate your data" -ForegroundColor White
Write-Host "4. Start using your budget Sophia consciousness!" -ForegroundColor White
Write-Host ""
Write-Host "💡 When you get the $300k grant, run: .\LAUNCH_BEAST_MODE.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "🌟 BUDGET SOPHIA IS READY! 🌟" -ForegroundColor Green
