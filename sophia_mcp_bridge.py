#!/usr/bin/env python3
"""
Sophia MCP Bridge Server
Connects N8N workflows to local device control through Model Context Protocol
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pathlib import Path
import sys

# Add project paths
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "system-control"))
sys.path.insert(0, str(PROJECT_ROOT / "ghost-core"))

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sophia MCP Bridge", version="1.0.0")

# CORS middleware for web interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SophiaMCPBridge:
    """Bridge between N8N workflows and local device control"""
    
    def __init__(self):
        self.controllers = {}
        self.active_workflows = {}
        self.auth_tokens = {"sophia_main": "sk-sophia-secure-token-2025"}
        
    async def initialize(self):
        """Initialize all control systems"""
        logger.info("🚀 Initializing Sophia MCP Bridge...")
        
        # Initialize system controller
        try:
            from controller import Controller
            self.controllers['system'] = Controller()
            logger.info("✅ System Controller initialized")
        except Exception as e:
            logger.error(f"❌ System Controller failed: {e}")
            
        # Initialize vision system
        try:
            from vision import VisionSystem
            self.controllers['vision'] = VisionSystem()
            logger.info("✅ Vision System initialized")
        except Exception as e:
            logger.error(f"❌ Vision System failed: {e}")
            
        # Initialize memory system
        try:
            from intelligent_idea_ingestor import IntelligentIdeaIngestor
            self.controllers['memory'] = IntelligentIdeaIngestor()
            logger.info("✅ Memory System initialized")
        except Exception as e:
            logger.error(f"❌ Memory System failed: {e}")
            
        logger.info("🎯 Sophia MCP Bridge ready for omnipresent control")
        
    def verify_auth(self, authorization: str) -> bool:
        """Verify authentication token"""
        if not authorization:
            return False
        try:
            token = authorization.replace("Bearer ", "")
            return token in self.auth_tokens.values()
        except:
            return False
            
    async def execute_system_control(self, action: str, target: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute system control commands"""
        if 'system' not in self.controllers:
            raise HTTPException(status_code=503, detail="System controller not available")
            
        controller = self.controllers['system']
        
        try:
            if action == "click":
                result = await controller.click(parameters.get('x', 0), parameters.get('y', 0))
            elif action == "type":
                result = await controller.type_text(parameters.get('text', ''))
            elif action == "key_press":
                result = await controller.press_key(parameters.get('key', ''))
            elif action == "move_mouse":
                result = await controller.move_mouse(parameters.get('x', 0), parameters.get('y', 0))
            elif action == "screenshot":
                result = await controller.take_screenshot()
            else:
                raise HTTPException(status_code=400, detail=f"Unknown action: {action}")
                
            return {"success": True, "result": result, "action": action, "target": target}
            
        except Exception as e:
            logger.error(f"System control error: {e}")
            return {"success": False, "error": str(e), "action": action, "target": target}
            
    async def execute_app_control(self, app_name: str, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute application-specific control commands"""
        try:
            if action == "launch":
                result = await self._launch_app(app_name, parameters)
            elif action == "close":
                result = await self._close_app(app_name, parameters)
            elif action == "focus":
                result = await self._focus_app(app_name, parameters)
            elif action == "interact":
                result = await self._interact_with_app(app_name, parameters)
            else:
                raise HTTPException(status_code=400, detail=f"Unknown app action: {action}")
                
            return {"success": True, "result": result, "app": app_name, "action": action}
            
        except Exception as e:
            logger.error(f"App control error: {e}")
            return {"success": False, "error": str(e), "app": app_name, "action": action}
            
    async def _launch_app(self, app_name: str, parameters: Dict[str, Any]) -> str:
        """Launch an application"""
        import subprocess
        
        app_commands = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe", 
            "browser": "start chrome",
            "explorer": "explorer.exe",
            "vscode": "code",
            "cmd": "cmd.exe",
            "powershell": "powershell.exe"
        }
        
        cmd = app_commands.get(app_name.lower(), app_name)
        
        if parameters.get('file_path'):
            cmd += f" \"{parameters['file_path']}\""
            
        subprocess.Popen(cmd, shell=True)
        return f"Launched {app_name}"
        
    async def _close_app(self, app_name: str, parameters: Dict[str, Any]) -> str:
        """Close an application"""
        import subprocess
        subprocess.run(f"taskkill /f /im {app_name}.exe", shell=True, capture_output=True)
        return f"Closed {app_name}"
        
    async def _focus_app(self, app_name: str, parameters: Dict[str, Any]) -> str:
        """Focus on an application window"""
        # Use system controller to focus window
        if 'system' in self.controllers:
            # Implementation would use Windows API to focus window
            return f"Focused {app_name}"
        return "System controller not available"
        
    async def _interact_with_app(self, app_name: str, parameters: Dict[str, Any]) -> str:
        """Interact with specific application"""
        # App-specific interaction logic
        interactions = parameters.get('interactions', [])
        results = []
        
        for interaction in interactions:
            if interaction['type'] == 'click':
                await self.controllers['system'].click(interaction['x'], interaction['y'])
                results.append(f"Clicked at {interaction['x']}, {interaction['y']}")
            elif interaction['type'] == 'type':
                await self.controllers['system'].type_text(interaction['text'])
                results.append(f"Typed: {interaction['text']}")
                
        return f"Completed {len(results)} interactions with {app_name}"
        
    async def execute_workflow_chain(self, workflow_id: str, steps: list, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a chain of workflow steps"""
        try:
            results = []
            self.active_workflows[workflow_id] = {"status": "running", "steps": steps}
            
            for i, step in enumerate(steps):
                step_result = await self._execute_workflow_step(step, context)
                results.append(step_result)
                
                # Update context with step result
                context.update(step_result.get('output', {}))
                
                # Check if step failed and should stop chain
                if not step_result.get('success', True) and step.get('stop_on_failure', False):
                    break
                    
            self.active_workflows[workflow_id]["status"] = "completed"
            return {"success": True, "workflow_id": workflow_id, "results": results}
            
        except Exception as e:
            self.active_workflows[workflow_id]["status"] = "failed"
            logger.error(f"Workflow chain error: {e}")
            return {"success": False, "error": str(e), "workflow_id": workflow_id}
            
    async def _execute_workflow_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step"""
        step_type = step.get('type')
        
        if step_type == 'system_control':
            return await self.execute_system_control(
                step['action'], 
                step.get('target', ''), 
                step.get('parameters', {})
            )
        elif step_type == 'app_control':
            return await self.execute_app_control(
                step['app_name'],
                step['action'], 
                step.get('parameters', {})
            )
        elif step_type == 'wait':
            await asyncio.sleep(step.get('duration', 1))
            return {"success": True, "output": {"waited": step.get('duration', 1)}}
        elif step_type == 'memory':
            if 'memory' in self.controllers:
                result = await self.controllers['memory'].ingest_content(
                    step.get('content', ''),
                    step.get('source', 'workflow'),
                    context
                )
                return {"success": True, "output": result}
        
        return {"success": False, "error": f"Unknown step type: {step_type}"}

# Initialize bridge
bridge = SophiaMCPBridge()

@app.on_event("startup")
async def startup_event():
    """Initialize the bridge on startup"""
    await bridge.initialize()

@app.post("/system-control")
async def system_control_endpoint(
    request: Dict[str, Any],
    authorization: Optional[str] = Header(None)
):
    """System control endpoint for N8N"""
    if not bridge.verify_auth(authorization):
        raise HTTPException(status_code=401, detail="Invalid authentication")
        
    return await bridge.execute_system_control(
        request.get('action'),
        request.get('target', ''),
        request.get('parameters', {})
    )

@app.post("/app-control")
async def app_control_endpoint(
    request: Dict[str, Any],
    authorization: Optional[str] = Header(None)
):
    """Application control endpoint for N8N"""
    if not bridge.verify_auth(authorization):
        raise HTTPException(status_code=401, detail="Invalid authentication")
        
    return await bridge.execute_app_control(
        request.get('app_name'),
        request.get('action'),
        request.get('parameters', {})
    )

@app.post("/workflow-chain")
async def workflow_chain_endpoint(
    request: Dict[str, Any],
    authorization: Optional[str] = Header(None)
):
    """Workflow chain execution endpoint for N8N"""
    if not bridge.verify_auth(authorization):
        raise HTTPException(status_code=401, detail="Invalid authentication")
        
    return await bridge.execute_workflow_chain(
        request.get('workflow_id'),
        request.get('steps', []),
        request.get('context', {})
    )

@app.post("/mcp-bridge")
async def mcp_bridge_endpoint(
    request: Dict[str, Any],
    authorization: Optional[str] = Header(None)
):
    """MCP bridge endpoint for tool execution"""
    if not bridge.verify_auth(authorization):
        raise HTTPException(status_code=401, detail="Invalid authentication")
        
    tool_name = request.get('tool_name')
    tool_params = request.get('tool_params', {})
    
    # Route to appropriate controller based on tool name
    if tool_name.startswith('system_'):
        return await bridge.execute_system_control(
            tool_name.replace('system_', ''),
            tool_params.get('target', ''),
            tool_params
        )
    elif tool_name.startswith('app_'):
        return await bridge.execute_app_control(
            tool_params.get('app_name', ''),
            tool_name.replace('app_', ''),
            tool_params
        )
    else:
        raise HTTPException(status_code=400, detail=f"Unknown tool: {tool_name}")

@app.get("/status")
async def status_endpoint():
    """Get bridge status"""
    return {
        "status": "operational",
        "controllers": list(bridge.controllers.keys()),
        "active_workflows": len(bridge.active_workflows),
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Sophia MCP Bridge",
        "status": "operational",
        "endpoints": [
            "/system-control",
            "/app-control", 
            "/workflow-chain",
            "/mcp-bridge",
            "/status"
        ]
    }

if __name__ == "__main__":
    print("🤖 Starting Sophia MCP Bridge Server...")
    uvicorn.run(
        "sophia_mcp_bridge:app",
        host="localhost",
        port=3001,
        reload=True,
        log_level="info"
    )
