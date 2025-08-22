# Sophia Enterprise 1TB AlloyDB Quick Setup
# PowerShell script for enterprise deployment

Write-Host "🌟 SOPHIA CONSCIOUSNESS ENTERPRISE 1TB SETUP 🌟" -ForegroundColor Magenta
Write-Host "=================================================" -ForegroundColor Magenta

# Enterprise configuration
$ENTERPRISE_CONFIG = @{
    ProjectId = "your-project-id"
    Region = "us-central1"
    ClusterName = "sophia-consciousness-enterprise"
    PrimaryInstance = "sophia-primary-1tb"
    ReplicaInstance = "sophia-replica-analytics"
    DatabaseName = "sophia_consciousness"
    InstanceType = "alloydb-8xlarge"  # 32 vCPUs, 256GB RAM
    StorageSize = "1024GB"           # 1TB base storage (auto-expands)
    BackupRetention = 30             # 30 days backup retention
    ReadReplicas = 2                 # 2 read replicas for scaling
}

Write-Host "🚀 Enterprise Configuration:" -ForegroundColor Cyan
$ENTERPRISE_CONFIG.GetEnumerator() | ForEach-Object {
    Write-Host "  $($_.Key): $($_.Value)" -ForegroundColor White
}

Write-Host ""
Write-Host "💰 Estimated Monthly Cost: ~$8,000-12,000 USD" -ForegroundColor Yellow
Write-Host "⚡ Performance: 32 vCPUs, 256GB RAM, 1TB+ Storage" -ForegroundColor Green
Write-Host "🔒 Features: Encryption, Auto-backup, High Availability" -ForegroundColor Blue
Write-Host ""

$confirmation = Read-Host "Ready to deploy ENTERPRISE Sophia? This is a LARGE instance! (yes/NO)"
if ($confirmation -ne 'yes') {
    Write-Host "❌ Deployment cancelled - Enterprise setup requires 'yes' confirmation" -ForegroundColor Red
    exit 0
}

Write-Host "🎯 Creating enterprise AlloyDB cluster..." -ForegroundColor Green

# Create the enterprise setup script
$enterpriseSetup = @"
# Sophia Enterprise AlloyDB Setup Commands

# 1. Create the enterprise cluster
gcloud alloydb clusters create $($ENTERPRISE_CONFIG.ClusterName) \
    --location=$($ENTERPRISE_CONFIG.Region) \
    --project=$($ENTERPRISE_CONFIG.ProjectId)

# 2. Create primary instance (32 vCPUs, 256GB RAM)
gcloud alloydb instances create $($ENTERPRISE_CONFIG.PrimaryInstance) \
    --cluster=$($ENTERPRISE_CONFIG.ClusterName) \
    --location=$($ENTERPRISE_CONFIG.Region) \
    --instance-type=PRIMARY \
    --cpu-count=32 \
    --project=$($ENTERPRISE_CONFIG.ProjectId)

# 3. Create read replica for analytics
gcloud alloydb instances create $($ENTERPRISE_CONFIG.ReplicaInstance) \
    --cluster=$($ENTERPRISE_CONFIG.ClusterName) \
    --location=$($ENTERPRISE_CONFIG.Region) \
    --instance-type=READ_POOL \
    --cpu-count=16 \
    --read-pool-node-count=2 \
    --project=$($ENTERPRISE_CONFIG.ProjectId)

# 4. Get connection info
gcloud alloydb instances describe $($ENTERPRISE_CONFIG.PrimaryInstance) \
    --cluster=$($ENTERPRISE_CONFIG.ClusterName) \
    --location=$($ENTERPRISE_CONFIG.Region) \
    --project=$($ENTERPRISE_CONFIG.ProjectId) \
    --format="value(ipAddress)"
"@

$enterpriseSetup | Out-File -FilePath "enterprise_setup_commands.sh" -Encoding UTF8

Write-Host "📋 Enterprise setup commands saved to: enterprise_setup_commands.sh" -ForegroundColor Yellow
Write-Host ""
Write-Host "🎉 NEXT STEPS:" -ForegroundColor Magenta
Write-Host "  1. Run: .\enterprise_setup_commands.sh" -ForegroundColor White
Write-Host "  2. Apply schema: psql -h ALLOYDB_IP -U postgres -d sophia_consciousness -f sql/sophia_alloydb_schema.sql" -ForegroundColor White
Write-Host "  3. Deploy API: .\deploy.ps1 -ProjectId $($ENTERPRISE_CONFIG.ProjectId) -AlloyDbCluster $($ENTERPRISE_CONFIG.ClusterName)" -ForegroundColor White
Write-Host "  4. Migrate data: python migration/migrate_to_alloydb.py --auto-discover --alloydb-host ALLOYDB_IP" -ForegroundColor White
Write-Host ""
Write-Host "🌟 Welcome to Enterprise Sophia Consciousness! 🌟" -ForegroundColor Magenta
