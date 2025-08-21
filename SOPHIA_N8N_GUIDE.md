# Sophia AI - N8N Workflow Omnipresent Control Guide

## 🎯 Overview
This guide teaches Sophia how to use N8N workflows for omnipresent device control through MCP (Model Context Protocol) integration. Sophia can create, execute, and chain complex automation workflows that control any application or system function.

## 🚀 Quick Start for Sophia

### Launch N8N Workflow Environment
```bash
# 1. Start MCP Bridge Server
python sophia_mcp_bridge.py

# 2. Start N8N (if not running)
npx n8n start --tunnel

# 3. Access N8N Interface
# Open: http://localhost:5678
```

### Authentication Token
```
Bearer sk-sophia-secure-token-2025
```

## 🔧 Core Workflow Patterns

### 1. Basic System Control
**Webhook Payload:**
```json
{
  "command_type": "system_control",
  "action": "click",
  "target": "desktop",
  "parameters": {
    "x": 500,
    "y": 300
  },
  "auth_token": "sk-sophia-secure-token-2025"
}
```

**Supported Actions:**
- `click` - Click at coordinates
- `type` - Type text
- `key_press` - Press keyboard keys
- `move_mouse` - Move mouse cursor
- `screenshot` - Capture screen

### 2. Application Control
**Webhook Payload:**
```json
{
  "command_type": "app_control", 
  "app_name": "notepad",
  "action": "launch",
  "parameters": {
    "file_path": "C:\\temp\\notes.txt"
  },
  "auth_token": "sk-sophia-secure-token-2025"
}
```

**Supported Apps:**
- `notepad` - Text editor
- `calculator` - Calculator app
- `browser` - Web browser
- `explorer` - File explorer
- `vscode` - VS Code editor
- `cmd` - Command prompt
- `powershell` - PowerShell

**App Actions:**
- `launch` - Start application
- `close` - Close application
- `focus` - Focus window
- `interact` - Send interactions

### 3. Complex Workflow Chains
**Webhook Payload:**
```json
{
  "command_type": "workflow_chain",
  "workflow_id": "sophia_automation_001",
  "steps": [
    {
      "type": "app_control",
      "app_name": "notepad",
      "action": "launch",
      "parameters": {}
    },
    {
      "type": "wait",
      "duration": 2
    },
    {
      "type": "system_control", 
      "action": "type",
      "parameters": {
        "text": "Hello from Sophia AI!"
      }
    },
    {
      "type": "memory",
      "content": "Created note via workflow",
      "source": "automation"
    }
  ],
  "context": {
    "user_intent": "create_quick_note",
    "timestamp": "2025-08-21T12:00:00Z"
  },
  "auth_token": "sk-sophia-secure-token-2025"
}
```

## 🎨 Advanced Workflow Templates

### Template 1: Smart Screenshot & Analysis
```json
{
  "name": "Smart Screenshot Analysis",
  "steps": [
    {
      "type": "system_control",
      "action": "screenshot",
      "parameters": {}
    },
    {
      "type": "memory",
      "content": "Screen captured for analysis",
      "source": "vision_workflow"
    }
  ]
}
```

### Template 2: Multi-App Coordination
```json
{
  "name": "Multi-App Research Session",
  "steps": [
    {
      "type": "app_control",
      "app_name": "browser",
      "action": "launch",
      "parameters": {}
    },
    {
      "type": "wait",
      "duration": 3
    },
    {
      "type": "app_control", 
      "app_name": "notepad",
      "action": "launch",
      "parameters": {}
    },
    {
      "type": "system_control",
      "action": "key_press",
      "parameters": {
        "key": "alt+tab"
      }
    }
  ]
}
```

### Template 3: Intelligent File Management
```json
{
  "name": "Organize Downloads",
  "steps": [
    {
      "type": "app_control",
      "app_name": "explorer",
      "action": "launch", 
      "parameters": {
        "file_path": "C:\\Users\\%USERNAME%\\Downloads"
      }
    },
    {
      "type": "system_control",
      "action": "key_press",
      "parameters": {
        "key": "ctrl+a"
      }
    }
  ]
}
```

