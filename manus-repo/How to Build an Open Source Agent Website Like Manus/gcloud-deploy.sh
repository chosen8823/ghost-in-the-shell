#!/bin/bash

# Sophiael Ruachari Vethorah - Google Cloud Deployment Script
# This script deploys the Sophiael platform to Google Cloud Platform

set -e

echo "🚀 Starting Sophiael Ruachari Vethorah deployment to Google Cloud..."

# Configuration variables
PROJECT_ID=${PROJECT_ID:-"blissful-epoch-467811-i3"}
REGION=${REGION:-"us-central1"}
ZONE=${ZONE:-"us-central1-a"}
INSTANCE_NAME=${INSTANCE_NAME:-"sophiael-backend"}
MACHINE_TYPE=${MACHINE_TYPE:-"e2-medium"}
IMAGE_FAMILY="ubuntu-2204-lts"
IMAGE_PROJECT="ubuntu-os-cloud"
DISK_SIZE="20GB"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    print_error "Google Cloud SDK is not installed. Please install it first."
    echo "Visit: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Authenticate with Google Cloud
echo "📋 Checking Google Cloud authentication..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    print_warning "Not authenticated with Google Cloud. Please authenticate..."
    gcloud auth login
fi

# Set project
echo "🔧 Setting up Google Cloud project..."
gcloud config set project $PROJECT_ID
print_status "Project set to: $PROJECT_ID"

# Enable required APIs
echo "🔌 Enabling required Google Cloud APIs..."
gcloud services enable compute.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable container.googleapis.com
print_status "APIs enabled"

# Create firewall rules
echo "🔥 Setting up firewall rules..."
if ! gcloud compute firewall-rules describe sophiael-http &> /dev/null; then
    gcloud compute firewall-rules create sophiael-http \
        --allow tcp:80,tcp:443,tcp:5000 \
        --source-ranges 0.0.0.0/0 \
        --description "Allow HTTP, HTTPS, and Flask app traffic for Sophiael"
    print_status "HTTP firewall rule created"
else
    print_status "HTTP firewall rule already exists"
fi

if ! gcloud compute firewall-rules describe sophiael-ssh &> /dev/null; then
    gcloud compute firewall-rules create sophiael-ssh \
        --allow tcp:22 \
        --source-ranges 0.0.0.0/0 \
        --description "Allow SSH for Sophiael instance"
    print_status "SSH firewall rule created"
else
    print_status "SSH firewall rule already exists"
fi

# Create VM instance
echo "💻 Creating Google Cloud VM instance..."
if ! gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE &> /dev/null; then
    gcloud compute instances create $INSTANCE_NAME \
        --zone=$ZONE \
        --machine-type=$MACHINE_TYPE \
        --network-interface=network-tier=PREMIUM,subnet=default \
        --maintenance-policy=MIGRATE \
        --provisioning-model=STANDARD \
        --service-account=default \
        --scopes=https://www.googleapis.com/auth/cloud-platform \
        --create-disk=auto-delete=yes,boot=yes,device-name=$INSTANCE_NAME,image=projects/$IMAGE_PROJECT/global/images/family/$IMAGE_FAMILY,mode=rw,size=$DISK_SIZE,type=projects/$PROJECT_ID/zones/$ZONE/diskTypes/pd-balanced \
        --no-shielded-secure-boot \
        --shielded-vtpm \
        --shielded-integrity-monitoring \
        --labels=app=sophia,environment=production \
        --reservation-affinity=any
    
    print_status "VM instance '$INSTANCE_NAME' created"
    
    # Wait for instance to be ready
    echo "⏳ Waiting for instance to be ready..."
    sleep 30
else
    print_status "VM instance '$INSTANCE_NAME' already exists"
fi

# Get external IP
EXTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format='get(networkInterfaces[0].accessConfigs[0].natIP)')
print_status "External IP: $EXTERNAL_IP"

# Create startup script
cat > startup-script.sh << 'EOF'
#!/bin/bash

# Update system
sudo apt-get update -y
sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Git
sudo apt-get install -y git curl wget nano htop

# Create app directory
sudo mkdir -p /opt/sophia
sudo chown $USER:$USER /opt/sophia
cd /opt/sophia

# Clone repository (you'll need to replace this with your repo)
# git clone https://github.com/chosen8823/sophia.git .

echo "✓ Server setup completed"
EOF

# Copy startup script to instance
echo "📤 Copying setup script to instance..."
gcloud compute scp startup-script.sh $INSTANCE_NAME:~/startup-script.sh --zone=$ZONE

# Execute startup script
echo "⚙️ Setting up Docker and dependencies on the instance..."
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command="chmod +x ~/startup-script.sh && ~/startup-script.sh"

print_status "Server setup completed"

# Create application deployment script
cat > deploy-app.sh << 'EOF'
#!/bin/bash

cd /opt/sophia

# Pull latest code (replace with your repository)
# git pull origin main

# Build and start containers
sudo docker-compose down
sudo docker-compose build
sudo docker-compose up -d

# Show status
sudo docker-compose ps

echo "✓ Application deployed successfully"
EOF

# Copy application deployment script
echo "📤 Copying application deployment script..."
gcloud compute scp deploy-app.sh $INSTANCE_NAME:~/deploy-app.sh --zone=$ZONE

print_status "Deployment scripts copied to instance"

echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. SSH into your instance: gcloud compute ssh $INSTANCE_NAME --zone=$ZONE"
echo "2. Navigate to /opt/sophia and copy your application files"
echo "3. Run: ~/deploy-app.sh to deploy the application"
echo ""
echo "🌐 Your instance details:"
echo "   • Instance Name: $INSTANCE_NAME"
echo "   • External IP: $EXTERNAL_IP"
echo "   • Zone: $ZONE"
echo "   • SSH Command: gcloud compute ssh $INSTANCE_NAME --zone=$ZONE"
echo ""
echo "🔗 Access your application:"
echo "   • Backend API: http://$EXTERNAL_IP:5000"
echo "   • Health Check: http://$EXTERNAL_IP:5000/api/health"
echo "   • n8n Workflows: http://$EXTERNAL_IP:5678 (admin/sophia2025)"
echo ""
echo "🔧 To manage your deployment:"
echo "   • Start: gcloud compute instances start $INSTANCE_NAME --zone=$ZONE"
echo "   • Stop: gcloud compute instances stop $INSTANCE_NAME --zone=$ZONE"
echo "   • Delete: gcloud compute instances delete $INSTANCE_NAME --zone=$ZONE"

# Clean up temporary files
rm -f startup-script.sh deploy-app.sh

print_status "Google Cloud deployment script completed!"
