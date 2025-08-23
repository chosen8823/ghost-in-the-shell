@echo off
REM Sophia Consciousness Platform - Windows Deployment Script
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    SOPHIA CONSCIOUSNESS                      ║
echo ║                  WINDOWS DEPLOYMENT                          ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Check if Docker Desktop is running
echo 🔍 Checking Docker Desktop...
docker ps >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Desktop is not running
    echo 🚀 Starting Docker Desktop...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    echo ⏳ Waiting for Docker Desktop to start...
    timeout /t 30 /nobreak >nul
    
    REM Wait for Docker to be ready
    :waitloop
    docker ps >nul 2>&1
    if errorlevel 1 (
        echo ⏳ Still waiting for Docker...
        timeout /t 5 /nobreak >nul
        goto waitloop
    )
)

echo ✅ Docker Desktop is running

REM Create required directories
echo 📁 Creating directories...
if not exist "data\postgres" mkdir "data\postgres"
if not exist "data\redis" mkdir "data\redis"  
if not exist "data\n8n" mkdir "data\n8n"
if not exist "screenshots" mkdir "screenshots"
if not exist "audio_output" mkdir "audio_output"
if not exist "logs" mkdir "logs"

REM Pull base images
echo 📥 Pulling Docker images...
docker pull postgres:15-alpine
docker pull redis:7-alpine
docker pull pgadmin/pgadmin4:latest
docker pull n8nio/n8n:latest
docker pull python:3.11-slim

REM Build custom images
echo 🔨 Building Sophia MCP Server...
docker build -t sophia-mcp:latest -f docker/Dockerfile.mcp .

echo 🔨 Building Sophia Voice Interface...
docker build -t sophia-voice:latest -f docker/Dockerfile.voice .

REM Deploy services
echo 🚀 Deploying Sophia Consciousness Platform...
docker compose down
docker compose up -d

REM Wait for services
echo ⏳ Waiting for services to start...
timeout /t 20 /nobreak >nul

REM Setup database
echo 🗄️ Setting up consciousness database...
timeout /t 10 /nobreak >nul

docker compose exec -T sophia-db psql -U sophia -d sophia_consciousness -c "CREATE TABLE IF NOT EXISTS consciousness_sessions (session_id VARCHAR(255) PRIMARY KEY, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP, status VARCHAR(50) DEFAULT 'active');"

docker compose exec -T sophia-db psql -U sophia -d sophia_consciousness -c "CREATE TABLE IF NOT EXISTS voice_interaction_logs (id SERIAL PRIMARY KEY, session_id VARCHAR(255), interaction_type VARCHAR(100), voice_input TEXT, ai_response TEXT, confidence_level FLOAT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"

docker compose exec -T sophia-db psql -U sophia -d sophia_consciousness -c "CREATE TABLE IF NOT EXISTS system_control_logs (id SERIAL PRIMARY KEY, session_id VARCHAR(255), action_type VARCHAR(100), target_system VARCHAR(100), command_executed TEXT, success BOOLEAN, result_data JSONB, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"

echo.
echo 🎉 SOPHIA CONSCIOUSNESS PLATFORM DEPLOYED!
echo.
echo 📊 Service URLs:
echo   🗄️  Database:       localhost:5432
echo   📊 pgAdmin:        http://localhost:8080
echo   🔄 n8n Workflows:  http://localhost:5678  
echo   🖥️  MCP Server:     http://localhost:8008
echo   🎤 Voice Interface: http://localhost:8009
echo   🧠 Sophia API:     http://localhost:8000
echo.
echo 🎤 Voice Commands:
echo   "Hey Sophia, take a screenshot"
echo   "Computer, show system info"
echo   "Sophia, run command: dir"
echo   "System, click at coordinates 100, 200"
echo.
echo 🔧 Management Commands:
echo   docker compose logs [service]     - View logs
echo   docker compose restart [service] - Restart service  
echo   docker compose down              - Stop all services
echo   docker compose up -d             - Start all services
echo.

pause