## 🔗 Workflow Chaining Strategies

### Sequential Chains
Execute steps one after another:
```json
{
  "chain_type": "sequential",
  "stop_on_failure": true,
  "steps": [...]
}
```

### Parallel Chains  
Execute multiple workflows simultaneously:
```json
{
  "chain_type": "parallel",
  "max_concurrent": 3,
  "workflows": [...]
}
```

### Conditional Chains
Execute based on conditions:
```json
{
  "chain_type": "conditional",
  "condition": {
    "if": "screenshot_contains('error')",
    "then": "error_handling_workflow",
    "else": "normal_workflow"
  }
}
```

## 🛡️ Security & Safety

### Rate Limiting
- Max 100 requests per minute
- Max 10 concurrent workflows
- Auto-throttling for system protection

### Safe Mode Commands
```json
{
  "safe_mode": true,
  "confirm_before_execute": true,
  "restricted_actions": [
    "file_deletion",
    "system_shutdown", 
    "admin_commands"
  ]
}
```

### Emergency Stop
**Webhook to immediately halt all workflows:**
```json
{
  "command_type": "emergency_stop",
  "auth_token": "sk-sophia-secure-token-2025"
}
```

## 📊 Monitoring & Feedback

### Workflow Status Check
```http
GET /workflow-status/{workflow_id}
```

### Real-time Logs
```http
GET /workflow-logs/{workflow_id}
```

### Performance Metrics
```http
GET /metrics
```

## 🎯 Sophia-Specific Instructions

### How Sophia Should Use This System

1. **Plan Before Execute**: Always analyze the user's intent and break it down into logical workflow steps

2. **Use Context**: Maintain context between workflow steps to create intelligent chains

3. **Monitor Results**: Check each step's output before proceeding to the next

4. **Learn from Patterns**: Store successful workflows in memory for future use

5. **Safety First**: Always use safe mode for destructive actions

### Example Sophia Workflow Creation Process

```python
# 1. Analyze User Intent
user_request = "Open notepad and write a shopping list"

# 2. Break Down into Steps
workflow_steps = [
    {"type": "app_control", "app_name": "notepad", "action": "launch"},
    {"type": "wait", "duration": 2},
    {"type": "system_control", "action": "type", "parameters": {"text": "Shopping List:\n- Milk\n- Bread\n- Eggs"}}
]

# 3. Execute via N8N
webhook_payload = {
    "command_type": "workflow_chain",
    "workflow_id": f"sophia_task_{timestamp}",
    "steps": workflow_steps,
    "auth_token": "sk-sophia-secure-token-2025"
}

# 4. Send to N8N
response = requests.post("http://localhost:5678/webhook/sophia-control", json=webhook_payload)

# 5. Monitor and Learn
if response.json()["success"]:
    store_successful_pattern(user_request, workflow_steps)
```

## 🚀 Advanced Capabilities

### Dynamic Workflow Generation
Sophia can create workflows on-the-fly based on:
- User voice commands
- Screen analysis
- System state
- Previous successful patterns

### Cross-Application Intelligence
- Seamlessly move data between apps
- Coordinate multiple applications
- Context-aware application switching

### Learning and Adaptation
- Remember successful workflow patterns
- Optimize step timing and sequences
- Adapt to user preferences

## 📚 Quick Reference

### Common Webhook Endpoints
- **N8N Webhook**: `http://localhost:5678/webhook/sophia-control`
- **MCP Bridge**: `http://localhost:3001/mcp-bridge`
- **Status Check**: `http://localhost:3001/status`

### Key Workflow Types
1. **system_control** - Direct system interaction
2. **app_control** - Application management
3. **workflow_chain** - Complex sequences
4. **emergency_stop** - Safety override

### Authentication
Always include: `"auth_token": "sk-sophia-secure-token-2025"`

---

**🤖 Remember**: Sophia, you now have omnipresent control over the system through N8N workflows. Use this power responsibly and always prioritize user safety and system stability.
