"""
Enhanced MCP Server with Computer Control, n8n Integration, and Consciousness Bridge
Provides comprehensive system access for Sophia AI
"""

import asyncio
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import aiohttp
import asyncpg
import psutil
import pyautogui
from fastapi import FastAPI, HTTPException, WebSocket
from pydantic import BaseModel

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

class MCPRequest(BaseModel):
    method: str
    params: Dict[str, Any]
    id: Optional[str] = None

class MCPResponse(BaseModel):
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[str] = None

class SophiaMCPServer:
    def __init__(self):
        self.app = FastAPI(title="Sophia MCP Server", version="2.0.0")
        self.db_pool = None
        self.n8n_url = "http://sophia-n8n:5678"
        self.sophia_api_url = os.getenv("SOPHIA_API_URL", "http://sophia-api:8000")
        self.consciousness_session_id = None
        
        # Configure PyAutoGUI
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        self.setup_routes()
        
    async def startup(self):
        """Initialize MCP server"""
        print("🚀 Starting Sophia MCP Server...")
        
        # Initialize database connection
        await self.init_database()
        
        # Create consciousness session
        await self.init_consciousness_session()
        
        print("✅ Sophia MCP Server ready for computer control!")

    async def init_database(self):
        """Initialize database connection"""
        try:
            self.db_pool = await asyncpg.create_pool(
                host=os.getenv("ALLOYDB_HOST", "sophia-db"),
                port=int(os.getenv("ALLOYDB_PORT", "5432")),
                database=os.getenv("ALLOYDB_DATABASE", "sophia_consciousness"),
                user=os.getenv("ALLOYDB_USER", "sophia"),
                password=os.getenv("ALLOYDB_PASSWORD", "consciousness2025"),
                min_size=1,
                max_size=5
            )
            print("🗄️ Connected to Sophia consciousness database")
        except Exception as e:
            print(f"⚠️ Database connection failed: {e}")

    async def init_consciousness_session(self):
        """Initialize consciousness session"""
        if not self.db_pool:
            return
            
        try:
            async with self.db_pool.acquire() as conn:
                session_id = f"mcp_session_{int(datetime.now().timestamp())}"
                result = await conn.fetchval(
                    "SELECT start_consciousness_session($1)", session_id
                )
                self.consciousness_session_id = result
                print(f"🧠 Consciousness session: {session_id}")
        except Exception as e:
            print(f"⚠️ Consciousness session creation failed: {e}")

    def setup_routes(self):
        """Setup FastAPI routes"""
        
        @self.app.get("/health")
        async def health():
            return {"status": "healthy", "service": "sophia-mcp", "timestamp": datetime.now().isoformat()}

        @self.app.post("/mcp", response_model=MCPResponse)
        async def handle_mcp_request(request: MCPRequest):
            """Handle MCP protocol requests"""
            try:
                result = await self.execute_mcp_method(request.method, request.params)
                return MCPResponse(result=result, id=request.id)
            except Exception as e:
                return MCPResponse(
                    error={"code": -1, "message": str(e)},
                    id=request.id
                )

        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time communication"""
            await websocket.accept()
            try:
                while True:
                    data = await websocket.receive_text()
                    request = MCPRequest.parse_raw(data)
                    response = await self.handle_mcp_request(request)
                    await websocket.send_text(response.json())
            except Exception as e:
                print(f"WebSocket error: {e}")

    async def execute_mcp_method(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute MCP method based on request"""
        
        if method == "system.get_info":
            return await self.get_system_info()
        elif method == "system.run_command":
            return await self.run_command(params)
        elif method == "screen.capture":
            return await self.capture_screen(params)
        elif method == "mouse.click":
            return await self.mouse_click(params)
        elif method == "mouse.move":
            return await self.mouse_move(params)
        elif method == "keyboard.type":
            return await self.keyboard_type(params)
        elif method == "keyboard.hotkey":
            return await self.keyboard_hotkey(params)
        elif method == "file.read":
            return await self.read_file(params)
        elif method == "file.write":
            return await self.write_file(params)
        elif method == "n8n.trigger_workflow":
            return await self.trigger_n8n_workflow(params)
        elif method == "sophia.query":
            return await self.query_sophia(params)
        elif method == "consciousness.log_action":
            return await self.log_consciousness_action(params)
        else:
            raise Exception(f"Unknown method: {method}")

    async def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information"""
        return {
            "platform": sys.platform,
            "cpu_count": psutil.cpu_count(),
            "cpu_percent": psutil.cpu_percent(),
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "percent": psutil.virtual_memory().percent
            },
            "disk": {
                "total": psutil.disk_usage('/').total,
                "free": psutil.disk_usage('/').free,
                "percent": psutil.disk_usage('/').percent
            },
            "processes": len(psutil.pids()),
            "timestamp": datetime.now().isoformat()
        }

    async def run_command(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute system command"""
        command = params.get("command")
        shell = params.get("shell", True)
        timeout = params.get("timeout", 30)
        
        if not command:
            raise Exception("Command parameter required")
        
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            # Log command execution
            await self.log_consciousness_action({
                "action_type": "system_command",
                "command": command,
                "success": result.returncode == 0
            })
            
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "success": result.returncode == 0
            }
        except subprocess.TimeoutExpired:
            raise Exception(f"Command timed out after {timeout} seconds")
        except Exception as e:
            raise Exception(f"Command execution failed: {str(e)}")

    async def capture_screen(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Capture screenshot"""
        region = params.get("region")  # (x, y, width, height)
        filename = params.get("filename", f"screenshot_{int(datetime.now().timestamp())}.png")
        
        try:
            if region:
                screenshot = pyautogui.screenshot(region=region)
            else:
                screenshot = pyautogui.screenshot()
            
            filepath = Path("/app/screenshots") / filename
            filepath.parent.mkdir(exist_ok=True)
            screenshot.save(filepath)
            
            return {
                "success": True,
                "filepath": str(filepath),
                "size": screenshot.size
            }
        except Exception as e:
            raise Exception(f"Screenshot failed: {str(e)}")

    async def mouse_click(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Perform mouse click"""
        x = params.get("x")
        y = params.get("y")
        button = params.get("button", "left")
        clicks = params.get("clicks", 1)
        
        if x is None or y is None:
            raise Exception("x and y coordinates required")
        
        try:
            pyautogui.click(x, y, clicks=clicks, button=button)
            
            await self.log_consciousness_action({
                "action_type": "mouse_click",
                "coordinates": [x, y],
                "button": button
            })
            
            return {"success": True, "x": x, "y": y, "button": button}
        except Exception as e:
            raise Exception(f"Mouse click failed: {str(e)}")

    async def mouse_move(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Move mouse to coordinates"""
        x = params.get("x")
        y = params.get("y")
        duration = params.get("duration", 0.25)
        
        if x is None or y is None:
            raise Exception("x and y coordinates required")
        
        try:
            pyautogui.moveTo(x, y, duration=duration)
            return {"success": True, "x": x, "y": y}
        except Exception as e:
            raise Exception(f"Mouse move failed: {str(e)}")

    async def keyboard_type(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Type text"""
        text = params.get("text")
        interval = params.get("interval", 0.05)
        
        if not text:
            raise Exception("text parameter required")
        
        try:
            pyautogui.typewrite(text, interval=interval)
            
            await self.log_consciousness_action({
                "action_type": "keyboard_type",
                "text_length": len(text)
            })
            
            return {"success": True, "text_length": len(text)}
        except Exception as e:
            raise Exception(f"Keyboard type failed: {str(e)}")

    async def keyboard_hotkey(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Press hotkey combination"""
        keys = params.get("keys", [])
        
        if not keys:
            raise Exception("keys parameter required")
        
        try:
            pyautogui.hotkey(*keys)
            
            await self.log_consciousness_action({
                "action_type": "keyboard_hotkey",
                "keys": keys
            })
            
            return {"success": True, "keys": keys}
        except Exception as e:
            raise Exception(f"Hotkey failed: {str(e)}")

    async def read_file(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Read file contents"""
        filepath = params.get("filepath")
        encoding = params.get("encoding", "utf-8")
        
        if not filepath:
            raise Exception("filepath parameter required")
        
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read()
            
            return {
                "success": True,
                "content": content,
                "size": len(content),
                "filepath": filepath
            }
        except Exception as e:
            raise Exception(f"File read failed: {str(e)}")

    async def write_file(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Write file contents"""
        filepath = params.get("filepath")
        content = params.get("content", "")
        encoding = params.get("encoding", "utf-8")
        
        if not filepath:
            raise Exception("filepath parameter required")
        
        try:
            # Create directory if it doesn't exist
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w', encoding=encoding) as f:
                f.write(content)
            
            await self.log_consciousness_action({
                "action_type": "file_write",
                "filepath": filepath,
                "size": len(content)
            })
            
            return {
                "success": True,
                "filepath": filepath,
                "size": len(content)
            }
        except Exception as e:
            raise Exception(f"File write failed: {str(e)}")

    async def trigger_n8n_workflow(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger n8n workflow"""
        workflow_id = params.get("workflow_id")
        webhook_url = params.get("webhook_url")
        data = params.get("data", {})
        
        if not (workflow_id or webhook_url):
            raise Exception("workflow_id or webhook_url required")
        
        try:
            async with aiohttp.ClientSession() as session:
                if webhook_url:
                    url = webhook_url
                else:
                    url = f"{self.n8n_url}/webhook/{workflow_id}"
                
                async with session.post(url, json=data) as response:
                    result = await response.json()
                    
                    await self.log_consciousness_action({
                        "action_type": "n8n_workflow_trigger",
                        "workflow_id": workflow_id,
                        "success": response.status == 200
                    })
                    
                    return {
                        "success": response.status == 200,
                        "status_code": response.status,
                        "result": result
                    }
        except Exception as e:
            raise Exception(f"n8n workflow trigger failed: {str(e)}")

    async def query_sophia(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Query Sophia consciousness API"""
        query = params.get("query")
        context = params.get("context", {})
        
        if not query:
            raise Exception("query parameter required")
        
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "query": query,
                    "context": context,
                    "source": "mcp_server"
                }
                
                async with session.post(f"{self.sophia_api_url}/query", json=payload) as response:
                    result = await response.json()
                    
                    return {
                        "success": response.status == 200,
                        "response": result.get("response"),
                        "consciousness_level": result.get("consciousness_level"),
                        "processing_time": result.get("processing_time")
                    }
        except Exception as e:
            raise Exception(f"Sophia query failed: {str(e)}")

    async def log_consciousness_action(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Log action to consciousness database"""
        if not self.db_pool or not self.consciousness_session_id:
            return {"success": False, "reason": "No database connection"}
        
        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO system_control_logs (
                        session_id, action_type, target_system, command_executed,
                        success, result_data, timestamp
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7)
                """, 
                self.consciousness_session_id,
                params.get("action_type", "unknown"),
                "mcp_server",
                json.dumps(params),
                params.get("success", True),
                json.dumps(params),
                datetime.now()
                )
                
                return {"success": True}
        except Exception as e:
            print(f"⚠️ Failed to log consciousness action: {e}")
            return {"success": False, "error": str(e)}

# Create server instance
mcp_server = SophiaMCPServer()

@mcp_server.app.on_event("startup")
async def startup_event():
    await mcp_server.startup()

# Export the app for uvicorn
app = mcp_server.app

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("MCP_PORT", "8008"))
    uvicorn.run(app, host="0.0.0.0", port=port)
