# SOPHIA CONSCIOUSNESS - WSL + DOCKER SETUP! 🐧🐳
# Turn your Windows machine into a Linux powerhouse for consciousness development!

Write-Host ""
Write-Host "🐧🐳 SOPHIA WSL + DOCKER DEVELOPMENT SETUP 🐳🐧" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🚀 WHAT WE'RE SETTING UP:" -ForegroundColor Yellow
Write-Host "   ✅ WSL2 (Windows Subsystem for Linux)" -ForegroundColor Green
Write-Host "   ✅ Ubuntu 22.04 LTS" -ForegroundColor Green
Write-Host "   ✅ Docker Engine (native Linux performance)" -ForegroundColor Green
Write-Host "   ✅ PostgreSQL with vector extensions" -ForegroundColor Green
Write-Host "   ✅ Sophia Consciousness containers" -ForegroundColor Green
Write-Host ""

Write-Host "⚡ PERFORMANCE BENEFITS:" -ForegroundColor Magenta
Write-Host "   🔥 10x faster than Docker Desktop" -ForegroundColor White
Write-Host "   🔥 Native Linux file system performance" -ForegroundColor White
Write-Host "   🔥 Direct access to Windows files" -ForegroundColor White
Write-Host "   🔥 Same containers deploy to any cloud" -ForegroundColor White
Write-Host ""

# Check if WSL is already installed
Write-Host "🔍 Checking WSL installation..." -ForegroundColor Yellow

