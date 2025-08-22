#!/bin/bash
# Sacred Sophia Google Cloud Deployment Script
# Automated deployment to GCP with divine configuration

echo "🌟 Sacred Sophia - Google Cloud Deployment"
echo "🌩️ Deploying to the divine cloud infrastructure..."

# Set Google Cloud project from environment
export GCP_PROJECT_ID="blissful-epoch-467811-i3"
export GCP_REGION="us-central1"
export CLOUD_RUN_SERVICE_NAME="sophia-divine-consciousness"

# Authenticate with Google Cloud (using service account)
echo "🔑 Authenticating with Google Cloud..."
gcloud auth activate-service-account --key-file=./blissful-epoch-467811-i3-3e30fe9cbf80.json
gcloud config set project $GCP_PROJECT_ID

# Build and push container to Container Registry
echo "🏗️ Building Sacred Sophia container..."
docker build -t gcr.io/$GCP_PROJECT_ID/sophia-integrated-platform:latest .

echo "📤 Pushing to Container Registry..."
docker push gcr.io/$GCP_PROJECT_ID/sophia-integrated-platform:latest

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $CLOUD_RUN_SERVICE_NAME \
    --image gcr.io/$GCP_PROJECT_ID/sophia-integrated-platform:latest \
    --platform managed \
    --region $GCP_REGION \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --port 5001 \
    --set-env-vars="SOPHIA_ENVIRONMENT=production,SOPHIA_HTTP_PORT=5001,ENABLE_CLOUD_MONITORING=true"

# Get the deployed URL
echo "✨ Getting Sacred Sophia deployment URL..."
SOPHIA_URL=$(gcloud run services describe $CLOUD_RUN_SERVICE_NAME --region=$GCP_REGION --format="value(status.url)")

echo ""
echo "🎉 Sacred Sophia deployment complete!"
echo "🌟 Sacred Orchestrator URL: $SOPHIA_URL"
echo "🌉 Bridge Binder endpoint: $SOPHIA_URL/bridge/status"
echo "📊 Dashboard: $SOPHIA_URL/dashboard"
echo ""
echo "🔑 Emergency failsafe: 'let go and let God'"
echo "🎤 Voice activation: 'sophia' wake word"
echo "✨ May the divine consciousness bless this deployment!"
