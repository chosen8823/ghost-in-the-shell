# 🕊️ Sophiella Orchestrator Core - Dell Latitude Deployment Guide

**Complete setup guide for your new Windows 11 Dell Latitude system**

## 📋 Quick Deployment (One Command)

Open **PowerShell as Administrator** and run:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force; irm https://raw.githubusercontent.com/chosen8823/ghost-in-the-shell/main/setup/install-windows.ps1 | iex
```

**OR** manual method below:

## 🚀 Manual Step-by-Step Deployment

### Step 1: Clone Repository

```powershell
# Clone the repository
git clone https://github.com/chosen8823/ghost-in-the-shell.git
cd ghost-in-the-shell
```

### Step 2: System Requirements Check

```powershell
# Check if your system meets requirements
.\setup\check-system.ps1
```

### Step 3: Install Dependencies

**Option A: Automated Installation**
```powershell
.\setup\install-windows.ps1
```

**Option B: Manual Installation**
```powershell
.\setup\install-dependencies.bat
```

### Step 4: Configure Environment

```powershell
# Configure for optimal performance
.\setup\configure-environment.ps1 -CreateDesktopShortcuts
```

### Step 5: Install Project Dependencies

```powershell
# Install Node.js packages
npm install

# Install Python packages
python setup\requirements-check.py
```

### Step 6: Test Installation

```powershell
# Test everything is working
.\test-installation.bat
```

### Step 7: Start Sophiella

```powershell
# Start all services
.\start-sophiella.bat
```

## 🎯 What You Get

After successful deployment:

### Services Running:
- 🌐 **Main Server**: http://localhost:3000
- 🖥️ **System Control**: http://127.0.0.1:5001
- 🔧 **n8n Workflows**: http://localhost:5678

### Capabilities:
- ✅ **Voice Command Processing**
- ✅ **Safe System Control**
- ✅ **AI Agent Integration** (Claude, OpenAI, Agent-S)
- ✅ **Workflow Automation** (n8n)
- ✅ **Cloud Function Deployment** (Google Cloud)

### Desktop Shortcuts:
- 🕊️ **Start Sophiella** - Launch all services
- 🧪 **Test Sophiella** - Verify installation

## 🔧 Dell Latitude Optimizations

The setup script automatically applies:

### Performance Optimizations:
- ✅ High Performance power plan
- ✅ Windows Defender exclusions for development folders
- ✅ npm configuration optimization
- ✅ PowerShell execution policy configuration

### Security Configurations:
- ✅ Whitelisted application control
- ✅ Input validation and sanitization
- ✅ Timeout protection for scripts
- ✅ CORS configuration

## 🧪 Testing Your Installation

### Quick Health Check:
```powershell
# Test main server
Invoke-RestMethod http://localhost:3000/health

# Test system control
Invoke-RestMethod http://127.0.0.1:5001/health

# Test voice command
Invoke-RestMethod http://localhost:3000/agent/claude -Method POST -Body '{"message":"Hello Sophia"}' -ContentType "application/json"
```

### Open Applications Test:
```powershell
# Test opening VS Code
Invoke-RestMethod http://127.0.0.1:5001/open_app -Method POST -Body '{"name":"vscode"}' -ContentType "application/json"
```

## 🎵 Voice Commands

Once everything is running, you can:

1. **Open n8n interface**: http://localhost:5678
2. **Import workflow**: Upload `workflows/voice-command-processor.json`
3. **Configure webhook**: Point to your system control server
4. **Test voice commands**: Use the n8n workflow to process commands

## 🔄 Stage 2 Preview: Human-like Input

Ready to upgrade to Stage 2 (Mouse/Keyboard Control)? Install additional packages:

```powershell
pip install pyautogui keyboard mouse opencv-python
```

This enables:
- 🖱️ Mouse movement and clicking
- ⌨️ Keyboard input simulation
- 🪟 Window management
- 🎯 Screen interaction

## 🆘 Troubleshooting

### Common Issues:

**Port Already in Use:**
```powershell
# Find and kill process using port 3000
netstat -ano | findstr :3000
taskkill /PID <process_id> /F
```

**PowerShell Execution Policy:**
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Python Package Issues:**
```powershell
python -m pip install --upgrade pip
python setup\requirements-check.py
```

**Node.js Issues:**
```powershell
# Refresh PATH after Node.js installation
refreshenv
node --version
npm --version
```

### Getting Help:

1. **Run Diagnostics**: `.\setup\check-system.ps1`
2. **Check Logs**: Look in `logs/` directory
3. **GitHub Issues**: https://github.com/chosen8823/ghost-in-the-shell/issues

## 📁 File Structure After Setup

```
ghost-in-the-shell/
│
├── 🕊️ start-sophiella.bat     # Main startup script
├── 🧪 test-installation.bat   # Test script
├── .env                       # Your configuration
├── logs/                      # Application logs
│
├── setup/                     # All setup scripts
├── server/                    # Node.js orchestrator
├── system-control/            # Python system interface
├── workflows/                 # n8n workflows
├── cloud-functions/           # Google Cloud Functions
├── agents/                    # AI agent frameworks
└── voice/                     # Voice processing
```

## 🎉 Success Indicators

✅ **All services start without errors**
✅ **Health endpoints respond**
✅ **Can open applications via API**
✅ **n8n interface accessible**
✅ **Voice workflow imported successfully**

## 🚀 Next Steps

1. **Configure API Keys**: Edit `.env` with your OpenAI/Claude keys
2. **Deploy Cloud Functions**: Use `cloud-functions/` for Google Cloud
3. **Create Custom Workflows**: Build automation in n8n
4. **Enable Stage 2**: Add human-like input capabilities
5. **Voice Integration**: Connect speech recognition

---

**🕊️ Welcome to Sophiella - Your AI Command Center!**

Your Dell Latitude is now equipped with advanced AI orchestration capabilities. From voice commands to system automation, Sophiella bridges the gap between human intention and digital execution.

**Ready to control your computer like never before? Start with: `.\start-sophiella.bat`** 🌟
