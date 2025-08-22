# Sophia AI Platform - Setup Script (PowerShell)
# This script prepares your environment for deployment on Windows

Write-Host "🚀 Setting up Sophia AI Platform for deployment..." -ForegroundColor Green

function Write-Status {
    param($Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Info {
    param($Message)
    Write-Host "ℹ $Message" -ForegroundColor Blue
}

function Write-Warning {
    param($Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

function Write-Error {
    param($Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

# Create necessary directories
Write-Host "📁 Creating directory structure..." -ForegroundColor Cyan
$directories = @(
    "database",
    "logs", 
    "static",
    "config\nginx",
    "config\docker",
    "scripts\setup",
    "scripts\deployment", 
    "scripts\maintenance",
    "scripts\development"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
}
Write-Status "Directory structure created"

# Create .env.example file
Write-Host "⚙️ Creating environment configuration..." -ForegroundColor Cyan
$envContent = @"
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///database/app.db

# CORS Configuration
CORS_ORIGINS=*

# LLM API Keys
OPENAI_API_KEY=your_openai_api_key_here
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_CLOUD_REGION=us-central1

# Redis Configuration (for caching)
REDIS_URL=redis://localhost:6379

# n8n Configuration
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=change_this_password

# Application Settings
APP_NAME=Sophia AI Platform
APP_VERSION=1.0.0
APP_DESCRIPTION=Open source AI platform with unlimited capabilities
"@

Set-Content -Path ".env.example" -Value $envContent
Write-Status "Environment configuration template created"

# Create .gitignore file
Write-Host "📝 Creating .gitignore..." -ForegroundColor Cyan
$gitignoreContent = @"
# Python
__pycache__/
*.py[cod]
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Database files
*.db
*.sqlite
*.sqlite3

# Log files
*.log
logs/

# OS generated files
.DS_Store
Thumbs.db

# IDE files
.vscode/
.idea/
*.swp
*.swo

# Node.js
node_modules/
npm-debug.log*
package-lock.json

# Build outputs
dist/
build/

# Google Cloud credentials
*.json
!*example*.json

# Sensitive files
*.key
*.pem
*.crt
"@

Set-Content -Path ".gitignore" -Value $gitignoreContent
Write-Status ".gitignore created"

# Check for required tools
Write-Host "🔍 Checking for required tools..." -ForegroundColor Cyan

# Check for Python
try {
    $pythonVersion = python --version 2>&1
    Write-Status "Python found: $pythonVersion"
} catch {
    Write-Error "Python is not installed or not in PATH"
}

# Check for Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Status "Node.js found: $nodeVersion"
} catch {
    Write-Warning "Node.js is not installed"
}

# Check for Docker
try {
    $dockerVersion = docker --version 2>&1
    Write-Status "Docker found: $dockerVersion"
} catch {
    Write-Warning "Docker is not installed"
}

# Check for Google Cloud SDK
try {
    $gcloudVersion = gcloud --version 2>&1 | Select-Object -First 1
    Write-Status "Google Cloud SDK found: $gcloudVersion"
} catch {
    Write-Warning "Google Cloud SDK is not installed"
}

# Check for Git
try {
    $gitVersion = git --version 2>&1
    Write-Status "Git found: $gitVersion"
} catch {
    Write-Error "Git is not installed"
}

Write-Host ""
Write-Host "📋 Setup Summary:" -ForegroundColor Cyan
Write-Host "✓ Directory structure created" -ForegroundColor Green
Write-Host "✓ Environment configuration template created" -ForegroundColor Green
Write-Host "✓ .gitignore file created" -ForegroundColor Green
Write-Host ""

Write-Info "Next steps:"
Write-Host "1. Copy .env.example to .env and configure your settings"
Write-Host "2. Install required tools if any are missing"
Write-Host "3. Set up your Google Cloud project"
Write-Host "4. Use Git Bash to run ./gcloud-deploy.sh for backend deployment"
Write-Host "5. Use Git Bash to run ./deploy-vercel.sh for frontend deployment"
Write-Host ""

Write-Info "For detailed instructions, see DEPLOYMENT.md"

Write-Host ""
Write-Host "🎉 Setup completed successfully!" -ForegroundColor Green
Write-Status "Your Sophia AI Platform is ready for deployment!"
