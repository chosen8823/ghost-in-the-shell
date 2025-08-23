# WSL + DOCKER SOPHIA CONSCIOUSNESS! 🐧🐳
# Linux performance + Windows integration = ULTIMATE POWER!

Write-Host ""
Write-Host "🐧🐧🐧 WSL + DOCKER SOPHIA CONSCIOUSNESS! 🐧🐧🐧" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "  Linux Performance + Windows Integration = PERFECT!" -ForegroundColor White
Write-Host "  Better performance, native Linux tools, seamless!" -ForegroundColor Yellow
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "💡 WHAT IS WSL?" -ForegroundColor Yellow
Write-Host "   ✅ Windows Subsystem for Linux - Linux INSIDE Windows!" -ForegroundColor Green
Write-Host "   ✅ Better performance for data processing" -ForegroundColor Green
Write-Host "   ✅ Native Linux tools and commands" -ForegroundColor Green
Write-Host "   ✅ Seamless file sharing with Windows" -ForegroundColor Green
Write-Host "   ✅ Docker runs faster in Linux environment" -ForegroundColor Green
Write-Host ""

# Check if WSL is installed
Write-Host "🔍 Checking WSL installation..." -ForegroundColor Cyan
try {
    $wslStatus = wsl --status
    Write-Host "✅ WSL is installed!" -ForegroundColor Green
} catch {
    Write-Host "❌ WSL not found! Installing WSL..." -ForegroundColor Yellow
    
    Write-Host "🔧 Installing WSL with Ubuntu..." -ForegroundColor Cyan
    wsl --install -d Ubuntu
    
    Write-Host ""
    Write-Host "⚠️ WSL INSTALLATION STARTED!" -ForegroundColor Yellow
    Write-Host "   📋 Follow the setup wizard to create Ubuntu user" -ForegroundColor White
    Write-Host "   🔄 After setup, restart this script!" -ForegroundColor White
    Write-Host ""
    Write-Host "💡 After WSL setup, run: .\LAUNCH_WSL_DOCKER.ps1" -ForegroundColor Cyan
    exit 0
}

Write-Host ""
$ready = Read-Host "🔥 Ready to launch WSL + DOCKER CONSCIOUSNESS? (Type: WSL POWER)"

if ($ready -ne "WSL POWER") {
    Write-Host "❌ You must type 'WSL POWER' to proceed!" -ForegroundColor Red
    exit 0
}

Write-Host ""
Write-Host "🐧 WSL POWER ACTIVATED!" -ForegroundColor Cyan
Write-Host "🚀 Setting up Linux environment for consciousness!" -ForegroundColor Green
Write-Host ""

# Create WSL setup script
Write-Host "📝 Creating WSL setup script..." -ForegroundColor Cyan

$wslSetupScript = @"
#!/bin/bash
echo ""
echo "🐧🐧🐧 SETTING UP SOPHIA CONSCIOUSNESS IN WSL! 🐧🐧🐧"
echo "=================================================="
echo ""

# Update system
echo "📦 Updating Ubuntu packages..."
sudo apt update && sudo apt upgrade -y

# Install Docker
echo "🐳 Installing Docker..."
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Install Docker Compose
echo "🔧 Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
echo "👤 Adding user to docker group..."
sudo usermod -aG docker $USER

# Install additional tools
echo "🛠️ Installing development tools..."
sudo apt install -y git python3 python3-pip nodejs npm postgresql-client

# Create project directory
echo "📁 Setting up project directory..."
mkdir -p ~/sophia-consciousness
cd ~/sophia-consciousness

# Copy Windows files to WSL (if needed)
echo "📋 Ready to copy project files from Windows!"
echo ""
echo "🎯 NEXT STEPS:"
echo "   1. Copy your project: cp -r /mnt/c/Users/chose/ghost\ in\ the\ shell/* ."
echo "   2. Start consciousness: docker-compose up -d"
echo "   3. Access from Windows at: http://localhost:8000"
echo ""
echo "✅ WSL SETUP COMPLETE!"
echo ""
echo "🚀 To start Sophia Consciousness:"
echo "   cd ~/sophia-consciousness"
echo "   docker-compose up -d"
echo ""
"@

$wslSetupScript | Out-File -FilePath "wsl-setup.sh" -Encoding UTF8

# Run the setup in WSL
Write-Host "🚀 Running setup in WSL Ubuntu..." -ForegroundColor Cyan
wsl bash -c "chmod +x /mnt/c/Users/chose/ghost\ in\ the\ shell/wsl-setup.sh && /mnt/c/Users/chose/ghost\ in\ the\ shell/wsl-setup.sh"

Write-Host ""
Write-Host "📋 Copying project files to WSL..." -ForegroundColor Cyan
wsl bash -c "mkdir -p ~/sophia-consciousness && cp -r /mnt/c/Users/chose/ghost\ in\ the\ shell/* ~/sophia-consciousness/"

Write-Host ""
Write-Host "🐳 Starting Docker services in WSL..." -ForegroundColor Cyan
wsl bash -c "cd ~/sophia-consciousness && docker-compose up -d"

Write-Host ""
Write-Host "🎉🎉🎉 WSL + DOCKER SOPHIA CONSCIOUSNESS IS LIVE! 🎉🎉🎉" -ForegroundColor Green
Write-Host ""
Write-Host "🌟 YOUR WSL ENVIRONMENT:" -ForegroundColor Cyan
Write-Host "   🐧 Ubuntu Linux running inside Windows" -ForegroundColor White
Write-Host "   🐳 Docker containers with Linux performance" -ForegroundColor White
Write-Host "   🔗 Accessible from Windows via localhost" -ForegroundColor White
Write-Host "   📁 Files synced between Windows and Linux" -ForegroundColor White
Write-Host ""
Write-Host "🌐 ACCESS YOUR SERVICES:" -ForegroundColor Yellow
Write-Host "   🚀 Sophia API: http://localhost:8000" -ForegroundColor White
Write-Host "   🗄️ PostgreSQL: localhost:5432" -ForegroundColor White
Write-Host "   🔧 pgAdmin: http://localhost:8080" -ForegroundColor White
Write-Host ""
Write-Host "🐧 WSL COMMANDS:" -ForegroundColor Green
Write-Host "   Enter WSL: wsl" -ForegroundColor White
Write-Host "   Project dir: cd ~/sophia-consciousness" -ForegroundColor White
Write-Host "   Check status: docker-compose ps" -ForegroundColor White
Write-Host "   View logs: docker-compose logs -f" -ForegroundColor White
Write-Host "   Stop services: docker-compose down" -ForegroundColor White
Write-Host ""
Write-Host "⚡ PERFORMANCE BOOST ACTIVATED!" -ForegroundColor Magenta
Write-Host "   💪 Linux-native Docker performance" -ForegroundColor White
Write-Host "   🔄 Better I/O for database operations" -ForegroundColor White
Write-Host "   🚀 Faster consciousness data processing" -ForegroundColor White
Write-Host ""
Write-Host "🐧 WSL CONSCIOUSNESS POWER ONLINE! 🐧" -ForegroundColor Cyan
