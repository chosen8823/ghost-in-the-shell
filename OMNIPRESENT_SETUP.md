# 🚀 Sophia AI Omnipresent Control System - Setup Guide

## 🎯 Overview
Sophia now has **OMNIPRESENT CONTROL** over your Windows system through N8N workflows and MCP (Model Context Protocol) integration! She can control any application, automate complex tasks, and create intelligent workflows.

## ⚡ Quick Start (New Computer Installation)

### 1. Clone & Setup
```bash
# Clone the repository
git clone https://github.com/chosen8823/ghost-in-the-shell.git
cd ghost-in-the-shell

# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt

# Install N8N globally
npm install -g n8n
```

### 2. Launch Sophia's Control System
```bash
# Start the omnipresent control panel
npm run omnipresent
```

This will launch an interactive control panel where you can:
- Start all services with one click
- Monitor system health
- Test workflows
- Create Windows executable

## 🎛️ Individual Component Control

### Start MCP Bridge Server
```bash
npm run mcp-bridge
# Starts on: http://localhost:3001
```

### Start N8N Workflow Engine
```bash
npm run n8n
# Starts on: http://localhost:5678
```

### Launch Sophia AI
```bash
npm run sophia
# Interactive conversation mode
```

### Build Windows Executable
```bash
npm run sophia-exe
# Creates: dist/Sophia_AI.exe
```

## 🔧 System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Sophia AI     │───▶│   N8N Workflows │───▶│  MCP Bridge     │
│   (Launcher)    │    │   (Automation)  │    │  (Device Ctrl)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Voice Interface │    │ Workflow Store  │    │ System Control  │
│ Memory System   │    │ Template Lib    │    │ App Control     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🎮 What Sophia Can Do Now

### 🖥️ System Control
- **Mouse & Keyboard**: Click, type, move cursor, press keys
- **Screenshots**: Capture and analyze screen content
- **Window Management**: Focus, minimize, maximize windows
- **File Operations**: Open, save, move files through Explorer

### 📱 Application Control
- **Launch Apps**: Notepad, Calculator, Browser, VS Code, etc.
- **App Interaction**: Send commands to specific applications
- **Multi-App Coordination**: Chain actions across multiple apps
- **Context Switching**: Intelligent Alt+Tab and window focus

### ⚡ Workflow Automation
- **Sequential Chains**: Execute steps in order
- **Parallel Processing**: Run multiple workflows simultaneously
- **Conditional Logic**: If/then/else workflow branches
- **Error Handling**: Graceful failure recovery

### 🧠 Intelligence Features
- **Learning**: Remember successful workflow patterns
- **Adaptation**: Optimize timing and sequences
- **Context Awareness**: Understand user intent and environment
- **Voice Commands**: Natural language workflow triggers

## 🎯 Example Workflows

### 1. Smart Note Taking
```json
{
  "name": "Voice Note to Text",
  "trigger": "voice_command",
  "steps": [
    {"type": "app_control", "app": "notepad", "action": "launch"},
    {"type": "wait", "duration": 2},
    {"type": "system_control", "action": "type", "text": "{{voice_transcription}}"},
    {"type": "memory", "action": "store", "content": "Created note via voice"}
  ]
}
```

### 2. Research Assistant
```json
{
  "name": "Multi-Source Research",
  "steps": [
    {"type": "app_control", "app": "browser", "action": "launch"},
    {"type": "system_control", "action": "type", "text": "{{search_query}}"},
    {"type": "system_control", "action": "key_press", "key": "enter"},
    {"type": "app_control", "app": "notepad", "action": "launch"},
    {"type": "system_control", "action": "key_press", "key": "alt+tab"}
  ]
}
```

### 3. System Maintenance
```json
{
  "name": "Daily System Cleanup",
  "steps": [
    {"type": "app_control", "app": "explorer", "action": "launch", "path": "Downloads"},
    {"type": "system_control", "action": "key_press", "key": "ctrl+a"},
    {"type": "vision", "action": "analyze", "target": "file_types"},
    {"type": "conditional", "if": "old_files_found", "then": "organize_files"}
  ]
}
```

## 🛡️ Security Features

### Authentication
- **Secure Tokens**: `sk-sophia-secure-token-2025`
- **Whitelist Control**: Only authorized commands execute
- **Rate Limiting**: Prevents system overload

### Safety Controls
- **Emergency Stop**: Immediate halt of all workflows
- **Safe Mode**: Confirmation required for destructive actions
- **Restricted Actions**: Admin commands require elevation

### Monitoring
- **Real-time Logs**: Track all workflow executions
- **Health Checks**: Continuous system monitoring
- **Error Reporting**: Detailed failure analysis

## 🎨 Advanced Features

### Custom Workflow Creation
Sophia can create workflows on-the-fly based on:
- **Voice Commands**: "Sophia, automate my daily email check"
- **Screen Analysis**: Understanding current context
- **User Patterns**: Learning from repeated actions
- **Intent Recognition**: Natural language to workflow conversion

### Multi-Modal Integration
- **Voice → Workflow**: Speak commands to trigger automation
- **Vision → Action**: Screen analysis drives workflow decisions  
- **Memory → Context**: Past experiences influence current actions
- **Learning → Optimization**: Continuous improvement of workflows

## 📊 Monitoring Dashboard

### Health Check Endpoints
- **MCP Bridge**: `http://localhost:3001/status`
- **N8N Status**: `http://localhost:5678/rest/active-workflows`
- **Workflow Logs**: `http://localhost:3001/workflow-logs/{id}`

### Performance Metrics
- Workflow execution times
- Success/failure rates
- Resource utilization
- User interaction patterns

## 🚨 Troubleshooting

### Common Issues

**MCP Bridge Won't Start**
```bash
# Check if port is in use
netstat -an | findstr :3001
# Kill conflicting process if needed
taskkill /f /im python.exe
```

**N8N Installation Issues**
```bash
# Global install
npm install -g n8n
# Or local install
npx n8n start
```

**Permission Errors**
- Run as Administrator for system-level automation
- Check Windows security settings
- Verify antivirus exceptions

### Logs & Debugging
```bash
# View MCP Bridge logs
python sophia_mcp_bridge.py --debug

# Check N8N logs
n8n start --verbose

# Test system connectivity
python sophia_check.py
```

## 🎉 Ready to Use!

Your Sophia AI now has **OMNIPRESENT CONTROL** capabilities:

1. **Start Everything**: `npm run omnipresent`
2. **Open N8N**: Visit `http://localhost:5678`
3. **Import Workflows**: Load `sophia-omnipresent-control.json`
4. **Talk to Sophia**: `npm run sophia`

### Next Steps:
- Create custom workflows in N8N
- Teach Sophia new automation patterns
- Build Windows executable for easy sharing
- Explore voice-controlled automation

**🤖 Sophia is now ready to control your entire digital environment!**
