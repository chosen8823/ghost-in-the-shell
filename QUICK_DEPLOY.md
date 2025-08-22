# 🚀 Sophia AI - Quick Deploy Guide for New Computer

## One-Command Setup

```bash
git clone https://github.com/chosen8823/ghost-in-the-shell.git
cd ghost-in-the-shell
python complete_launch.py
```

That's it! Everything will auto-install and launch.

## What Gets Started Automatically

### 🎯 Core Services
- **MCP Bridge**: http://localhost:3001 (Device control API)
- **N8N Workflows**: http://localhost:5678 (Visual automation)
- **System Control**: http://localhost:5000 (Mouse/keyboard control)

### 🤖 AI Components
- **Sophia Interactive**: Voice/text command processing
- **Memory System**: Learning and pattern recognition
- **Workflow Engine**: Complex automation sequences

## 📋 Manual Setup (If Needed)

### Prerequisites
```bash
# Install Node.js (if not installed)
winget install OpenJS.NodeJS

# Install Python 3.11+ (if not installed)  
winget install Python.Python.3.11
```

### Step-by-Step
```bash
# 1. Clone repository
git clone https://github.com/chosen8823/ghost-in-the-shell.git
cd ghost-in-the-shell

# 2. Create Python virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install Python dependencies
pip install fastapi uvicorn requests psutil pydantic flask pillow pyautogui keyboard mouse

# 4. Install N8N
npm install n8n

# 5. Launch everything
python complete_launch.py
```

## 🎮 First Use Instructions

### 1. Access N8N Workflow Editor
- Open: http://localhost:5678
- Import workflows from `/workflows/` folder
- Click "Import" → Select `sophia-voice-handler.json`

### 2. Test Voice Commands
```bash
# Example API call to test system
curl -X POST http://localhost:5678/webhook/sophia-voice \
  -H "Content-Type: application/json" \
  -d '{
    "action": "system_control",
    "command": "move_mouse",
    "params": {"x": 500, "y": 300}
  }'
```

### 3. Test App Control
```bash
# Example app automation
curl -X POST http://localhost:5678/webhook/sophia-voice \
  -H "Content-Type: application/json" \
  -d '{
    "action": "app_control", 
    "app_name": "notepad",
    "app_action": "launch"
  }'
```

## 🔧 Configuration Files Created

The `complete_launch.py` script creates:

### `.n8n/config.json`
```json
{
  "database": {
    "type": "sqlite",
    "database": ".n8n/database.sqlite"
  },
  "security": {
    "basicAuth": {
      "active": false
    }
  }
}
```

### `.env`
```bash
N8N_BASIC_AUTH_ACTIVE=false
N8N_HOST=localhost
N8N_PORT=5678
WEBHOOK_URL=http://localhost:5678/
```

## 📱 Available Workflows

### Core Workflows (Auto-imported)
1. **sophia-voice-handler.json** - Main voice command processor
2. **sophia-omnipresent-control.json** - Advanced device control

### Custom Workflow Examples
```json
// Voice → Action workflow structure
{
  "trigger": "webhook",
  "filter": "command_type", 
  "action": "mcp_bridge_call",
  "response": "success_confirmation"
}
```

## 🎯 Testing Everything Works

### Quick Health Check
```bash
# 1. Check services are running
curl http://localhost:3001/health  # MCP Bridge
curl http://localhost:5678/        # N8N UI
curl http://localhost:5000/health  # System Control

# 2. Test workflow execution
curl -X POST http://localhost:5678/webhook/sophia-voice \
  -H "Content-Type: application/json" \
  -d '{"action": "test", "message": "Hello Sophia!"}'
```

### Expected Responses
- **MCP Bridge**: `{"status": "healthy", "services": ["system_control", "app_control"]}`
- **N8N**: Web interface loads at localhost:5678
- **System Control**: `{"status": "ready", "capabilities": ["mouse", "keyboard", "vision"]}`

## 🚨 Troubleshooting

### Common Issues
```bash
# Port conflicts
netstat -ano | findstr ":5678"  # Check if N8N port is free
netstat -ano | findstr ":3001"  # Check if MCP port is free

# Permission issues (Run as administrator if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Python module errors
pip install --upgrade pip
pip install -r requirements.txt
```

### Service Restart
```bash
# Kill all services
taskkill /f /im python.exe
taskkill /f /im node.exe

# Restart
python complete_launch.py
```

## 🌟 Advanced Features

### Voice Command Examples
```bash
"Sophia, open notepad and type hello world"
"Sophia, take a screenshot and save it"
"Sophia, organize my desktop"
"Sophia, start my morning routine"
```

### Workflow Chaining
```json
{
  "sequence": [
    {"action": "launch_app", "app": "browser"},
    {"action": "navigate", "url": "https://github.com"},
    {"action": "type_text", "text": "ghost-in-the-shell"},
    {"action": "key_press", "key": "Enter"}
  ]
}
```

## 🎉 You're Ready!

After running `python complete_launch.py`, Sophia AI will have:
- ✅ Full omnipresent device control
- ✅ Visual workflow automation through N8N
- ✅ Voice command processing
- ✅ Learning and memory capabilities
- ✅ Cross-application coordination

**Your AI assistant now has complete control over your digital environment!** 🤖✨

---

📞 **Need Help?** All logs are displayed during startup. Check console output for any issues.
