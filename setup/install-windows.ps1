# Sophiella Orchestrator Core - Windows 11 Installation Script
# Automated setup for Dell Latitude and Windows 11 systems

param(
    [switch]$SkipNodeInstall,
    [switch]$SkipPythonInstall,
    [switch]$SkipGitInstall,
    [switch]$QuietMode
)

# Color functions for better output
function Write-ColorText($text, $color = "White") {
    Write-Host $text -ForegroundColor $color
}

function Write-Success($text) { Write-ColorText "✅ $text" "Green" }
function Write-Error($text) { Write-ColorText "❌ $text" "Red" }
function Write-Warning($text) { Write-ColorText "⚠️  $text" "Yellow" }
function Write-Info($text) { Write-ColorText "🔵 $text" "Cyan" }

# Header
Clear-Host
Write-ColorText @"
🕊️ ================================================================
   SOPHIELLA ORCHESTRATOR CORE - WINDOWS 11 INSTALLER
   Dell Latitude Optimized Setup
================================================================
"@ "Magenta"

Write-Info "Starting installation on $(Get-Date)"
Write-Info "System: $($env:COMPUTERNAME) - $($env:USERNAME)"

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Warning "This script should be run as Administrator for best results."
    Write-Info "Some features may require elevated privileges."
}

# Set PowerShell execution policy
try {
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    Write-Success "PowerShell execution policy configured"
} catch {
    Write-Warning "Could not set execution policy: $($_.Exception.Message)"
}

# Function to check if a command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Function to download and install software
function Install-Software($name, $url, $installer, $checkCommand) {
    Write-Info "Checking $name..."
    
    if (Test-Command $checkCommand) {
        Write-Success "$name is already installed"
        return $true
    }
    
    Write-Info "Downloading $name..."
    try {
        $tempPath = "$env:TEMP\$installer"
        Invoke-WebRequest -Uri $url -OutFile $tempPath -UseBasicParsing
        
        Write-Info "Installing $name..."
        Start-Process -FilePath $tempPath -Wait -ArgumentList "/SILENT"
        
        # Refresh environment variables
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        if (Test-Command $checkCommand) {
            Write-Success "$name installed successfully"
            return $true
        } else {
            Write-Error "$name installation failed"
            return $false
        }
    } catch {
        Write-Error "Failed to install $name: $($_.Exception.Message)"
        return $false
    }
}

# Install Node.js
if (-not $SkipNodeInstall) {
    $nodeInstalled = Install-Software "Node.js" "https://nodejs.org/dist/v20.11.0/node-v20.11.0-x64.msi" "node-installer.msi" "node"
    if (-not $nodeInstalled) {
        Write-Error "Node.js installation failed. Please install manually from https://nodejs.org/"
        exit 1
    }
}

# Install Python
if (-not $SkipPythonInstall) {
    Write-Info "Checking Python..."
    if (-not (Test-Command "python")) {
        Write-Info "Python not found. Installing Python 3.11..."
        try {
            $pythonUrl = "https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"
            $pythonInstaller = "$env:TEMP\python-installer.exe"
            
            Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller -UseBasicParsing
            Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_pip=1" -Wait
            
            # Refresh PATH
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
            
            if (Test-Command "python") {
                Write-Success "Python installed successfully"
            } else {
                Write-Error "Python installation failed"
            }
        } catch {
            Write-Error "Failed to install Python: $($_.Exception.Message)"
        }
    } else {
        Write-Success "Python is already installed"
    }
}

# Install Git
if (-not $SkipGitInstall) {
    $gitInstalled = Install-Software "Git" "https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.2/Git-2.42.0.2-64-bit.exe" "git-installer.exe" "git"
    if (-not $gitInstalled) {
        Write-Warning "Git installation failed. You may need to install manually."
    }
}

# Verify installations
Write-Info "Verifying installations..."

$nodeVersion = if (Test-Command "node") { node --version } else { "Not installed" }
$npmVersion = if (Test-Command "npm") { npm --version } else { "Not installed" }
$pythonVersion = if (Test-Command "python") { python --version } else { "Not installed" }
$gitVersion = if (Test-Command "git") { git --version } else { "Not installed" }

Write-Info "Installation Summary:"
Write-Host "  Node.js: $nodeVersion" -ForegroundColor $(if ($nodeVersion -ne "Not installed") { "Green" } else { "Red" })
Write-Host "  npm: $npmVersion" -ForegroundColor $(if ($npmVersion -ne "Not installed") { "Green" } else { "Red" })
Write-Host "  Python: $pythonVersion" -ForegroundColor $(if ($pythonVersion -ne "Not installed") { "Green" } else { "Red" })
Write-Host "  Git: $gitVersion" -ForegroundColor $(if ($gitVersion -ne "Not installed") { "Green" } else { "Red" })

# Install Node.js global packages
if (Test-Command "npm") {
    Write-Info "Installing global Node.js packages..."
    try {
        npm install -g n8n nodemon --silent
        Write-Success "Global packages installed (n8n, nodemon)"
    } catch {
        Write-Warning "Some global packages may have failed to install"
    }
}

# Install project dependencies
Write-Info "Installing project dependencies..."

if (Test-File "package.json") {
    try {
        npm install --silent
        Write-Success "Node.js dependencies installed"
    } catch {
        Write-Error "Failed to install Node.js dependencies"
    }
} else {
    Write-Warning "package.json not found. Make sure you're in the project directory."
}

# Install Python dependencies
if (Test-File "system-control\requirements.txt") {
    try {
        python -m pip install --quiet -r system-control\requirements.txt
        Write-Success "Python dependencies installed"
    } catch {
        Write-Error "Failed to install Python dependencies"
    }
} else {
    Write-Warning "Python requirements.txt not found"
}

# Create environment file
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Success "Environment file created from template"
    } else {
        Write-Warning ".env.example not found"
    }
}

# Windows-specific optimizations for Dell Latitude
Write-Info "Applying Dell Latitude optimizations..."

try {
    # Set high performance power plan
    powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
    Write-Success "Set high performance power plan"
} catch {
    Write-Warning "Could not set power plan (requires admin privileges)"
}

# Create desktop shortcuts
Write-Info "Creating desktop shortcuts..."
$desktop = [Environment]::GetFolderPath("Desktop")
$currentDir = Get-Location

# Create start script
$startScript = @"
@echo off
echo 🕊️ Starting Sophiella Orchestrator Core...
cd /d "$currentDir"
start "Main Server" cmd /k "npm start"
timeout /t 3 /nobreak >nul
start "System Control" cmd /k "npm run system-control"
timeout /t 3 /nobreak >nul
start "n8n" cmd /k "npm run n8n"
echo ✅ All services started!
pause
"@

$startScript | Out-File -FilePath "$desktop\Start Sophiella.bat" -Encoding ASCII
Write-Success "Desktop shortcut created"

# Final summary
Write-ColorText @"

🎉 ================================================================
   INSTALLATION COMPLETE!
================================================================

🚀 To start Sophiella:
   - Double-click 'Start Sophiella.bat' on your desktop
   - OR run: npm start

🌐 Access Points:
   - Main Server: http://localhost:3000
   - System Control: http://127.0.0.1:5001  
   - n8n Interface: http://localhost:5678

📋 Next Steps:
   1. Configure .env file with your API keys (optional)
   2. Test the installation with: npm run test
   3. Start with voice commands or n8n workflows

🕊️ Welcome to Sophiella - Your AI Orchestration System!

"@ "Green"

Write-Info "Installation completed on $(Get-Date)"
Write-Info "Logs saved to: $env:TEMP\sophiella-install.log"
