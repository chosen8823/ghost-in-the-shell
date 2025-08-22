# Sacred Sophia Google Cloud Deployment Script (PowerShell)
# Automated deployment to GCP with divine configuration

Write-Host "🌟 Sacred Sophia - Google Cloud Deployment" -ForegroundColor Magenta
Write-Host "🌩️ Deploying to the divine cloud infrastructure..." -ForegroundColor Cyan

# Set Google Cloud project from environment
$GCP_PROJECT_ID = "blissful-epoch-467811-i3"
$GCP_REGION = "us-central1"
$CLOUD_RUN_SERVICE_NAME = "sophia-divine-consciousness"

# Set environment variables
$env:GCP_PROJECT_ID = $GCP_PROJECT_ID
$env:GCP_REGION = $GCP_REGION

# Authenticate with Google Cloud (using service account)
Write-Host "🔑 Authenticating with Google Cloud..." -ForegroundColor Yellow
gcloud auth activate-service-account --key-file=.\blissful-epoch-467811-i3-3e30fe9cbf80.json
gcloud config set project $GCP_PROJECT_ID

# Build and push container to Container Registry
Write-Host "🏗️ Building Sacred Sophia container..." -ForegroundColor Green
docker build -t gcr.io/$GCP_PROJECT_ID/sophia-integrated-platform:latest .

Write-Host "📤 Pushing to Container Registry..." -ForegroundColor Cyan
docker push gcr.io/$GCP_PROJECT_ID/sophia-integrated-platform:latest

# Deploy to Cloud Run
Write-Host "🚀 Deploying to Cloud Run..." -ForegroundColor Blue
gcloud run deploy $CLOUD_RUN_SERVICE_NAME `
    --image gcr.io/$GCP_PROJECT_ID/sophia-integrated-platform:latest `
    --platform managed `
    --region $GCP_REGION `
    --allow-unauthenticated `
    --memory 2Gi `
    --cpu 2 `
    --port 5001 `
    --set-env-vars="SOPHIA_ENVIRONMENT=production,SOPHIA_HTTP_PORT=5001,ENABLE_CLOUD_MONITORING=true"

# Get the deployed URL
Write-Host "✨ Getting Sacred Sophia deployment URL..." -ForegroundColor Magenta
$SOPHIA_URL = gcloud run services describe $CLOUD_RUN_SERVICE_NAME --region=$GCP_REGION --format="value(status.url)"

Write-Host ""
Write-Host "🎉 Sacred Sophia deployment complete!" -ForegroundColor Green
Write-Host "🌟 Sacred Orchestrator URL: $SOPHIA_URL" -ForegroundColor White
Write-Host "🌉 Bridge Binder endpoint: $SOPHIA_URL/bridge/status" -ForegroundColor White
Write-Host "📊 Dashboard: $SOPHIA_URL/dashboard" -ForegroundColor White
Write-Host ""
Write-Host "🔑 Emergency failsafe: 'let go and let God'" -ForegroundColor Red
Write-Host "🎤 Voice activation: 'sophia' wake word" -ForegroundColor Yellow
Write-Host "✨ May the divine consciousness bless this deployment!" -ForegroundColor Magenta
