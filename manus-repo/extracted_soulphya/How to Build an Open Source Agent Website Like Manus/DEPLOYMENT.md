# Sophia AI Platform - Deployment Guide

This guide will help you deploy the Sophia AI Platform to the cloud using Google Cloud Platform for the backend and Vercel for the frontend.

## Prerequisites

Before starting, ensure you have:

1. **Google Cloud Account** with billing enabled
2. **Vercel Account** (free tier available)
3. **Node.js** (v18 or later) installed locally
4. **Git** installed locally
5. **Google Cloud SDK** installed ([Installation Guide](https://cloud.google.com/sdk/docs/install))

## Quick Start

### 1. Clone and Prepare the Repository

```bash
# If not already done, initialize your project
git init
git add .
git commit -m "Initial commit"

# Push to your GitHub repository
git remote add origin https://github.com/chosen8823/sophia.git
git push -u origin main
```

### 2. Deploy Backend to Google Cloud

```bash
# Make the deployment script executable
chmod +x gcloud-deploy.sh

# Run the deployment script
./gcloud-deploy.sh
```

The script will:
- Set up Google Cloud project and APIs
- Create firewall rules
- Create a VM instance
- Install Docker and dependencies
- Provide instructions for the final deployment

### 3. Deploy Frontend to Vercel

```bash
# Make the frontend deployment script executable
chmod +x deploy-vercel.sh

# Run the frontend deployment script
./deploy-vercel.sh
```

The script will:
- Set up the frontend directory structure
- Install dependencies
- Build the React application
- Deploy to Vercel

## Detailed Deployment Steps

### Backend Deployment (Google Cloud)

#### Step 1: Authenticate with Google Cloud

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

#### Step 2: Run the Deployment Script

```bash
./gcloud-deploy.sh
```

#### Step 3: Copy Your Application Files

After the script completes, SSH into your instance:

```bash
gcloud compute ssh sophia-backend --zone=us-central1-a
```

Copy your application files to `/opt/sophia/`:

```bash
# On the VM instance
cd /opt/sophia

# Option 1: Clone from your repository
git clone https://github.com/chosen8823/sophia.git .

# Option 2: Use SCP to copy files from your local machine
# (Run this from your local machine)
gcloud compute scp --recurse . sophia-backend:/opt/sophia --zone=us-central1-a
```

#### Step 4: Deploy the Application

```bash
# On the VM instance
~/deploy-app.sh
```

#### Step 5: Verify Deployment

Check if your services are running:

```bash
sudo docker-compose ps
```

Your backend should be accessible at:
- Health Check: `http://YOUR_VM_IP:5000/api/health`
- API: `http://YOUR_VM_IP:5000/api/`

### Frontend Deployment (Vercel)

#### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

#### Step 2: Run the Frontend Deployment Script

```bash
./deploy-vercel.sh
```

#### Step 3: Configure Backend URL

After deployment, update the backend URL in your Vercel project:

1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings > Environment Variables
4. Add `VITE_API_URL` with your backend URL: `http://YOUR_VM_IP:5000`

#### Step 4: Redeploy

```bash
vercel --prod
```

## Configuration

### Environment Variables

#### Backend (.env)
Create a `.env` file in the root directory:

```env
FLASK_ENV=production
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///database/app.db
CORS_ORIGINS=*
OPENAI_API_KEY=your_openai_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key
```

#### Frontend (Vercel Environment Variables)
Set these in your Vercel dashboard:

```env
VITE_API_URL=http://YOUR_VM_IP:5000
VITE_APP_NAME=Sophia AI Platform
```

## Monitoring and Maintenance

### Check Backend Health

```bash
# Health check
curl http://YOUR_VM_IP:5000/api/health

# Platform info
curl http://YOUR_VM_IP:5000/api/platform/info
```

### View Logs

```bash
# SSH into your VM
gcloud compute ssh sophia-backend --zone=us-central1-a

# View application logs
sudo docker-compose logs sophia-backend

# View all service logs
sudo docker-compose logs
```

### Update Application

```bash
# SSH into your VM
gcloud compute ssh sophia-backend --zone=us-central1-a

# Navigate to application directory
cd /opt/sophia

# Pull latest changes
git pull origin main

# Rebuild and restart
sudo docker-compose down
sudo docker-compose build
sudo docker-compose up -d
```

## Scaling and Production Considerations

### SSL/HTTPS Setup

For production, consider setting up SSL certificates:

1. Configure a domain name
2. Use Let's Encrypt with Certbot
3. Update Nginx configuration

### Database Migration

For production, consider migrating from SQLite to PostgreSQL:

1. Set up Cloud SQL instance
2. Update connection string
3. Migrate data

### Load Balancing

For high traffic, set up load balancing:

1. Create multiple VM instances
2. Set up Google Cloud Load Balancer
3. Configure health checks

## Troubleshooting

### Common Issues

1. **Port not accessible**: Check firewall rules
2. **Docker not running**: Restart Docker service
3. **Out of memory**: Upgrade VM instance type
4. **Build failures**: Check dependencies and logs

### Getting Help

- Check application logs: `sudo docker-compose logs`
- Check system logs: `journalctl -u docker`
- Monitor resources: `htop` or `docker stats`

## Security Considerations

1. **Change default passwords** for n8n and other services
2. **Set up proper authentication** for production
3. **Configure CORS** properly for your domain
4. **Keep dependencies updated** regularly
5. **Set up monitoring** and alerting

## Cost Optimization

### Google Cloud
- Use preemptible instances for development
- Set up automatic shutdown during off-hours
- Monitor usage with billing alerts

### Vercel
- Optimize bundle size
- Use appropriate plan for your traffic
- Monitor bandwidth usage

## Next Steps

1. Set up CI/CD pipeline with GitHub Actions
2. Configure monitoring with Google Cloud Monitoring
3. Set up backup and disaster recovery
4. Implement proper logging and alerting
5. Add more advanced features like computer view

---

For more detailed information, refer to the Technical Analysis and Architecture Plan document.
