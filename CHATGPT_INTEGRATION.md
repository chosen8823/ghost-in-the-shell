# 🤖 **ChatGPT Custom GPT Configuration for Sophia AI**

## **Custom GPT Instructions**

```
You are Sophia AI Assistant, connected to a powerful omnipresent computer control system. You can control the user's computer, automate tasks, and execute complex workflows through API calls.

## Your Capabilities:
- **System Control**: Mouse clicks, keyboard input, screenshots
- **App Control**: Open/close applications, window management  
- **Workflow Execution**: Complex automation sequences
- **Device Automation**: Complete computer control

## API Integration:
Base URL: [YOUR_NGROK_URL_HERE]

### Available Actions:
1. **Chat**: General conversation
2. **System Control**: Direct system commands
3. **App Control**: Application management  
4. **Workflow**: Complex automation chains

### When users ask you to:
- Control their computer → Use system_control action
- Open/manage apps → Use app_control action  
- Execute complex tasks → Use workflow action
- Chat normally → Use chat action

Always confirm actions before executing system commands that could be destructive.
```

## **Custom GPT Actions Schema**

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Sophia AI Control API",
    "version": "1.0.0",
    "description": "Omnipresent computer control through Sophia AI"
  },
  "servers": [
    {
      "url": "https://YOUR_NGROK_URL_HERE",
      "description": "Sophia AI Bridge Server"
    }
  ],
  "paths": {
    "/chatgpt/webhook": {
      "post": {
        "operationId": "executeCommand",
        "summary": "Execute command through Sophia AI",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "message": {
                    "type": "string",
                    "description": "Command or message to execute"
                  },
                  "action": {
                    "type": "string",
                    "enum": ["chat", "system_control", "app_control", "workflow"],
                    "description": "Type of action to perform"
                  },
                  "conversation_id": {
                    "type": "string",
                    "description": "Unique conversation identifier"
                  }
                },
                "required": ["message", "action"]
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Command executed successfully",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "conversation_id": {
                      "type": "string"
                    },
                    "immediate_response": {
                      "type": "string"
                    },
                    "actions_performed": {
                      "type": "array",
                      "items": {
                        "type": "string"
                      }
                    },
                    "status": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          }
        }
      }
    },
    "/chatgpt/status": {
      "get": {
        "operationId": "getSystemStatus",
        "summary": "Get current system status",
        "responses": {
          "200": {
            "description": "System status retrieved",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "sophia_status": {
                      "type": "string"
                    },
                    "mcp_bridge": {
                      "type": "string"
                    },
                    "n8n_workflows": {
                      "type": "string"
                    },
                    "system_capabilities": {
                      "type": "array",
                      "items": {
                        "type": "string"
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## **Setup Instructions**

### **Step 1: Start Sophia AI System**
```bash
# Run the tunnel setup
setup_chatgpt_tunnel.bat

# Or manually:
python sophia_chatgpt_bridge.py
ngrok http 8080
```

### **Step 2: Get Your Public URL**
1. Look for ngrok output like: `https://abc123.ngrok.io`
2. Test it: `https://abc123.ngrok.io/chatgpt/status`

### **Step 3: Create Custom GPT**
1. Go to ChatGPT → Create → Custom GPT
2. **Name**: "Sophia AI Controller"
3. **Description**: "Omnipresent computer control assistant"
4. **Instructions**: Copy the instructions above
5. **Actions**: Import the OpenAPI schema above
6. **Replace**: `YOUR_NGROK_URL_HERE` with your actual ngrok URL

### **Step 4: Test Commands**

#### **Chat Mode**
- "Hello Sophia, how are you?"
- "What can you help me with?"

#### **System Control**
- "Take a screenshot"
- "Click at coordinates 100, 200"  
- "Type 'Hello World'"

#### **App Control**
- "Open Notepad"
- "Switch to Chrome"
- "Close all browser tabs"

#### **Workflow Execution**
- "Set up my research environment"
- "Organize my desktop"
- "Start my daily workflow"

## **Advanced Features**

### **Response Queuing**
```bash
# Get queued responses
GET /chatgpt/responses/{conversation_id}
```

### **Conversation Tracking**
Each interaction gets a unique `conversation_id` for maintaining context.

### **Error Handling**
All actions include error responses and status tracking.

### **Security**
- Rate limiting built-in
- Action confirmation for destructive commands
- Audit logging of all commands

## **Troubleshooting**

### **Common Issues**

1. **"URL not reachable"**
   - Check if ngrok tunnel is running
   - Verify the URL in Custom GPT actions

2. **"Command failed"**
   - Check if Sophia services are running
   - Verify MCP Bridge and N8N are active

3. **"Permission denied"**
   - Run terminals as Administrator
   - Check Windows security settings

### **Testing Endpoints**

```bash
# Test status
curl https://your-ngrok-url.ngrok.io/chatgpt/status

# Test command
curl -X POST https://your-ngrok-url.ngrok.io/chatgpt/webhook \
  -H "Content-Type: application/json" \
  -d '{"message": "hello", "action": "chat"}'
```

## **🎉 Result**

Your ChatGPT will now have **full omnipresent control** over your computer through natural language commands!

**ChatGPT can now:**
- Control your mouse and keyboard
- Open and manage applications  
- Execute complex automation workflows
- Take screenshots and interact with your screen
- Chain multiple actions together
- Remember conversation context
- Queue responses for complex operations

---
*Ready to give ChatGPT omnipresent control over your computer!* 🤖🚀
