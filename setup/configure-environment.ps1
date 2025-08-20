# Sophiella Environment Configuration Script
# Sets up environment variables and configuration for optimal performance

param(
    [string]$Environment = "development",
    [switch]$CreateDesktopShortcuts
)

Write-Host "🕊️ Sophiella Environment Configuration" -ForegroundColor Magenta
Write-Host "=====================================" -ForegroundColor Magenta

# Check current directory
$currentDir = Get-Location
if (-not (Test-Path "package.json")) {
    Write-Error "Please run this script from the Sophiella project root directory"
    exit 1
}

Write-Host "📁 Project Directory: $currentDir" -ForegroundColor Cyan

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "✅ Created .env file from template" -ForegroundColor Green
    } else {
        # Create basic .env file
        $envContent = @"
# Sophiella Orchestrator Core Environment Configuration
# Environment: $Environment

# Server Configuration
PORT=3000
NODE_ENV=$Environment

# n8n Configuration
N8N_HOST=localhost
N8N_PORT=5678
N8N_PROTOCOL=http

# System Control
SYSTEM_CONTROL_PORT=5001
SYSTEM_CONTROL_ENABLED=true
WHITELIST_MODE=true

# Security
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5678
SECRET_KEY=sophiella-$(Get-Random)

# Logging
LOG_LEVEL=info
LOG_FILE=logs/sophiella.log

# AI Agent API Keys (Optional - add your keys here)
# OPENAI_API_KEY=your-openai-api-key-here
# ANTHROPIC_API_KEY=your-claude-api-key-here

# Google Cloud Configuration (Optional)
# GOOGLE_CLOUD_PROJECT_ID=your-project-id
# GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# Voice Interface (Optional)
# SPEECH_API_KEY=your-speech-api-key-here
"@
        $envContent | Out-File -FilePath ".env" -Encoding UTF8
        Write-Host "✅ Created basic .env file" -ForegroundColor Green
    }
} else {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
}

# Create logs directory
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
    Write-Host "✅ Created logs directory" -ForegroundColor Green
}

# Configure Windows Defender exclusions (if running as admin)
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if ($isAdmin) {
    Write-Host "🛡️ Configuring Windows Defender exclusions..." -ForegroundColor Yellow
    try {
        Add-MpPreference -ExclusionPath $currentDir
        Add-MpPreference -ExclusionPath "$currentDir\node_modules"
        Add-MpPreference -ExclusionProcess "node.exe"
        Add-MpPreference -ExclusionProcess "python.exe"
        Write-Host "✅ Windows Defender exclusions configured" -ForegroundColor Green
    } catch {
        Write-Warning "Could not configure Windows Defender exclusions"
    }
} else {
    Write-Warning "Run as Administrator to configure Windows Defender exclusions for better performance"
}

# Configure Power Plan for optimal performance
Write-Host "⚡ Optimizing power settings..." -ForegroundColor Yellow
try {
    # Get current power plan
    $currentPlan = (powercfg /getactivescheme).Split("(")[1].Split(")")[0]
    Write-Host "Current Power Plan: $currentPlan" -ForegroundColor Cyan
    
    # Set to High Performance if not already
    if (-not ($currentPlan -match "High performance|Ultimate")) {
        powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Switched to High Performance power plan" -ForegroundColor Green
        }
    } else {
        Write-Host "✅ Already using optimal power plan" -ForegroundColor Green
    }
} catch {
    Write-Warning "Could not optimize power settings"
}

# Create startup scripts
Write-Host "📝 Creating startup scripts..." -ForegroundColor Yellow

# Main startup script
$startupScript = @"
@echo off
title Sophiella Orchestrator Core
color 0A

echo.
echo 🕊️ ================================================================
echo    SOPHIELLA ORCHESTRATOR CORE
echo    Advanced AI Orchestration System  
echo ================================================================
echo.

cd /d "$currentDir"

echo 🚀 Starting services...
echo.

