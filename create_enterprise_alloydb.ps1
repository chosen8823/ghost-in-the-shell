# Sophia Enterprise AlloyDB Setup - PowerShell Version
# 1TB BEAST MODE DEPLOYMENT!

Write-Host "🚀 Creating Sophia Consciousness Enterprise AlloyDB..." -ForegroundColor Cyan

# Set variables (CHANGE THESE TO YOUR PROJECT!)
$PROJECT_ID = "your-project-id"
$REGION = "us-central1"
$CLUSTER_NAME = "sophia-consciousness-enterprise"
$PRIMARY_INSTANCE = "sophia-primary-1tb"
$REPLICA_INSTANCE = "sophia-replica-analytics"

Write-Host "⚙️ Configuration:" -ForegroundColor Yellow
Write-Host "  Project: $PROJECT_ID"
Write-Host "  Region: $REGION"
Write-Host "  Cluster: $CLUSTER_NAME"
Write-Host ""

# 1. Enable AlloyDB API
Write-Host "📡 Enabling AlloyDB API..." -ForegroundColor Green
gcloud services enable alloydb.googleapis.com --project=$PROJECT_ID

# 2. Create the ENTERPRISE cluster
Write-Host "🏗️ Creating enterprise AlloyDB cluster..." -ForegroundColor Green
gcloud alloydb clusters create $CLUSTER_NAME `
    --location=$REGION `
    --project=$PROJECT_ID `
    --automated-backup-retention-period=30d `
    --automated-backup-start-time="03:00"

# 3. Create PRIMARY instance - 32 vCPUs (MASSIVE!)
Write-Host "💪 Creating primary instance (32 vCPUs, 256GB RAM)..." -ForegroundColor Green
gcloud alloydb instances create $PRIMARY_INSTANCE `
    --cluster=$CLUSTER_NAME `
    --location=$REGION `
    --instance-type=PRIMARY `
    --cpu-count=32 `
    --project=$PROJECT_ID

# 4. Create READ REPLICA
Write-Host "📊 Creating read replica for analytics..." -ForegroundColor Green
gcloud alloydb instances create $REPLICA_INSTANCE `
    --cluster=$CLUSTER_NAME `
    --location=$REGION `
    --instance-type=READ_POOL `
    --cpu-count=16 `
    --read-pool-node-count=2 `
    --project=$PROJECT_ID

# 5. Get connection info
Write-Host "🌐 Getting connection information..." -ForegroundColor Cyan
Write-Host "Primary Instance IP:" -ForegroundColor Yellow
$IP_ADDRESS = gcloud alloydb instances describe $PRIMARY_INSTANCE `
    --cluster=$CLUSTER_NAME `
    --location=$REGION `
    --project=$PROJECT_ID `
    --format="value(ipAddress)"

Write-Host $IP_ADDRESS -ForegroundColor White

Write-Host ""
Write-Host "✅ ENTERPRISE ALLOYDB CREATED!" -ForegroundColor Green
Write-Host "🎯 Next steps:" -ForegroundColor Cyan
Write-Host "  1. Connect: psql -h $IP_ADDRESS -U postgres" -ForegroundColor White
Write-Host "  2. Create DB: CREATE DATABASE sophia_consciousness;" -ForegroundColor White
Write-Host "  3. Run schema: \i sql/sophia_alloydb_schema.sql" -ForegroundColor White
Write-Host "  4. Deploy API: .\deploy.ps1 -ProjectId $PROJECT_ID -AlloyDbCluster $CLUSTER_NAME" -ForegroundColor White
Write-Host ""
Write-Host "🌟 SOPHIA IS NOW ENTERPRISE READY! 🌟" -ForegroundColor Magenta
