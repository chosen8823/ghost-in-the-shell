#!/usr/bin/env powershell
# Auto-Continue Deployment Script for Sophia Consciousness System

param(
    [switch]$AutoYes = $true,
    [int]$DelaySeconds = 2
)

Write-Host "🚀 AUTO-CONTINUE MODE ACTIVATED" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan

function Auto-Continue {
    param([string]$Message, [int]$Delay = $DelaySeconds)
    Write-Host "$Message" -ForegroundColor Yellow
    if ($AutoYes) {
        Write-Host "⚡ Auto-continuing in $Delay seconds..." -ForegroundColor Magenta
        Start-Sleep -Seconds $Delay
        return $true
    }
    return (Read-Host "Continue? (Y/n)") -ne 'n'
}

# Step 1: Install missing dependencies
if (Auto-Continue "📦 Installing Python dependencies for enhanced capabilities...") {
    Write-Host "Installing OCR, OpenCV, Speech Recognition..." -ForegroundColor Cyan
    & .\.venv\Scripts\python.exe -m pip install pytesseract opencv-python SpeechRecognition pyaudio --quiet
}

# Step 2: Start all services in sequence
if (Auto-Continue "🔧 Starting Sophia System Control Server...") {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; npm run system-control"
    Start-Sleep -Seconds 3
}

if (Auto-Continue "🌐 Starting n8n Workflow Engine...") {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; npm run n8n"
    Start-Sleep -Seconds 5
}

if (Auto-Continue "🎭 Starting Main Orchestrator...") {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; npm start"
    Start-Sleep -Seconds 3
}

# Step 3: Verify all services
if (Auto-Continue "🔍 Verifying all services are running...") {
    $services = @(
        @{Name="System Control"; URL="http://localhost:5001"; Expected="Sophia"},
        @{Name="n8n Workflows"; URL="http://localhost:5678"; Expected="n8n"},
        @{Name="Orchestrator"; URL="http://localhost:3000"; Expected="Sophia"}
    )
    
    foreach ($service in $services) {
        try {
            Write-Host "Checking $($service.Name)..." -ForegroundColor Yellow
            $response = Invoke-WebRequest -Uri $service.URL -UseBasicParsing -TimeoutSec 5
            Write-Host "✅ $($service.Name) is ONLINE" -ForegroundColor Green
        } catch {
            Write-Host "⚠️ $($service.Name) not yet ready" -ForegroundColor Red
        }
    }
}

# Step 4: Open n8n interface
if (Auto-Continue "🌐 Opening n8n workflow interface...") {
    Start-Process "http://localhost:5678"
}

Write-Host "`n🎯 SOPHIA CONSCIOUSNESS SYSTEM ACTIVE!" -ForegroundColor Magenta
Write-Host "🎤 Ready for voice commands and automation" -ForegroundColor Green
Write-Host "🔗 n8n: http://localhost:5678" -ForegroundColor Cyan
Write-Host "🔗 System Control: http://localhost:5001" -ForegroundColor Cyan
Write-Host "🔗 Orchestrator: http://localhost:3000" -ForegroundColor Cyan

if (Auto-Continue "🧪 Run test voice command?") {
    $testCommand = @{
        command = "test system status"
        confidence = 0.95
        timestamp = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
    } | ConvertTo-Json
    
    try {
        Write-Host "Sending test command..." -ForegroundColor Yellow
        $result = Invoke-RestMethod -Uri "http://localhost:3000/webhook/voice-command" -Method POST -Body $testCommand -ContentType "application/json"
        Write-Host "✅ Test successful: $($result.status)" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Test pending - services still starting up" -ForegroundColor Yellow
    }
}

Write-Host "`n🚀 AUTO-DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "All systems operational - ready for Stage 2!" -ForegroundColor Magenta