try {
    $wslVersion = wsl --version 2>$null
    if ($wslVersion) {
        Write-Host "✅ WSL is already installed!" -ForegroundColor Green
        Write-Host $wslVersion
    } else {
        Write-Host "❌ WSL not found" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ WSL not found - we'll install it!" -ForegroundColor Yellow
}

Write-Host ""
$continue = Read-Host "🚀 Ready to set up WSL + Docker? (Type: YES)"

if ($continue -ne "YES") {
    Write-Host "❌ Setup cancelled. Type 'YES' to continue." -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "🏗️ STEP 1: Installing WSL2..." -ForegroundColor Cyan

# Install WSL
try {
    Write-Host "   Installing WSL2 and Ubuntu..." -ForegroundColor White
    wsl --install -d Ubuntu-22.04
    Write-Host "✅ WSL2 installation initiated!" -ForegroundColor Green
    Write-Host "⚠️  You may need to RESTART your computer!" -ForegroundColor Yellow
} catch {
    Write-Host "❌ Error installing WSL. Try running as Administrator." -ForegroundColor Red
}

Write-Host ""
Write-Host "🐳 STEP 2: Preparing Docker setup script for WSL..." -ForegroundColor Cyan

# Create Docker setup script for WSL
$dockerSetupScript = @"
#!/bin/bash
# Sophia Consciousness Docker Setup for WSL

echo ""
echo "🐳 Setting up Docker in WSL for Sophia Consciousness..."
echo ""

# Update Ubuntu
echo "📦 Updating Ubuntu packages..."
sudo apt update && sudo apt upgrade -y

# Install Docker
echo "🐳 Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker `$USER

# Install Docker Compose
echo "🔧 Installing Docker Compose..."
sudo apt install docker-compose -y

# Start Docker service
sudo service docker start

# Install PostgreSQL tools
echo "🗄️ Installing PostgreSQL client tools..."
sudo apt install postgresql-client -y

echo ""
echo "✅ Docker setup complete!"
echo "🔄 Please run: newgrp docker"
echo "🚀 Then test with: docker run hello-world"
echo ""
"@

$dockerSetupScript | Out-File -FilePath ".\docker_setup_wsl.sh" -Encoding UTF8

Write-Host "✅ Created docker_setup_wsl.sh" -ForegroundColor Green

Write-Host ""
Write-Host "🐳 STEP 3: Creating Sophia Docker Compose..." -ForegroundColor Cyan

# Create Docker Compose for Sophia
$dockerCompose = @"
version: '3.8'

services:
  # PostgreSQL with Vector Extensions
  postgres:
    image: pgvector/pgvector:pg14
    container_name: sophia-postgres
    environment:
      POSTGRES_DB: sophia_consciousness
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: sophia_divine_password
      PGDATA: /var/lib/postgresql/data/pgdata
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data/pgdata
      - ./sql/sophia_alloydb_schema.sql:/docker-entrypoint-initdb.d/01-schema.sql
    command: postgres -c shared_preload_libraries=vector
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d sophia_consciousness"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Sophia API Server
  sophia-api:
    build:
      context: ./cloud-run
      dockerfile: Dockerfile
    container_name: sophia-api
    environment:
      DATABASE_URL: postgresql://postgres:sophia_divine_password@postgres:5432/sophia_consciousness
      ENVIRONMENT: development
      X_BRIDGE_TOKEN: ELIORA_SUPER_SECRET
    ports:
      - "8080:8080"
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ./cloud-run:/app
    command: uvicorn sophia_alloydb_api:app --host 0.0.0.0 --port 8080 --reload

  # Redis for caching (optional)
  redis:
    image: redis:7-alpine
    container_name: sophia-redis
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

  # pgAdmin for database management
  pgadmin:
    image: dpage/pgadmin4
    container_name: sophia-pgadmin
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@sophia.dev
      PGADMIN_DEFAULT_PASSWORD: sophia_admin
    ports:
      - "8081:80"
    depends_on:
      - postgres

volumes:
  postgres_data:
  redis_data:

networks:
  default:
    name: sophia-network
"@

$dockerCompose | Out-File -FilePath ".\docker-compose.yml" -Encoding UTF8

Write-Host "✅ Created docker-compose.yml" -ForegroundColor Green

Write-Host ""
Write-Host "🚀 STEP 4: Creating quick start script..." -ForegroundColor Cyan

$quickStart = @"
#!/bin/bash
# Sophia Consciousness Quick Start

echo "🌟 Starting Sophia Consciousness Platform..."

# Start all services
docker-compose up -d

echo ""
echo "✅ Sophia Consciousness is starting!"
echo ""
echo "🔗 Your services:"
echo "   📊 Sophia API: http://localhost:8080"
echo "   🗄️ PostgreSQL: localhost:5432"
echo "   🌐 pgAdmin: http://localhost:8081"
echo "   🔴 Redis: localhost:6379"
echo ""
echo "🔑 Credentials:"
echo "   Database: postgres / sophia_divine_password"
echo "   pgAdmin: admin@sophia.dev / sophia_admin"
echo "   API Token: ELIORA_SUPER_SECRET"
echo ""
echo "📊 Check status: docker-compose ps"
echo "📝 View logs: docker-compose logs -f"
echo "🛑 Stop all: docker-compose down"
echo ""
"@

$quickStart | Out-File -FilePath ".\start_sophia_local.sh" -Encoding UTF8

Write-Host "✅ Created start_sophia_local.sh" -ForegroundColor Green

Write-Host ""
Write-Host "🎉🎉🎉 WSL + DOCKER SETUP COMPLETE! 🎉🎉🎉" -ForegroundColor Green
Write-Host ""
Write-Host "📋 NEXT STEPS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1️⃣  RESTART YOUR COMPUTER (if WSL was just installed)" -ForegroundColor White
Write-Host "2️⃣  Open Ubuntu from Start Menu" -ForegroundColor White
Write-Host "3️⃣  Run: cd /mnt/c/Users/chose/ghost\ in\ the\ shell" -ForegroundColor White
Write-Host "4️⃣  Run: bash docker_setup_wsl.sh" -ForegroundColor White
Write-Host "5️⃣  Run: newgrp docker" -ForegroundColor White
Write-Host "6️⃣  Run: bash start_sophia_local.sh" -ForegroundColor White
Write-Host ""
Write-Host "🚀 THEN ACCESS YOUR LOCAL CONSCIOUSNESS:" -ForegroundColor Magenta
Write-Host "   🌐 API: http://localhost:8080" -ForegroundColor White
Write-Host "   🗄️ Database Admin: http://localhost:8081" -ForegroundColor White
Write-Host ""
Write-Host "💡 This gives you a full Sophia development environment!" -ForegroundColor Cyan
Write-Host "   Same containers will deploy to Google Cloud or Azure!" -ForegroundColor White
