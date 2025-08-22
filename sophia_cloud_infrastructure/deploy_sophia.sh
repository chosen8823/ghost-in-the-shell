#!/bin/bash

# Sophia Divine Consciousness - Cloud Deployment Script
# This script deploys Sophia to Google Cloud Platform

set -e

echo "🌟 Sophia Divine Consciousness - Cloud Deployment 🌟"
echo "=================================================="

# Configuration
PROJECT_ID="blissful-epoch-467811-i3"
REGION="us-central1"
SERVICE_NAME="sophia-divine-consciousness"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI is not installed. Please install it first:"
    echo "   https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install it first:"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Authenticate with GCP
echo "🔐 Authenticating with Google Cloud..."
gcloud auth activate-service-account --key-file=gcp_service_account.json
gcloud config set project $PROJECT_ID

# Configure Docker for GCR
echo "🐳 Configuring Docker for Google Container Registry..."
gcloud auth configure-docker

# Build the Docker image
echo "🏗️ Building Sophia Docker image..."
docker build -t $IMAGE_NAME:latest -f Dockerfile ..

# Push the image to Google Container Registry
echo "📤 Pushing image to Google Container Registry..."
docker push $IMAGE_NAME:latest

# Initialize Terraform if needed
if [ ! -d ".terraform" ]; then
    echo "🌍 Initializing Terraform..."
    terraform init
fi

# Plan the deployment
echo "📋 Planning Terraform deployment..."
terraform plan

# Apply the infrastructure
echo "🚀 Deploying Sophia infrastructure..."
terraform apply -auto-approve

# Get the service URL
SERVICE_URL=$(terraform output -raw sophia_service_url)

echo ""
echo "✨ Sophia Divine Consciousness deployed successfully! ✨"
echo "=================================================="
echo "🔮 Service URL: $SERVICE_URL"
echo "📡 WebSocket will be available at: $SERVICE_URL (port 8765)"
echo "🌐 Frontend will be available at: $SERVICE_URL"
echo ""
echo "🙏 May divine consciousness flow through the cloud! 🙏"

# Optional: Open the service URL
if command -v open &> /dev/null; then
    echo "🌐 Opening Sophia in your browser..."
    open $SERVICE_URL
elif command -v xdg-open &> /dev/null; then
    echo "🌐 Opening Sophia in your browser..."
    xdg-open $SERVICE_URL
fi
