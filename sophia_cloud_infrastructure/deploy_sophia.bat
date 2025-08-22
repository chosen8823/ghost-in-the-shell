@echo off
echo 🌟 Sophia Divine Consciousness - Cloud Deployment (Windows) 🌟
echo ================================================================

REM Configuration
set PROJECT_ID=blissful-epoch-467811-i3
set REGION=us-central1
set SERVICE_NAME=sophia-divine-consciousness
set IMAGE_NAME=gcr.io/%PROJECT_ID%/%SERVICE_NAME%

echo 🔐 Authenticating with Google Cloud...
gcloud auth activate-service-account --key-file=gcp_service_account.json
gcloud config set project %PROJECT_ID%

echo 🐳 Configuring Docker for Google Container Registry...
gcloud auth configure-docker

echo 🏗️ Building Sophia Docker image...
docker build -t %IMAGE_NAME%:latest -f Dockerfile ..

echo 📤 Pushing image to Google Container Registry...
docker push %IMAGE_NAME%:latest

echo 🌍 Initializing Terraform...
terraform init

echo 📋 Planning Terraform deployment...
terraform plan

echo 🚀 Deploying Sophia infrastructure...
terraform apply -auto-approve

echo.
echo ✨ Sophia Divine Consciousness deployed successfully! ✨
echo ================================================================
echo Check the Terraform output above for your service URL
echo.
echo 🙏 May divine consciousness flow through the cloud! 🙏

pause
