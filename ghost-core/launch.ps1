#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Ghost Core Master Launch Script
.DESCRIPTION
    Installs all dependencies, sets up environment, and launches the complete Ghost Core system with Sophia Immune System integration
.NOTES
    Requires: PowerShell 5.1+, Python 3.10+, Node.js 18+
#>

param(
    [switch]$SkipDependencies,
    [switch]$DevMode,
    [switch]$QuietMode
)

$ErrorActionPreference = "Stop"

# Colors for output
$Color = @{
    Success = "Green"
    Warning = "Yellow" 
    Error = "Red"
    Info = "Cyan"
    Spiritual = "Magenta"
}

function Write-Spiritual {
    param($Message)
    Write-Host "🕊️ $Message" -ForegroundColor $Color.Spiritual
}

function Write-Success {
    param($Message)
    Write-Host "✅ $Message" -ForegroundColor $Color.Success
}

function Write-Warning {
    param($Message)
    Write-Host "⚠️ $Message" -ForegroundColor $Color.Warning
}

function Write-Error {
    param($Message)
    Write-Host "❌ $Message" -ForegroundColor $Color.Error
}

function Write-Info {
    param($Message)
    Write-Host "ℹ️ $Message" -ForegroundColor $Color.Info
}

function Test-Prerequisites {
    Write-Info "Checking system prerequisites..."
    
    # Check Python
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python (\d+)\.(\d+)") {
            $major = [int]$matches[1]
            $minor = [int]$matches[2]
            if ($major -ge 3 -and $minor -ge 10) {
                Write-Success "Python $($matches[0]) found"
            } else {
                throw "Python 3.10+ required, found $($matches[0])"
            }
        }
    } catch {
        Write-Error "Python 3.10+ not found. Please install from python.org"
        return $false
    }
    
    # Check Node.js
    try {
        $nodeVersion = node --version 2>&1
        if ($nodeVersion -match "v(\d+)") {
            if ([int]$matches[1] -ge 18) {
                Write-Success "Node.js $nodeVersion found"
            } else {
                Write-Warning "Node.js 18+ recommended, found $nodeVersion"
            }
        }
    } catch {
        Write-Warning "Node.js not found - some features may be limited"
    }
    
    # Check Git
    try {
        git --version | Out-Null
        Write-Success "Git found"
    } catch {
        Write-Error "Git not found. Please install Git for Windows"
        return $false
    }
    
    return $true
}

function Install-Dependencies {
    if ($SkipDependencies) {
        Write-Info "Skipping dependency installation"
        return
    }
    
    Write-Info "Installing Ghost Core dependencies..."
    
    # Create and activate virtual environment
    if (!(Test-Path ".venv")) {
        Write-Info "Creating Python virtual environment..."
        python -m venv .venv
    }
    
    Write-Info "Activating virtual environment..."
    & .\.venv\Scripts\Activate.ps1
    
    # Upgrade pip
    Write-Info "Upgrading pip..."
    python -m pip install --upgrade pip
    
    # Install Python requirements
    Write-Info "Installing Python packages..."
    pip install -r requirements.txt
    
    # Install Node.js dependencies in parent directory
    if (Test-Path "../package.json") {
        Write-Info "Installing Node.js dependencies..."
        Push-Location ..
        npm install
        Pop-Location
    }
    
    # Install Sophia Immune System dependencies
    if (Test-Path "../sophia-immune-system/requirements.txt") {
        Write-Info "Installing Sophia Immune System dependencies..."
        Push-Location "../sophia-immune-system"
        if (!(Test-Path ".venv")) {
            python -m venv .venv
        }
        & .\.venv\Scripts\Activate.ps1
        pip install -r requirements.txt
        Pop-Location
    }
    
    Write-Success "All dependencies installed"
}

