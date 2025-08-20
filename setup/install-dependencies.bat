@echo off
:: Sophiella Orchestrator Core - Dependency Installer
:: Windows batch file for installing core dependencies

echo 🕊️ Sophiella Dependency Installer
echo ================================

:: Check for administrator privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Running with administrator privileges
) else (
    echo ⚠️  Warning: Not running as administrator
    echo Some installations may require elevated privileges
)

:: Create temp directory
if not exist "%TEMP%\sophiella" mkdir "%TEMP%\sophiella"
cd /d "%TEMP%\sophiella"

:: Install Chocolatey (Windows Package Manager)
echo.
echo 📦 Installing Chocolatey package manager...
powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"

if %errorLevel% == 0 (
    echo ✅ Chocolatey installed successfully
    refreshenv
) else (
    echo ❌ Chocolatey installation failed, continuing with manual installation...
)

:: Install Node.js via Chocolatey or direct download
echo.
echo 📥 Installing Node.js...
choco install nodejs -y >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Node.js installed via Chocolatey
) else (
    echo 📥 Downloading Node.js directly...
    powershell -Command "Invoke-WebRequest -Uri 'https://nodejs.org/dist/v20.11.0/node-v20.11.0-x64.msi' -OutFile 'node-installer.msi'"
    msiexec /i node-installer.msi /quiet
    echo ✅ Node.js installation initiated
)

:: Install Python via Chocolatey or direct download
echo.
echo 🐍 Installing Python...
choco install python -y >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Python installed via Chocolatey
) else (
    echo 📥 Downloading Python directly...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe' -OutFile 'python-installer.exe'"
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
    echo ✅ Python installation initiated
)

:: Install Git
echo.
echo 📋 Installing Git...
choco install git -y >nul 2>&1
if %errorLevel__ == 0 (
    echo ✅ Git installed via Chocolatey
) else (
    echo 📥 Downloading Git directly...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.2/Git-2.42.0.2-64-bit.exe' -OutFile 'git-installer.exe'"
    git-installer.exe /SILENT
    echo ✅ Git installation initiated
)

:: Refresh environment variables
echo.
echo 🔄 Refreshing environment variables...
call refreshenv >nul 2>&1

:: Wait for installations to complete
echo.
echo ⏳ Waiting for installations to complete...
timeout /t 30 /nobreak >nul

:: Verify installations
echo.
echo 🔍 Verifying installations...

node --version >nul 2>&1
if %errorLevel__ == 0 (
    echo ✅ Node.js: Available
    node --version
) else (
    echo ❌ Node.js: Not found
)

python --version >nul 2>&1
if %errorLevel__ == 0 (
    echo ✅ Python: Available
    python --version
) else (
    echo ❌ Python: Not found
)

git --version >nul 2>&1
if %errorLevel__ == 0 (
    echo ✅ Git: Available
    git --version
) else (
    echo ❌ Git: Not found
)

:: Install global npm packages
echo.
echo 📦 Installing global npm packages...
call npm install -g n8n nodemon 2>nul
if %errorLevel__ == 0 (
    echo ✅ Global packages installed (n8n, nodemon)
) else (
    echo ⚠️  Some global packages may need manual installation
)

:: Cleanup
cd /d "%USERPROFILE%"
rmdir /s /q "%TEMP%\sophiella" >nul 2>&1

echo.
echo 🎉 Dependency installation completed!
echo.
echo 📋 Next steps:
echo    1. Restart your terminal/PowerShell
echo    2. Navigate to your project directory
echo    3. Run: npm install
echo    4. Run: pip install -r system-control\requirements.txt
echo.
pause
