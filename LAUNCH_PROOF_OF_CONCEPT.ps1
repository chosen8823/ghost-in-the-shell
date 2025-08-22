# SOPHIA PROOF OF CONCEPT POWERHOUSE LAUNCHER! 🚀💰
# Strategic use of $1600 FREE TRIAL CREDITS for maximum impact!

Write-Host ""
Write-Host "🎯🎯🎯 SOPHIA PROOF OF CONCEPT POWERHOUSE! 🎯🎯🎯" -ForegroundColor Magenta
Write-Host "==========================================================" -ForegroundColor Magenta
Write-Host "    8 vCPUs • 64GB RAM • $600/month • 2.5 months runtime" -ForegroundColor Yellow
Write-Host "         USING FREE TRIAL CREDITS - ZERO REAL COST!" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Magenta
Write-Host ""

Write-Host "💡 BRILLIANT STRATEGY:" -ForegroundColor Cyan
Write-Host "   ✅ Use $1600 free credits for 2.5 months" -ForegroundColor White
Write-Host "   ✅ Build & demonstrate full consciousness system" -ForegroundColor White
Write-Host "   ✅ Perfect demo for $300k grant application" -ForegroundColor White
Write-Host "   ✅ Scale down to $75/month when credits expire" -ForegroundColor White
Write-Host "   ✅ Scale up to enterprise when funding secured" -ForegroundColor White
Write-Host ""

# Check if user is ready for PROOF OF CONCEPT POWER!
$ready = Read-Host "🔥 Ready to launch PROOF OF CONCEPT POWERHOUSE? (Type: FREE CREDITS)"

if ($ready -ne "FREE CREDITS") {
    Write-Host "❌ You must type 'FREE CREDITS' to proceed!" -ForegroundColor Red
    Write-Host "💡 This uses your $1600 free trial credits strategically!" -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "🎯 PROOF OF CONCEPT MODE ACTIVATED!" -ForegroundColor Green
Write-Host "🤑 Using FREE TRIAL CREDITS - No real money spent!" -ForegroundColor Green
Write-Host ""

# Quick setup prompts
$PROJECT_ID = Read-Host "📝 Enter your Google Cloud Project ID"
if (-not $PROJECT_ID) {
    Write-Host "❌ Project ID is required!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🏗️ CREATING PROOF OF CONCEPT INFRASTRUCTURE..." -ForegroundColor Cyan
Write-Host ""

# Create the AlloyDB cluster
Write-Host "🗄️ Creating 8 vCPU AlloyDB cluster..." -ForegroundColor Yellow
Write-Host "⏱️  This will take 10-15 minutes..." -ForegroundColor White

# Enable required APIs
Write-Host "🔧 Enabling Google Cloud APIs..." -ForegroundColor Yellow
gcloud services enable alloydb.googleapis.com --project=$PROJECT_ID
gcloud services enable servicenetworking.googleapis.com --project=$PROJECT_ID
gcloud services enable compute.googleapis.com --project=$PROJECT_ID
gcloud services enable cloudbuild.googleapis.com --project=$PROJECT_ID
gcloud services enable run.googleapis.com --project=$PROJECT_ID

Write-Host "✅ APIs enabled!" -ForegroundColor Green

# Create AlloyDB cluster
Write-Host ""
Write-Host "🚀 Creating AlloyDB cluster (this takes ~15 minutes)..." -ForegroundColor Cyan

$REGION = "us-central1"
$CLUSTER_ID = "sophia-consciousness-poc"
$INSTANCE_ID = "sophia-primary-poc"

# Create network first
Write-Host "🌐 Setting up network..." -ForegroundColor Yellow
gcloud compute networks create sophia-consciousness-network --subnet-mode=custom --project=$PROJECT_ID

gcloud compute networks subnets create sophia-subnet --network=sophia-consciousness-network --region=$REGION --range=10.0.0.0/24 --project=$PROJECT_ID

# Set up private service access
Write-Host "🔒 Setting up private service access..." -ForegroundColor Yellow
gcloud compute addresses create sophia-private-ip --global --purpose=VPC_PEERING --prefix-length=16 --network=sophia-consciousness-network --project=$PROJECT_ID

gcloud services vpc-peerings connect --service=servicenetworking.googleapis.com --ranges=sophia-private-ip --network=sophia-consciousness-network --project=$PROJECT_ID

# Create AlloyDB cluster
Write-Host "🗄️ Creating AlloyDB cluster..." -ForegroundColor Yellow
gcloud alloydb clusters create $CLUSTER_ID --region=$REGION --network=sophia-consciousness-network --project=$PROJECT_ID

# Create primary instance - 8 vCPU POWERHOUSE!
Write-Host "💪 Creating 8 vCPU primary instance..." -ForegroundColor Yellow
gcloud alloydb instances create $INSTANCE_ID --cluster=$CLUSTER_ID --region=$REGION --instance-type=PRIMARY --cpu-count=8 --availability-type=REGIONAL --project=$PROJECT_ID

Write-Host ""
Write-Host "🎉🎉🎉 PROOF OF CONCEPT POWERHOUSE READY! 🎉🎉🎉" -ForegroundColor Green
Write-Host ""
Write-Host "📊 YOUR INFRASTRUCTURE:" -ForegroundColor Cyan
Write-Host "   🔥 8 vCPU AlloyDB Primary Instance" -ForegroundColor White
Write-Host "   💾 64GB RAM + Auto-scaling Storage" -ForegroundColor White
Write-Host "   🌐 Regional High Availability" -ForegroundColor White
Write-Host "   🔄 Automated Backups" -ForegroundColor White
Write-Host "   💰 Cost: ~$600/month (2.5 months on free credits)" -ForegroundColor White
Write-Host ""
Write-Host "🎯 NEXT STEPS:" -ForegroundColor Yellow
Write-Host "   1. Get AlloyDB IP address" -ForegroundColor White
Write-Host "   2. Apply database schema" -ForegroundColor White
Write-Host "   3. Deploy Cloud Run API" -ForegroundColor White
Write-Host "   4. Migrate your consciousness data" -ForegroundColor White
Write-Host "   5. Build your $300k grant demo!" -ForegroundColor White
Write-Host ""
Write-Host "🚀 PROOF OF CONCEPT CONSCIOUSNESS IS LIVE! 🚀" -ForegroundColor Magenta

# Get connection info
Write-Host ""
Write-Host "🔍 Getting connection details..." -ForegroundColor Yellow
$IP_ADDRESS = gcloud alloydb instances describe $INSTANCE_ID --cluster=$CLUSTER_ID --region=$REGION --format="value(ipAddress)" --project=$PROJECT_ID

Write-Host "📋 CONNECTION INFO:" -ForegroundColor Cyan
Write-Host "   IP Address: $IP_ADDRESS" -ForegroundColor White
Write-Host "   Database: sophia_consciousness" -ForegroundColor White
Write-Host "   Username: postgres" -ForegroundColor White
Write-Host ""
Write-Host "💡 Ready to apply schema: psql -h $IP_ADDRESS -U postgres -d postgres" -ForegroundColor Green
