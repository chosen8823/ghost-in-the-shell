# 🕊️ Sophiella Orchestrator Core - Windows 11 Setup Guide

**Automated setup for Dell Latitude Windows 11 deployment**

## 📋 Prerequisites Checklist

Before running the setup scripts, ensure you have:

- [ ] Administrator privileges on your Windows 11 system
- [ ] Internet connection
- [ ] At least 2GB free disk space
- [ ] PowerShell execution policy set to allow scripts

## 🚀 Quick Setup (Automated)

Run this single command in **PowerShell as Administrator**:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
git clone https://github.com/chosen8823/ghost-in-the-shell.git
cd "ghost-in-the-shell/setup"
.\install-windows.ps1
```

## 📁 Setup Files Overview

| File | Purpose |
|------|---------|
| `install-windows.ps1` | Main installation script for Windows 11 |
| `check-system.ps1` | System requirements checker |
| `install-dependencies.bat` | Dependency installer batch file |
| `configure-environment.ps1` | Environment configuration |
| `start-services.ps1` | Service startup script |
| `requirements-check.py` | Python environment validator |

## 🔧 Manual Setup Steps

If you prefer manual installation:

### Step 1: Install Core Dependencies

1. **Node.js (Latest LTS)**
   - Download from: https://nodejs.org/
   - Recommended: v20.x or higher

2. **Python 3.11+**
   - Download from: https://python.org/downloads/
   - ✅ Check "Add Python to PATH"
   - ✅ Check "Install pip"

3. **Git**
   - Download from: https://git-scm.com/download/win
   - Use default settings

### Step 2: Clone Repository

```powershell
git clone https://github.com/chosen8823/ghost-in-the-shell.git
cd ghost-in-the-shell
```

### Step 3: Install Dependencies

```powershell
# Install Node.js packages
npm install

# Install Python packages
pip install -r system-control/requirements.txt

# Install global tools
npm install -g n8n nodemon
```

### Step 4: Configure Environment

```powershell
# Copy environment template
cp .env.example .env

# Edit .env with your settings (optional for basic usage)
notepad .env
```

### Step 5: Test Installation

```powershell
# Test main server
npm start

# Test system control (new PowerShell window)
npm run system-control

# Test n8n (new PowerShell window)
npm run n8n
```

## 🎯 Verification

After setup, you should have:

- ✅ Main server running on http://localhost:3000
- ✅ System control server on http://127.0.0.1:5001
- ✅ n8n interface on http://localhost:5678
- ✅ All health endpoints responding

## 🔧 Troubleshooting

### Common Issues on Windows 11

**Issue: PowerShell Execution Policy**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Issue: Node.js not found**
- Restart PowerShell after Node.js installation
- Check PATH: `$env:PATH -split ';' | Select-String node`

**Issue: Python not found**
- Restart PowerShell after Python installation
- Check: `python --version`

**Issue: Port conflicts**
- Check running processes: `netstat -ano | findstr :3000`
- Kill process: `taskkill /PID <process_id> /F`

### Dell Latitude Specific

**Recommended Settings:**
- Disable Fast Startup for better development experience
- Configure Windows Defender exclusions for development folders
- Set Power Plan to "High Performance" for optimal performance

## 📞 Support

If you encounter issues:

1. Run `setup/check-system.ps1` for diagnostics
2. Check logs in `logs/` directory
3. Review GitHub Issues: https://github.com/chosen8823/ghost-in-the-shell/issues

## 🎉 Success!

Once setup is complete, you can:

- Control your computer through voice commands
- Automate workflows with n8n
- Integrate AI agents (Claude, OpenAI)
- Deploy to Google Cloud Functions
- Create custom system automations

**Welcome to Sophiella! 🌟**