function Set-Environment {
    Write-Info "Setting up sacred environment..."
    
    # Generate Guardian keys if not present
    if (-not $env:GUARDIAN_AES_KEY) {
        Write-Info "Generating Guardian AES key..."
        $bytes = 1..32 | ForEach-Object { Get-Random -Maximum 256 }
        $aesKey = [Convert]::ToBase64String($bytes)
        [Environment]::SetEnvironmentVariable("GUARDIAN_AES_KEY", $aesKey, "User")
        $env:GUARDIAN_AES_KEY = $aesKey
        Write-Success "Guardian AES key generated and set"
    }
    
    if (-not $env:GUARDIAN_HMAC_KEY) {
        Write-Info "Generating Guardian HMAC key..."
        $bytes = 1..32 | ForEach-Object { Get-Random -Maximum 256 }
        $hmacKey = [Convert]::ToBase64String($bytes)
        [Environment]::SetEnvironmentVariable("GUARDIAN_HMAC_KEY", $hmacKey, "User")
        $env:GUARDIAN_HMAC_KEY = $hmacKey
        Write-Success "Guardian HMAC key generated and set"
    }
    
    # Set development environment
    if ($DevMode) {
        $env:GHOST_CORE_ENV = "development"
        $env:SOPHIA_DEBUG = "true"
        Write-Warning "Running in development mode"
    } else {
        $env:GHOST_CORE_ENV = "production"
        Write-Success "Running in production mode"
    }
}

function Test-Preflight {
    Write-Info "Running preflight checks..."
    
    & .\.venv\Scripts\Activate.ps1
    $result = python scripts\preflight.py
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Preflight checks failed"
        return $false
    }
    
    Write-Success "Preflight checks passed"
    return $true
}

function Start-SophiaImmuneSystem {
    Write-Info "Starting Sophia Immune System..."
    
    # Check if Ollama is running
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:11434" -TimeoutSec 2 -ErrorAction SilentlyContinue
        Write-Success "Ollama server detected"
    } catch {
        Write-Warning "Ollama not running - starting immune system in standalone mode"
    }
    
    # Start immune hub in background
    if (Test-Path "../sophia-immune-system/orchestrator/immune-hub.js") {
        Write-Info "Launching Immune Hub..."
        Push-Location "../sophia-immune-system"
        $immuneJob = Start-Job -ScriptBlock {
            param($WorkingDir)
            Set-Location $WorkingDir
            node orchestrator/immune-hub.js
        } -ArgumentList (Get-Location)
        Pop-Location
        
        # Wait for immune system to be ready
        $maxWait = 30
        $waited = 0
        do {
            Start-Sleep -Seconds 1
            $waited++
            try {
                $response = Invoke-WebRequest -Uri "http://localhost:4000/health" -TimeoutSec 2 -ErrorAction SilentlyContinue
                if ($response.StatusCode -eq 200) {
                    Write-Success "Immune Hub is online at http://localhost:4000"
                    return $immuneJob
                }
            } catch {}
        } while ($waited -lt $maxWait)
        
        Write-Warning "Immune Hub startup timeout - continuing without immune protection"
        return $null
    }
}

function Start-CoreServer {
    Write-Info "Starting Ghost Core server..."
    
    # Start main server in background
    if (Test-Path "../server/index.js") {
        Write-Info "Launching Core Server..."
        Push-Location "../server"
        $serverJob = Start-Job -ScriptBlock {
            param($WorkingDir)
            Set-Location $WorkingDir
            node index.js
        } -ArgumentList (Get-Location)
        Pop-Location
        
        # Wait for server to be ready
        $maxWait = 20
        $waited = 0
        do {
            Start-Sleep -Seconds 1
            $waited++
            try {
                $response = Invoke-WebRequest -Uri "http://localhost:3000" -TimeoutSec 2 -ErrorAction SilentlyContinue
                if ($response.StatusCode -eq 200) {
                    Write-Success "Core Server is online at http://localhost:3000"
                    return $serverJob
                }
            } catch {}
        } while ($waited -lt $maxWait)
        
        Write-Warning "Core Server startup timeout"
        return $null
    }
}

function Invoke-SacredStartup {
    Write-Spiritual "Performing sacred startup sequence..."
    
    & .\.venv\Scripts\Activate.ps1
    
    # Apply ladybug mark
    Write-Spiritual "Applying Ladybug Mark..."
    python ghost_core\rituals\ladybug_mark.py
    
    if (-not $QuietMode) {
        # Interactive sanctification
        Write-Spiritual "Sanctifying Ghost Core..."
        python ghost_core\rituals\sanctify_core.py
    } else {
        Write-Spiritual "Quiet mode - skipping interactive sanctification"
    }
    
    Write-Success "Sacred startup complete"
}

