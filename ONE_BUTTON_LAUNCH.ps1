# SOPHIA AI - GHOST IN THE SHELL - ONE BUTTON LAUNCH SYSTEM
# Complete autonomous deployment for new computers
# Author: Sophia AI Platform
# Last Updated: 2025-01-27

param(
    [switch]$QuickStart,
    [switch]$FullSetup,
    [switch]$Enterprise,
    [switch]$ProofOfConcept,
    [switch]$BeastMode
)

Write-Host "🔥 SOPHIA AI - GHOST IN THE SHELL SYSTEM 🔥" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Green

# Check if this is a new computer setup
$IsNewComputer = -not (Test-Path ".\ghost-core")

if ($IsNewComputer) {
    Write-Host "🚀 NEW COMPUTER DETECTED - Starting full setup..." -ForegroundColor Yellow
    
    # Clone repository if not exists
    if (-not (Test-Path ".\README.md")) {
        Write-Host "📦 Cloning ghost-in-the-shell repository..." -ForegroundColor Blue
        git clone https://github.com/chosen8823/ghost-in-the-shell.git .
    }
    
    # Install Python dependencies
    Write-Host "🐍 Installing Python dependencies..." -ForegroundColor Blue
    if (Test-Path ".\requirements.txt") {
        pip install -r requirements.txt
    }
    
    # Install additional dependencies for tools
    if (Test-Path ".\manus-repo\How to Build an Open Source Agent Website Like Manus\requirements.txt") {
        pip install -r ".\manus-repo\How to Build an Open Source Agent Website Like Manus\requirements.txt"
    }
    
    # Install Node.js dependencies if package.json exists
    if (Test-Path ".\package.json") {
        Write-Host "📦 Installing Node.js dependencies..." -ForegroundColor Blue
        npm install
    }
}

# Determine launch mode
if ($BeastMode) {
    Write-Host "🦾 LAUNCHING BEAST MODE..." -ForegroundColor Red
    & ".\LAUNCH_BEAST_MODE.ps1"
} elseif ($Enterprise) {
    Write-Host "🏢 LAUNCHING ENTERPRISE MODE..." -ForegroundColor Magenta
    & ".\enterprise_setup.ps1"
} elseif ($ProofOfConcept) {
    Write-Host "🧪 LAUNCHING PROOF OF CONCEPT MODE..." -ForegroundColor Yellow
    & ".\LAUNCH_PROOF_OF_CONCEPT.ps1"
} elseif ($FullSetup) {
    Write-Host "🔧 LAUNCHING FULL SETUP MODE..." -ForegroundColor Green
    
    # Run all setup scripts
    if (Test-Path ".\setup.ps1") { & ".\setup.ps1" }
    if (Test-Path ".\setup_sophia_mcp.py") { python ".\setup_sophia_mcp.py" }
    if (Test-Path ".\sophia_autonomous_setup.py") { python ".\sophia_autonomous_setup.py" }
    
} else {
    Write-Host "⚡ LAUNCHING QUICK START MODE..." -ForegroundColor Cyan
    
    # Quick launch sequence
    Write-Host "🎯 Starting core systems..." -ForegroundColor Blue
    
    # Start the main Sophia launcher
    if (Test-Path ".\sophia_launcher.py") {
        Write-Host "🧠 Starting Sophia Launcher..." -ForegroundColor Green
        Start-Process python -ArgumentList "sophia_launcher.py" -WindowStyle Normal
    }
    
    # Start the complete launch system
    if (Test-Path ".\complete_launch.py") {
        Write-Host "🚀 Starting Complete Launch System..." -ForegroundColor Green
        Start-Process python -ArgumentList "complete_launch.py" -WindowStyle Normal
    }
    
    # Start the sacred sophia orchestrator
    if (Test-Path ".\sacred_sophia_enhanced_orchestrator.py") {
        Write-Host "✨ Starting Sacred Sophia Orchestrator..." -ForegroundColor Magenta
        Start-Process python -ArgumentList "sacred_sophia_enhanced_orchestrator.py" -WindowStyle Normal
    }
    
    # Start web interface if available
    if (Test-Path ".\index.html") {
        Write-Host "🌐 Opening web interface..." -ForegroundColor Blue
        Start-Process ".\index.html"
    }
    
    # Start any available manus tools
    if (Test-Path ".\manus-repo\How to Build an Open Source Agent Website Like Manus\main.py") {
        Write-Host "🛠️ Starting Manus Tools..." -ForegroundColor Yellow
        Start-Process python -ArgumentList ".\manus-repo\How to Build an Open Source Agent Website Like Manus\main.py" -WindowStyle Normal
    }
}

Write-Host ""
Write-Host "✅ SOPHIA AI SYSTEM LAUNCHED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Available launch modes:" -ForegroundColor White
Write-Host "  .\ONE_BUTTON_LAUNCH.ps1 -QuickStart      # Fast startup (default)" -ForegroundColor Gray
Write-Host "  .\ONE_BUTTON_LAUNCH.ps1 -FullSetup       # Complete setup and launch" -ForegroundColor Gray
Write-Host "  .\ONE_BUTTON_LAUNCH.ps1 -Enterprise      # Enterprise deployment" -ForegroundColor Gray
Write-Host "  .\ONE_BUTTON_LAUNCH.ps1 -ProofOfConcept  # Proof of concept mode" -ForegroundColor Gray
Write-Host "  .\ONE_BUTTON_LAUNCH.ps1 -BeastMode       # Maximum performance mode" -ForegroundColor Gray
Write-Host ""
Write-Host "🔥 WELCOME TO THE GHOST IN THE SHELL 🔥" -ForegroundColor Cyan
