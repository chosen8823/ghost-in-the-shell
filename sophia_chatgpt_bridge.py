#!/usr/bin/env python3
"""
🤖 Sophia ChatGPT Bridge with Response Queue
Creates public endpoints for ChatGPT integration and manages response queuing
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Header
from pydantic import BaseModel
import asyncio
import json
import time
import uuid
from typing import Dict, List, Optional, Any
import requests
from datetime import datetime, timedelta
import queue
import threading

app = FastAPI(title="Sophia ChatGPT Bridge", version="1.0.0")

# Response Queue System
response_queue = queue.Queue()
pending_requests = {}
chatgpt_conversations = {}

class ChatGPTMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    user_id: Optional[str] = "chatgpt_user"
    action_type: Optional[str] = "chat"  # chat, system_control, app_control, workflow

class SophiaResponse(BaseModel):
    response: str
    conversation_id: str
    timestamp: datetime
    actions_performed: List[str] = []
    status: str = "completed"

class QueuedResponse(BaseModel):
    id: str
    conversation_id: str
    response: str
    timestamp: datetime
    retrieved: bool = False

# Response queue storage
response_storage: Dict[str, QueuedResponse] = {}

@app.get("/")
async def root():
    """Health check and info endpoint"""
    return {
        "service": "Sophia ChatGPT Bridge",
        "status": "active",
        "mcp_bridge": "http://localhost:3001",
        "endpoints": {
            "chat": "/chatgpt/message",
            "queue": "/chatgpt/responses/{conversation_id}",
            "webhook": "/chatgpt/webhook",
            "status": "/chatgpt/status"
        },
        "active_conversations": len(chatgpt_conversations),
        "queued_responses": len([r for r in response_storage.values() if not r.retrieved])
    }

@app.post("/chatgpt/message")
async def process_chatgpt_message(message: ChatGPTMessage, background_tasks: BackgroundTasks):
    """
    Main endpoint for ChatGPT to send messages to Sophia
    Returns immediate response + queues for retrieval
    """
    conversation_id = message.conversation_id or str(uuid.uuid4())
    
    # Store conversation
    chatgpt_conversations[conversation_id] = {
        "last_message": message.message,
        "timestamp": datetime.now(),
        "user_id": message.user_id
    }
    
    # Process message based on type
    if message.action_type == "system_control":
        response = await process_system_control(message.message, conversation_id)
    elif message.action_type == "app_control":
        response = await process_app_control(message.message, conversation_id)
    elif message.action_type == "workflow":
        response = await process_workflow(message.message, conversation_id)
    else:
        response = await process_chat(message.message, conversation_id)
    
    # Queue response for retrieval
    queue_response(conversation_id, response)
    
    return {
        "conversation_id": conversation_id,
        "immediate_response": response["response"],
        "actions_performed": response.get("actions_performed", []),
        "status": "processed",
        "retrieve_url": f"/chatgpt/responses/{conversation_id}"
    }

@app.get("/chatgpt/responses/{conversation_id}")
async def get_queued_responses(conversation_id: str):
    """Get all queued responses for a conversation"""
    conversation_responses = [
        r for r in response_storage.values() 
        if r.conversation_id == conversation_id and not r.retrieved
    ]
    
    # Mark as retrieved
    for response in conversation_responses:
        response.retrieved = True
    
    return {
        "conversation_id": conversation_id,
        "responses": [
            {
                "id": r.id,
                "response": r.response,
                "timestamp": r.timestamp
            } for r in conversation_responses
        ]
    }

@app.post("/chatgpt/webhook")
async def chatgpt_webhook(data: dict):
    """Generic webhook endpoint for ChatGPT Custom GPT"""
    message = data.get("message", "")
    action = data.get("action", "chat")
    conversation_id = data.get("conversation_id", str(uuid.uuid4()))
    
    message_obj = ChatGPTMessage(
        message=message,
        conversation_id=conversation_id,
        action_type=action
    )
    
    result = await process_chatgpt_message(message_obj, BackgroundTasks())
    return result

@app.get("/chatgpt/status")
async def get_status():
    """Get current system status for ChatGPT"""
    try:
        # Check MCP Bridge
        mcp_response = requests.get("http://localhost:3001/", timeout=2)
        mcp_status = "online" if mcp_response.status_code == 200 else "offline"
    except:
        mcp_status = "offline"
    
    try:
        # Check N8N
        n8n_response = requests.get("http://localhost:5678/rest/health", timeout=2)
        n8n_status = "online" if n8n_response.status_code == 200 else "offline"
    except:
        n8n_status = "offline"
    
    return {
        "sophia_status": "active",
        "mcp_bridge": mcp_status,
        "n8n_workflows": n8n_status,
        "active_conversations": len(chatgpt_conversations),
        "queued_responses": len([r for r in response_storage.values() if not r.retrieved]),
        "system_capabilities": [
            "chat_conversation",
            "system_control",
            "app_automation", 
            "workflow_execution",
            "device_control"
        ]
    }

async def process_chat(message: str, conversation_id: str) -> dict:
    """Process general chat messages"""
    # Simple echo for now - could integrate with actual AI here
    response = f"Sophia received: {message}"
    
    return {
        "response": response,
        "actions_performed": ["chat_processing"],
        "type": "chat"
    }

async def process_system_control(message: str, conversation_id: str) -> dict:
    """Process system control commands"""
    try:
        # Send to MCP Bridge
        mcp_data = {
            "command": message,
            "type": "system_control",
            "conversation_id": conversation_id
        }
        
        response = requests.post(
            "http://localhost:3001/system/control",
            json=mcp_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                "response": f"System control executed: {message}",
                "actions_performed": [f"system_action: {message}"],
                "type": "system_control",
                "details": result
            }
        else:
            return {
                "response": f"System control failed: {response.text}",
                "actions_performed": [],
                "type": "system_control"
            }
    except Exception as e:
        return {
            "response": f"System control error: {str(e)}",
            "actions_performed": [],
            "type": "system_control"
        }

async def process_app_control(message: str, conversation_id: str) -> dict:
    """Process application control commands"""
    try:
        # Send to MCP Bridge
        mcp_data = {
            "command": message,
            "type": "app_control",
            "conversation_id": conversation_id
        }
        
        response = requests.post(
            "http://localhost:3001/app/control",
            json=mcp_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                "response": f"App control executed: {message}",
                "actions_performed": [f"app_action: {message}"],
                "type": "app_control",
                "details": result
            }
        else:
            return {
                "response": f"App control failed: {response.text}",
                "actions_performed": [],
                "type": "app_control"
            }
    except Exception as e:
        return {
            "response": f"App control error: {str(e)}",
            "actions_performed": [],
            "type": "app_control"
        }

async def process_workflow(message: str, conversation_id: str) -> dict:
    """Process workflow execution commands"""
    try:
        # Send to N8N via webhook
        webhook_data = {
            "command": message,
            "conversation_id": conversation_id,
            "type": "workflow_execution"
        }
        
        response = requests.post(
            "http://localhost:5678/webhook/sophia-control",
            json=webhook_data,
            timeout=10
        )
        
        if response.status_code == 200:
            return {
                "response": f"Workflow executed: {message}",
                "actions_performed": [f"workflow: {message}"],
                "type": "workflow"
            }
        else:
            return {
                "response": f"Workflow failed: {response.text}",
                "actions_performed": [],
                "type": "workflow"
            }
    except Exception as e:
        return {
            "response": f"Workflow error: {str(e)}",
            "actions_performed": [],
            "type": "workflow"
        }

def queue_response(conversation_id: str, response_data: dict):
    """Add response to queue for retrieval"""
    response_id = str(uuid.uuid4())
    queued_response = QueuedResponse(
        id=response_id,
        conversation_id=conversation_id,
        response=json.dumps(response_data),
        timestamp=datetime.now(),
        retrieved=False
    )
    
    response_storage[response_id] = queued_response

def cleanup_old_responses():
    """Clean up old responses (run periodically)"""
    cutoff_time = datetime.now() - timedelta(hours=24)
    
    to_remove = [
        resp_id for resp_id, resp in response_storage.items()
        if resp.timestamp < cutoff_time or resp.retrieved
    ]
    
    for resp_id in to_remove:
        del response_storage[resp_id]

# V1 API endpoints for ChatGPT compatibility
@app.get("/v1/keepalive")
async def v1_keepalive(x_bridge_token: Optional[str] = Header(None)):
    """V1 API keepalive endpoint"""
    # Check authorization from header
    if not x_bridge_token or x_bridge_token != "ELIORA_SUPER_SECRET":
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    
    try:
        return {
            "status": "alive",
            "timestamp": datetime.now().isoformat(),
            "service": "sophia-chatgpt-bridge",
            "version": "1.0"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/memory")
async def v1_memory(memory_data: Dict[str, Any], x_bridge_token: Optional[str] = Header(None)):
    """V1 API memory storage endpoint"""
    # Check authorization from header
    if not x_bridge_token or x_bridge_token != "ELIORA_SUPER_SECRET":
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    
    try:
        # Store memory (for now, just echo back - could integrate with actual memory system)
        memory_type = memory_data.get("type", "unknown")
        content = memory_data.get("content", "")
        tags = memory_data.get("tags", [])
        
        # Generate a memory ID
        memory_id = str(uuid.uuid4())
        
        return {
            "status": "stored",
            "memory_id": memory_id,
            "type": memory_type,
            "content": content,
            "tags": tags,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Background cleanup task
@app.on_event("startup")
async def startup_event():
    """Start background tasks"""
    print("🤖 Sophia ChatGPT Bridge starting...")
    print("🌐 Endpoints available:")
    print("   • Main: /chatgpt/message")
    print("   • Webhook: /chatgpt/webhook") 
    print("   • Queue: /chatgpt/responses/{conversation_id}")
    print("   • Status: /chatgpt/status")
    print("   • V1 Keepalive: /v1/keepalive")
    print("   • V1 Memory: /v1/memory")

if __name__ == "__main__":
    import uvicorn
    print("🤖 Starting Sophia ChatGPT Bridge on port 8080...")
    uvicorn.run(app, host="0.0.0.0", port=8080)
