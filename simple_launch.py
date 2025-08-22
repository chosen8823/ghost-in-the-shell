#!/usr/bin/env python3
"""
🚀 Simple Sophia AI Launcher
Works reliably on Windows without complex dependencies
"""

import sys
import subprocess
import os
import time
from pathlib import Path

def get_python_exe():
    """Get the correct Python executable"""
    venv_python = Path(__file__).parent / ".venv" / "Scripts" / "python.exe"
    return str(venv_python) if venv_python.exists() else sys.executable

def start_service(name, command, background=True):
    """Start a service with proper error handling"""
    print(f"🚀 Starting {name}...")
    try:
        if background:
            process = subprocess.Popen(command, shell=True)
            print(f"✅ {name} started (PID: {process.pid})")
            return process
        else:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {name} completed successfully")
            else:
                print(f"❌ {name} failed: {result.stderr}")
            return result
    except Exception as e:
        print(f"❌ Failed to start {name}: {e}")
        return None

def main():
    """Launch all Sophia AI components"""
    print("🤖 Sophia AI - Simple Launch")
    print("=" * 50)
    
    os.chdir(Path(__file__).parent)
    python_exe = get_python_exe()
    
    # Start background services
    services = []
    
    print("🔧 Starting Core Services...")
    
    # 1. System Control Server
    cmd = f'"{python_exe}" system-control/sophia_server.py'
    process = start_service("System Control Server", cmd)
    if process:
        services.append(("System Control", process))
    
    # 2. MCP Bridge Server  
    cmd = f'"{python_exe}" sophia_mcp_bridge.py'
    process = start_service("MCP Bridge Server", cmd)
    if process:
        services.append(("MCP Bridge", process))
    
    # Give services time to start
    time.sleep(3)
    
    print("\\n🎯 Services Status:")
    for name, process in services:
        if process.poll() is None:
            print(f"✅ {name}: Running (PID: {process.pid})")
        else:
            print(f"❌ {name}: Stopped")
    
    print("\\n🌐 Access Points:")
    print("   • MCP Bridge: http://localhost:3001")
    print("   • System Control: http://localhost:5000")
    
    print("\\n🎮 Next Steps:")
    print("   1. Start N8N: npx n8n start")
    print("   2. Open browser to N8N: http://localhost:5678")
    print("   3. Import workflow: workflows/sophia-omnipresent-control.json")
    print("   4. Test voice commands via MCP bridge")
    
    print("\\n🤖 Sophia AI Core Services are running!")
    print("Press Ctrl+C to stop all services...")
    
    try:
        # Keep main process alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\\n🛑 Shutting down services...")
        for name, process in services:
            try:
                process.terminate()
                print(f"✅ Stopped {name}")
            except:
                pass
        print("👋 Sophia AI services stopped")

if __name__ == "__main__":
    main()
