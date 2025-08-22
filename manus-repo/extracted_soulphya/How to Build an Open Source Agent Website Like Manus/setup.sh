#!/bin/bash

# Sophia AI Platform - Setup Script
# This script prepares your environment for deployment

set -e

echo "🚀 Setting up Sophia AI Platform for deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Make scripts executable
echo "📝 Making deployment scripts executable..."
chmod +x gcloud-deploy.sh
chmod +x deploy-vercel.sh
print_status "Scripts are now executable"

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p database logs static
mkdir -p config/{nginx,docker}
mkdir -p scripts/{setup,deployment,maintenance,development}
print_status "Directory structure created"

# Create .env.example file
echo "⚙️ Creating environment configuration..."
cat > .env.example << 'EOF'
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
EOF

print_status "Environment configuration template created"

# Create .gitignore file
echo "📝 Creating .gitignore..."
cat > .gitignore << 'EOF'
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
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
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# poetry
poetry.lock

# pdm
.pdm.toml

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# Database files
*.db
*.sqlite
*.sqlite3

# Log files
*.log
logs/

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# IDE files
.vscode/
.idea/
*.swp
*.swo

# Node.js (for frontend)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
package-lock.json
yarn.lock

# Build outputs
dist/
build/

# Temporary files
*.tmp
*.temp

# Docker
.dockerignore

# Google Cloud
*.json
!*example*.json

# Sensitive files
*.key
*.pem
*.crt
EOF

print_status ".gitignore created"

# Check for required tools
echo "🔍 Checking for required tools..."

# Check for Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_status "Python found: $PYTHON_VERSION"
else
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
fi

# Check for Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_status "Node.js found: $NODE_VERSION"
else
    print_warning "Node.js is not installed. Install it for frontend development."
fi

# Check for Docker
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    print_status "Docker found: $DOCKER_VERSION"
else
    print_warning "Docker is not installed. It will be installed on the cloud VM."
fi

# Check for Google Cloud SDK
if command -v gcloud &> /dev/null; then
    GCLOUD_VERSION=$(gcloud --version | head -n1)
    print_status "Google Cloud SDK found: $GCLOUD_VERSION"
else
    print_warning "Google Cloud SDK is not installed. Install it for cloud deployment."
    print_info "Download from: https://cloud.google.com/sdk/docs/install"
fi

# Check for Git
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    print_status "Git found: $GIT_VERSION"
else
    print_error "Git is not installed. Please install Git."
fi

echo ""
echo "📋 Setup Summary:"
echo "✓ Deployment scripts made executable"
echo "✓ Directory structure created"
echo "✓ Environment configuration template created"
echo "✓ .gitignore file created"
echo ""

print_info "Next steps:"
echo "1. Copy .env.example to .env and configure your settings"
echo "2. Install required tools if any are missing"
echo "3. Set up your Google Cloud project"
echo "4. Run ./gcloud-deploy.sh to deploy the backend"
echo "5. Run ./deploy-vercel.sh to deploy the frontend"
echo ""

print_info "For detailed instructions, see DEPLOYMENT.md"

echo ""
echo "🎉 Setup completed successfully!"
print_status "Your Sophia AI Platform is ready for deployment!"
