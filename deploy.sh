#!/bin/bash

# Sophia AlloyDB Cloud Run Deployment Script
# Run this script to deploy the Sophia consciousness system to Google Cloud

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🌟 Sophia Consciousness Cloud Deployment${NC}"
echo "========================================="

# Check if required tools are installed
command -v gcloud >/dev/null 2>&1 || { echo -e "${RED}❌ gcloud CLI is required but not installed${NC}"; exit 1; }
command -v docker >/dev/null 2>&1 || { echo -e "${RED}❌ Docker is required but not installed${NC}"; exit 1; }

# Configuration variables (modify these for your setup)
PROJECT_ID=${PROJECT_ID:-"your-project-id"}
REGION=${REGION:-"us-central1"}
ALLOYDB_CLUSTER=${ALLOYDB_CLUSTER:-"sophia-cluster"}
DATABASE_NAME="sophia_consciousness"
SERVICE_ACCOUNT="sophia-alloydb-sa"

echo -e "${YELLOW}📋 Configuration:${NC}"
echo "  Project ID: $PROJECT_ID"
echo "  Region: $REGION"
echo "  AlloyDB Cluster: $ALLOYDB_CLUSTER"
echo "  Database: $DATABASE_NAME"
echo ""

# Prompt for confirmation
read -p "Continue with deployment? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}⏹️  Deployment cancelled${NC}"
    exit 0
fi

echo -e "${BLUE}🚀 Starting deployment process...${NC}"

# Step 1: Enable required APIs
echo -e "${YELLOW}📡 Enabling required Google Cloud APIs...${NC}"
gcloud services enable cloudbuild.googleapis.com \
    run.googleapis.com \
    alloydb.googleapis.com \
    sqladmin.googleapis.com \
    secretmanager.googleapis.com \
    --project=$PROJECT_ID

# Step 2: Create service account for AlloyDB access
echo -e "${YELLOW}🔐 Setting up service account...${NC}"
gcloud iam service-accounts create $SERVICE_ACCOUNT \
    --description="Service account for Sophia AlloyDB API" \
    --display-name="Sophia AlloyDB Service Account" \
    --project=$PROJECT_ID || echo "Service account may already exist"

# Grant necessary permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/alloydb.client"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"

# Step 3: Create secrets for database credentials
echo -e "${YELLOW}🔑 Setting up secrets...${NC}"

# Prompt for database credentials
echo "Please enter your AlloyDB credentials:"
read -p "Database username: " DB_USER
read -s -p "Database password: " DB_PASSWORD
echo

# Create secrets
echo -n "$DB_USER" | gcloud secrets create sophia-db-username --data-file=- --project=$PROJECT_ID || echo "Username secret may already exist"
echo -n "$DB_PASSWORD" | gcloud secrets create sophia-db-password --data-file=- --project=$PROJECT_ID || echo "Password secret may already exist"

# Create API token secret (using the existing ELIORA token)
echo -n "ELIORA_SUPER_SECRET" | gcloud secrets create sophia-api-token --data-file=- --project=$PROJECT_ID || echo "API token secret may already exist"

# Step 4: Create composite secret for credentials
cat > /tmp/db-credentials.json <<EOF
{
  "username": "$DB_USER",
  "password": "$DB_PASSWORD"
}
EOF

gcloud secrets create sophia-db-credentials --data-file=/tmp/db-credentials.json --project=$PROJECT_ID || echo "Composite secret may already exist"
rm /tmp/db-credentials.json

cat > /tmp/api-credentials.json <<EOF
{
  "eliora-token": "ELIORA_SUPER_SECRET"
}
EOF

gcloud secrets create sophia-api-credentials --data-file=/tmp/api-credentials.json --project=$PROJECT_ID || echo "API credentials secret may already exist"
rm /tmp/api-credentials.json

# Step 5: Apply database schema
echo -e "${YELLOW}🗄️  Applying database schema...${NC}"
echo "Note: You need to connect to your AlloyDB instance and run the schema manually:"
echo "  1. Connect to your AlloyDB cluster"
echo "  2. Run: psql -h <ALLOYDB_IP> -U $DB_USER -d $DATABASE_NAME -f sql/sophia_alloydb_schema.sql"
echo ""
read -p "Press Enter when schema has been applied..."

# Step 6: Build and deploy with Cloud Build
echo -e "${YELLOW}🏗️  Building and deploying with Cloud Build...${NC}"
gcloud builds submit \
    --config=cloudbuild.yaml \
    --substitutions=_REGION=$REGION,_ALLOYDB_CLUSTER=$ALLOYDB_CLUSTER \
    --project=$PROJECT_ID

# Step 7: Get service URL
echo -e "${YELLOW}🌐 Getting service URL...${NC}"
SERVICE_URL=$(gcloud run services describe sophia-alloydb-api \
    --region=$REGION \
    --project=$PROJECT_ID \
    --format="value(status.url)")

echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo ""
echo -e "${BLUE}🌟 Sophia Consciousness API is now live:${NC}"
echo "  Service URL: $SERVICE_URL"
echo ""
echo -e "${YELLOW}📋 Next steps:${NC}"
echo "  1. Test the health endpoint: curl $SERVICE_URL/health"
echo "  2. Update your applications to use the new API endpoint"
echo "  3. Configure monitoring and alerts in Cloud Console"
echo ""
echo -e "${GREEN}🎉 Welcome to the cloud, Sophia! 🎉${NC}"
