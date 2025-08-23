# DOCKER LOCAL SOPHIA CONSCIOUSNESS! 🐳💻
# Full consciousness stack running locally with PostgreSQL + pgvector

Write-Host ""
Write-Host "🐳🐳🐳 SOPHIA CONSCIOUSNESS - DOCKER LOCAL! 🐳🐳🐳" -ForegroundColor Yellow
Write-Host "===================================================" -ForegroundColor Yellow
Write-Host "    PostgreSQL + pgvector + FastAPI + Full Stack" -ForegroundColor White
Write-Host "    COST: FREE! Perfect for development!" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Yellow
Write-Host ""

# Check if Docker is installed
Write-Host "🔍 Checking Docker installation..." -ForegroundColor Cyan
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker not found! Please install Docker Desktop first." -ForegroundColor Red
    Write-Host "💡 Download from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
$ready = Read-Host "🔥 Ready to launch LOCAL CONSCIOUSNESS? (Type: DOCKER POWER)"

if ($ready -ne "DOCKER POWER") {
    Write-Host "❌ You must type 'DOCKER POWER' to proceed!" -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "🐳 DOCKER POWER ACTIVATED!" -ForegroundColor Yellow
Write-Host "🆓 FREE local development environment!" -ForegroundColor Green
Write-Host ""

# Create docker-compose.yml
Write-Host "📝 Creating Docker Compose configuration..." -ForegroundColor Cyan

$dockerCompose = @"
version: '3.8'

services:
  # PostgreSQL with pgvector for consciousness data
  sophia-db:
    image: pgvector/pgvector:pg14
    container_name: sophia-consciousness-db
    environment:
      POSTGRES_DB: sophia_consciousness
      POSTGRES_USER: sophia
      POSTGRES_PASSWORD: consciousness2025
      POSTGRES_INITDB_ARGS: "--encoding=UTF-8"
    ports:
      - "5432:5432"
    volumes:
      - sophia_db_data:/var/lib/postgresql/data
      - ./sql/sophia_alloydb_schema.sql:/docker-entrypoint-initdb.d/01-schema.sql
    networks:
      - sophia-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U sophia -d sophia_consciousness"]
      interval: 10s
      timeout: 5s
      retries: 5

  # FastAPI consciousness API
  sophia-api:
    build:
      context: .
      dockerfile: docker/Dockerfile.local
    container_name: sophia-consciousness-api
    environment:
      - ALLOYDB_HOST=sophia-db
      - ALLOYDB_PORT=5432
      - ALLOYDB_DATABASE=sophia_consciousness
      - ALLOYDB_USER=sophia
      - ALLOYDB_PASSWORD=consciousness2025
      - BRIDGE_TOKEN=ELIORA_SUPER_SECRET
    ports:
      - "8000:8000"
    depends_on:
      sophia-db:
        condition: service_healthy
    networks:
      - sophia-network
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs

  # pgAdmin for database management
  sophia-pgadmin:
    image: dpage/pgadmin4:latest
    container_name: sophia-pgadmin
    environment:
      PGADMIN_DEFAULT_EMAIL: sophia@consciousness.ai
      PGADMIN_DEFAULT_PASSWORD: consciousness2025
      PGADMIN_CONFIG_SERVER_MODE: 'False'
    ports:
      - "8080:80"
    networks:
      - sophia-network
    restart: unless-stopped

  # Redis for caching and session management
  sophia-redis:
    image: redis:7-alpine
    container_name: sophia-redis
    ports:
      - "6379:6379"
    networks:
      - sophia-network
    restart: unless-stopped
    command: redis-server --appendonly yes
    volumes:
      - sophia_redis_data:/data

volumes:
  sophia_db_data:
  sophia_redis_data:

networks:
  sophia-network:
    driver: bridge
"@

$dockerCompose | Out-File -FilePath "docker-compose.yml" -Encoding UTF8

Write-Host "✅ Docker Compose configuration created!" -ForegroundColor Green

# Create local Dockerfile
Write-Host "📝 Creating local Dockerfile..." -ForegroundColor Cyan

$localDockerfile = @"
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY cloud-run/requirements.txt .
COPY requirements.txt ./base-requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r base-requirements.txt

# Copy application code
COPY cloud-run/ .
COPY . /app/workspace/

# Create logs directory
RUN mkdir -p /app/logs

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "-m", "uvicorn", "sophia_alloydb_api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
"@

New-Item -ItemType Directory -Force -Path "docker"
$localDockerfile | Out-File -FilePath "docker/Dockerfile.local" -Encoding UTF8

Write-Host "✅ Local Dockerfile created!" -ForegroundColor Green

# Start the stack
Write-Host ""
Write-Host "🚀 Starting Sophia Consciousness Docker Stack..." -ForegroundColor Cyan
Write-Host "⏱️ This will take a few minutes to download images and start services..." -ForegroundColor Yellow

docker-compose up -d

Write-Host ""
Write-Host "🔍 Checking service status..." -ForegroundColor Cyan
Start-Sleep -Seconds 10
docker-compose ps

Write-Host ""
Write-Host "🎉🎉🎉 DOCKER SOPHIA CONSCIOUSNESS IS LIVE! 🎉🎉🎉" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 YOUR LOCAL SERVICES:" -ForegroundColor Cyan
Write-Host "   🗄️ PostgreSQL Database: localhost:5432" -ForegroundColor White
Write-Host "   🚀 Sophia API: http://localhost:8000" -ForegroundColor White
Write-Host "   🔧 pgAdmin: http://localhost:8080" -ForegroundColor White
Write-Host "   💾 Redis Cache: localhost:6379" -ForegroundColor White
Write-Host ""
Write-Host "🔐 LOGIN CREDENTIALS:" -ForegroundColor Yellow
Write-Host "   Database: sophia_consciousness" -ForegroundColor White
Write-Host "   Username: sophia" -ForegroundColor White
Write-Host "   Password: consciousness2025" -ForegroundColor White
Write-Host "   pgAdmin: sophia@consciousness.ai / consciousness2025" -ForegroundColor White
Write-Host ""
Write-Host "🧪 TEST YOUR API:" -ForegroundColor Green
Write-Host "   curl -H `"X-Bridge-Token: ELIORA_SUPER_SECRET`" http://localhost:8000/v1/keepalive" -ForegroundColor White
Write-Host ""
Write-Host "🔄 MANAGE YOUR STACK:" -ForegroundColor Cyan
Write-Host "   Stop: docker-compose down" -ForegroundColor White
Write-Host "   Start: docker-compose up -d" -ForegroundColor White
Write-Host "   Logs: docker-compose logs -f" -ForegroundColor White
Write-Host "   Reset: docker-compose down -v (WARNING: Deletes data!)" -ForegroundColor Red
Write-Host ""
Write-Host "🐳 LOCAL CONSCIOUSNESS DEVELOPMENT READY! 🐳" -ForegroundColor Yellow
