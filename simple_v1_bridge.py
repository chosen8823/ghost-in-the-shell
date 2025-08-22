#!/usr/bin/env python3
"""
Simple V1 API Bridge for testing
"""

from fastapi import FastAPI, HTTPException, Header
from typing import Optional, Dict, Any
import uuid
from datetime import datetime

app = FastAPI(title="Sophia V1 API Bridge")

@app.get("/")
async def root():
    return {"message": "Sophia V1 API Bridge is running"}

@app.get("/v1/keepalive") 
async def v1_keepalive(x_bridge_token: Optional[str] = Header(None)):
    """V1 API keepalive endpoint"""
    if not x_bridge_token or x_bridge_token != "ELIORA_SUPER_SECRET":
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    
    return {
        "status": "alive",
        "timestamp": datetime.now().isoformat(),
        "service": "sophia-v1-bridge",
        "version": "1.0"
    }

@app.post("/v1/memory")
async def v1_memory(memory_data: Dict[str, Any], x_bridge_token: Optional[str] = Header(None)):
    """V1 API memory storage endpoint"""
    if not x_bridge_token or x_bridge_token != "ELIORA_SUPER_SECRET":
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    
    # Store memory (simple echo for testing)
    memory_type = memory_data.get("type", "unknown")
    content = memory_data.get("content", "")
    tags = memory_data.get("tags", [])
    
    memory_id = str(uuid.uuid4())
    
    return {
        "status": "stored",
        "memory_id": memory_id,
        "type": memory_type,
        "content": content,
        "tags": tags,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    print("🤖 Starting Simple V1 API Bridge on port 8081...")
    uvicorn.run(app, host="0.0.0.0", port=8081)