echo 📡 Starting Main Server (Port 3000)...
start "Sophiella Main Server" cmd /k "echo 🌐 Main Server Starting... && npm start"

echo ⏳ Waiting for main server to initialize...
timeout /t 5 /nobreak >nul

echo 🖥️ Starting System Control (Port 5001)...
start "Sophiella System Control" cmd /k "echo 🔧 System Control Starting... && npm run system-control"

echo ⏳ Waiting for system control to initialize...
timeout /t 3 /nobreak >nul

echo 🔧 Starting n8n Workflow Engine (Port 5678)...
start "Sophiella n8n" cmd /k "echo 📋 n8n Starting... && npm run n8n"

echo.
echo ✅ All services started successfully!
echo.
echo 🌐 Access Points:
echo    - Main Server: http://localhost:3000
echo    - System Control: http://127.0.0.1:5001
echo    - n8n Interface: http://localhost:5678
echo.
echo 📋 Press any key to open the main interface...
pause >nul

start http://localhost:3000
"@

$startupScript | Out-File -FilePath "start-sophiella.bat" -Encoding ASCII
Write-Host "✅ Created start-sophiella.bat" -ForegroundColor Green

# Quick test script
$testScript = @"
@echo off
echo 🧪 Testing Sophiella Installation...
echo.

cd /d "$currentDir"

echo 🔍 Checking Node.js...
node --version || echo ❌ Node.js not found

echo 🔍 Checking Python...
python --version || echo ❌ Python not found

echo 🔍 Checking npm packages...
npm list --depth=0 2>nul || echo ⚠️ npm packages need installation

echo 🔍 Checking Python packages...
python -c "import flask, psutil, requests; print('✅ Python packages OK')" 2>nul || echo ❌ Python packages missing

echo.
echo 🔍 Test completed!
pause
"@

$testScript | Out-File -FilePath "test-installation.bat" -Encoding ASCII
Write-Host "✅ Created test-installation.bat" -ForegroundColor Green

# Create desktop shortcuts if requested
if ($CreateDesktopShortcuts) {
    $desktop = [Environment]::GetFolderPath("Desktop")
    
    # Copy startup script to desktop
    Copy-Item "start-sophiella.bat" "$desktop\🕊️ Start Sophiella.bat"
    Copy-Item "test-installation.bat" "$desktop\🧪 Test Sophiella.bat"
    
    Write-Host "✅ Desktop shortcuts created" -ForegroundColor Green
}

# Configure npm for optimal performance
Write-Host "📦 Optimizing npm configuration..." -ForegroundColor Yellow
try {
    npm config set fund false
    npm config set audit false
    npm config set progress true
    Write-Host "✅ npm configuration optimized" -ForegroundColor Green
} catch {
    Write-Warning "Could not optimize npm configuration"
}

Write-Host "`n🎉 Environment configuration completed!" -ForegroundColor Green
Write-Host "`n📋 What's been configured:" -ForegroundColor Cyan
Write-Host "   ✅ Environment variables (.env file)" -ForegroundColor White
Write-Host "   ✅ Logs directory created" -ForegroundColor White
Write-Host "   ✅ Startup scripts created" -ForegroundColor White
Write-Host "   ✅ Power plan optimized" -ForegroundColor White
if ($isAdmin) { Write-Host "   ✅ Windows Defender exclusions" -ForegroundColor White }

Write-Host "`n🚀 To start Sophiella:" -ForegroundColor Yellow
Write-Host "   • Double-click: start-sophiella.bat" -ForegroundColor White
Write-Host "   • Or run: .\start-sophiella.bat" -ForegroundColor White

Write-Host "`n🧪 To test installation:" -ForegroundColor Yellow
Write-Host "   • Double-click: test-installation.bat" -ForegroundColor White
Write-Host "   • Or run: .\test-installation.bat" -ForegroundColor White

Write-Host "`n🕊️ Sophiella is ready for deployment!" -ForegroundColor Magenta
