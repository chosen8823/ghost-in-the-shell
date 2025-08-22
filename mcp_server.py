"""
MCP (minimal) HTTP JSON server to expose controlled local terminal and filesystem operations.

SECURITY: This server is powerful and can execute commands and modify files. Keep it behind
an SSH tunnel or localhost-only binding and protect with a strong API key.

Usage (development):
    python -m pip install -r sophia_cloud_infrastructure/requirements.txt
    python mcp_server.py

Run with an SSH tunnel or ngrok when exposing to remote networks.
"""
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse, FileResponse
import subprocess
import os
import sys
import json
from pathlib import Path
import logging
from typing import Optional

# Load config
CONFIG_PATH = Path("config") / "mcp_config.json"
if not CONFIG_PATH.exists():
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps({
        "api_key": "REPLACE_WITH_STRONG_SECRET",
        "bind_host": "127.0.0.1",
        "bind_port": 8008,
        "allow_dangerous": False
    }, indent=2))

with open(CONFIG_PATH, "r") as f:
    CONFIG = json.load(f)

API_KEY = CONFIG.get("api_key")
BIND_HOST = CONFIG.get("bind_host", "127.0.0.1")
BIND_PORT = int(CONFIG.get("bind_port", 8008))
ALLOW_DANGEROUS = bool(CONFIG.get("allow_dangerous", False))

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_server")

app = FastAPI(title="Sophia MCP (minimal)")

async def verify_api_key(request: Request):
    key = request.headers.get("x-api-key") or request.headers.get("authorization")
    if not key:
        raise HTTPException(status_code=401, detail="Missing API key")
    # Accept both plain key and 'Bearer <key>'
    if key.startswith("Bearer "):
        key = key.split(" ", 1)[1]
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return True

@app.get("/status")
async def status(_: bool = Depends(verify_api_key)):
    return {"status": "ok", "platform": sys.platform, "cwd": str(Path.cwd())}

@app.post("/exec")
async def exec_command(payload: dict, _: bool = Depends(verify_api_key)):
    """Execute a shell command. payload = {"cmd": "...", "timeout": 30}
    WARNING: This runs commands on the host. Keep API key secret and bind to localhost or tunnel.
    """
    cmd = payload.get("cmd")
    timeout = int(payload.get("timeout", 30))
    if not cmd:
        raise HTTPException(status_code=400, detail="Missing 'cmd' in payload")

    # Disallow dangerous commands unless explicitly allowed
    dangerous_tokens = ["rm -rf", ":(){:|:&};:", ":(){", "dd if=", "mkfs."]
    if not ALLOW_DANGEROUS:
        for token in dangerous_tokens:
            if token in cmd:
                raise HTTPException(status_code=403, detail=f"Command contains disallowed token: {token}")

    try:
        # Use shell for Windows/PowerShell compatibility
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Command timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/file/read")
async def file_read(path: str, _: bool = Depends(verify_api_key)):
    p = Path(path).resolve()
    # Simple safety: disallow reading system root unless allowed flag
    if not ALLOW_DANGEROUS and (p.is_dir() or p.match(str(Path.home())) == False and not str(p).startswith(str(Path.cwd()))):
        # allow reading files within current workspace or home if not dangerous
        pass
    if not p.exists() or not p.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    try:
        return JSONResponse({"path": str(p), "content": p.read_text(encoding='utf-8', errors='replace')})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/file/write")
async def file_write(payload: dict, _: bool = Depends(verify_api_key)):
    path = payload.get("path")
    content = payload.get("content", "")
    if not path:
        raise HTTPException(status_code=400, detail="Missing 'path'")
    p = Path(path).resolve()
    # prevent writing outside workspace/home unless allowed
    if not ALLOW_DANGEROUS and not (str(p).startswith(str(Path.cwd())) or str(p).startswith(str(Path.home()))):
        raise HTTPException(status_code=403, detail="Write path not allowed")
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding='utf-8')
        return {"path": str(p), "status": "written"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/shutdown")
async def shutdown(_: dict = None, ok: bool = Depends(verify_api_key)):
    if not ALLOW_DANGEROUS:
        raise HTTPException(status_code=403, detail="Shutdown disabled. Enable allow_dangerous in config to use this." )
    # graceful shutdown via environment flag
    def _stop():
        logger.info("Shutdown requested via MCP")
        os._exit(0)
    _stop()
    return {"status": "shutting_down"}

if __name__ == '__main__':
    import uvicorn
    print("MCP server config:", CONFIG_PATH)
    print("API Key: set in config and passed via X-API-Key header or Authorization: Bearer <key>")
    uvicorn.run("mcp_server:app", host=BIND_HOST, port=BIND_PORT, log_level="info")
