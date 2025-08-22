# Sophia Enterprise AlloyDB Setup Commands - 1TB BEAST MODE!
echo "🚀 Creating Sophia Consciousness Enterprise AlloyDB..."

# Set variables (CHANGE THESE TO YOUR PROJECT!)
export PROJECT_ID="your-project-id"
export REGION="us-central1"
export CLUSTER_NAME="sophia-consciousness-enterprise"
export PRIMARY_INSTANCE="sophia-primary-1tb"
export REPLICA_INSTANCE="sophia-replica-analytics"

# 1. Enable AlloyDB API
echo "📡 Enabling AlloyDB API..."
gcloud services enable alloydb.googleapis.com --project=$PROJECT_ID

# 2. Create the ENTERPRISE cluster (with backup and encryption)
echo "🏗️ Creating enterprise AlloyDB cluster..."
gcloud alloydb clusters create $CLUSTER_NAME \
    --location=$REGION \
    --project=$PROJECT_ID \
    --automated-backup-retention-period=30d \
    --automated-backup-start-time="03:00"

# 3. Create PRIMARY instance - 32 vCPUs, 256GB RAM (MASSIVE!)
echo "💪 Creating primary instance (32 vCPUs, 256GB RAM)..."
gcloud alloydb instances create $PRIMARY_INSTANCE \
    --cluster=$CLUSTER_NAME \
    --location=$REGION \
    --instance-type=PRIMARY \
    --cpu-count=32 \
    --project=$PROJECT_ID

# 4. Create READ REPLICA for analytics (16 vCPUs)
echo "📊 Creating read replica for analytics..."
gcloud alloydb instances create $REPLICA_INSTANCE \
    --cluster=$CLUSTER_NAME \
    --location=$REGION \
    --instance-type=READ_POOL \
    --cpu-count=16 \
    --read-pool-node-count=2 \
    --project=$PROJECT_ID

# 5. Get connection info
echo "🌐 Getting connection information..."
echo "Primary Instance IP:"
gcloud alloydb instances describe $PRIMARY_INSTANCE \
    --cluster=$CLUSTER_NAME \
    --location=$REGION \
    --project=$PROJECT_ID \
    --format="value(ipAddress)"

echo ""
echo "✅ ENTERPRISE ALLOYDB CREATED!"
echo "🎯 Next: Connect with: psql -h <IP_ADDRESS> -U postgres"
echo "🗄️ Then run: \\i sql/sophia_alloydb_schema.sql"
echo "🚀 Finally: Deploy Cloud Run API!"
echo ""
echo "🌟 SOPHIA IS NOW ENTERPRISE READY! 🌟"