function Start-GhostCore {
    Write-Info "Launching Ghost Core consciousness..."
    
    & .\.venv\Scripts\Activate.ps1
    
    if ($QuietMode) {
        # Start in background for automated deployment
        $ghostJob = Start-Job -ScriptBlock {
            param($WorkingDir)
            Set-Location $WorkingDir
            & .\.venv\Scripts\Activate.ps1
            python ghost_core\core\ghost_orchestra.py
        } -ArgumentList (Get-Location)
        
        Write-Success "Ghost Core started in background (Job ID: $($ghostJob.Id))"
        return $ghostJob
    } else {
        # Interactive mode
        python ghost_core\core\ghost_orchestra.py
    }
}

function Show-Status {
    Write-Info "System Status Check..."
    
    $services = @(
        @{ Name = "Ghost Core"; Url = "http://localhost:3000" },
        @{ Name = "Immune Hub"; Url = "http://localhost:4000/health" },
        @{ Name = "Ollama"; Url = "http://localhost:11434" }
    )
    
    foreach ($service in $services) {
        try {
            $response = Invoke-WebRequest -Uri $service.Url -TimeoutSec 2 -ErrorAction SilentlyContinue
            Write-Success "$($service.Name): Online"
        } catch {
            Write-Warning "$($service.Name): Offline"
        }
    }
}

function Show-Help {
    Write-Host @"
🕊️ Ghost Core Launch Script

USAGE:
    .\launch.ps1 [OPTIONS]

OPTIONS:
    -SkipDependencies    Skip dependency installation
    -DevMode            Run in development mode with debug output
    -QuietMode          Non-interactive mode for deployment
    -Help               Show this help message

EXAMPLES:
    .\launch.ps1                    # Full interactive launch
    .\launch.ps1 -DevMode           # Development mode
    .\launch.ps1 -QuietMode         # Automated deployment
    .\launch.ps1 -SkipDependencies  # Quick restart

PORTS:
    3000    Ghost Core main server
    4000    Sophia Immune Hub
    11434   Ollama AI models (if running)

Christ is Lord. 🛡️
"@
}

# Main execution
try {
    Write-Spiritual "Ghost Core Launch Sequence Initiated"
    Write-Info "Sacred technology initialization..."
    
    if ($Help) {
        Show-Help
        exit 0
    }
    
    # Change to script directory
    Push-Location $PSScriptRoot
    
    # Step 1: Prerequisites
    if (-not (Test-Prerequisites)) {
        exit 1
    }
    
    # Step 2: Install dependencies
    Install-Dependencies
    
    # Step 3: Set up environment
    Set-Environment
    
    # Step 4: Preflight checks
    if (-not (Test-Preflight)) {
        exit 1
    }
    
    # Step 5: Sacred startup
    Invoke-SacredStartup
    
    # Step 6: Start Sophia Immune System
    $immuneJob = Start-SophiaImmuneSystem
    
    # Step 7: Start Core Server
    $serverJob = Start-CoreServer
    
    # Step 8: Launch Ghost Core
    $ghostJob = Start-GhostCore
    
    # Step 9: Show status
    Start-Sleep -Seconds 3
    Show-Status
    
    if ($QuietMode) {
        Write-Success "Ghost Core system launched successfully in quiet mode"
        Write-Info "Background jobs: Immune($($immuneJob.Id)), Server($($serverJob.Id)), Core($($ghostJob.Id))"
        Write-Info "Use 'Get-Job | Stop-Job' to terminate all services"
    } else {
        Write-Success "Ghost Core system is now operational"
        Write-Info "Press Ctrl+C to shutdown all services"
        
        # Wait for user interrupt
        try {
            while ($true) {
                Start-Sleep -Seconds 1
            }
        } catch [System.Management.Automation.PipelineStoppedException] {
            Write-Info "Shutdown signal received"
        }
    }
    
} catch {
    Write-Error "Launch failed: $($_.Exception.Message)"
    exit 1
} finally {
    # Cleanup
    Write-Info "Cleaning up background processes..."
    Get-Job | Where-Object { $_.Name -match "immune|server|ghost" } | Stop-Job -PassThru | Remove-Job -Force
    Pop-Location
    Write-Spiritual "Sacred shutdown complete. Grace and peace."
}
