#!/usr/bin/env python3
"""
🚀 Sophia AI Launch Script (Without N8N dependency)
Starts core services for testing and development
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def get_python_exe():
    """Get the correct Python executable path"""
    venv_python = Path(__file__).parent / ".venv" / "Scripts" / "python.exe"
    if venv_python.exists():
        return str(venv_python)
    # Use the Python3.13 executable that has the packages installed
    python313_path = "C:/Users/secure-channel/AppData/Local/Microsoft/WindowsApps/python3.13.exe"
    if Path(python313_path).exists():
        return python313_path
    return sys.executable

def install_python_deps():
    """Install Python dependencies only"""
    python_exe = get_python_exe()
    
    print("🔧 Installing Python dependencies...")
    python_deps = [
        "fastapi", "uvicorn", "requests", "psutil", "pydantic",
        "flask", "pillow", "pyautogui", "keyboard", "mouse"
    ]
    
    for dep in python_deps:
        try:
            with open(os.devnull, 'w') as devnull:
                subprocess.check_call([python_exe, "-m", "pip", "install", dep], 
                                    stdout=devnull, stderr=devnull)
            print(f"✅ Installed {dep}")
        except subprocess.CalledProcessError:
            print(f"⚠️  {dep} installation skipped (may already exist)")

def start_core_services():
    """Start core Sophia AI services (without N8N)"""
    python_exe = get_python_exe()
    services = []
    
    print("🚀 Starting Core Sophia AI Services...")
    
    # Start MCP Bridge
    try:
        mcp_process = subprocess.Popen([python_exe, "sophia_mcp_bridge.py"])
        services.append(("MCP Bridge", mcp_process, "http://localhost:3001"))
        print("✅ MCP Bridge starting on port 3001...")
        time.sleep(2)
    except Exception as e:
        print(f"❌ MCP Bridge failed: {e}")
    
    # Start System Control
    try:
        sys_process = subprocess.Popen([python_exe, "system-control/sophia_server.py"])
        services.append(("System Control", sys_process, "http://localhost:5000"))
        print("✅ System Control starting on port 5000...")
        time.sleep(2)
    except Exception as e:
        print(f"❌ System Control failed: {e}")
    
    # Start Node.js server (if available)
    try:
        server_process = subprocess.Popen(["node", "server/index.js"])
        services.append(("Node.js Server", server_process, "http://localhost:3000"))
        print("✅ Node.js Server starting on port 3000...")
        time.sleep(2)
    except Exception as e:
        print(f"⚠️  Node.js Server not available: {e}")
    
    return services

def main():
    """Main launch function"""
    print("🤖 Sophia AI - Core Services Launch")
    print("=" * 50)
    
    # Install dependencies
    install_python_deps()
    
    # Start services
    services = start_core_services()
    
    if not services:
        print("❌ No services started successfully")
        return
    
    print("\n🎉 Core Services Status:")
    for name, process, url in services:
        status = "RUNNING" if process.poll() is None else "STOPPED"
        print(f"  ✅ {name}: {status} - {url}")
    
    print("\n🎯 Quick Access URLs:")
    print("  • MCP Bridge API: http://localhost:3001/docs")
    print("  • System Control: http://localhost:5000")
    if any("Node.js" in name for name, _, _ in services):
        print("  • Node.js Server: http://localhost:3000")
    
    print("\n📚 Next Steps:")
    print("  1. Install Node.js to enable N8N workflows")
    print("  2. Test the MCP bridge endpoints")
    print("  3. Use system control for device automation")
    
    print("\n🛑 Press Ctrl+C to stop all services")
    
    try:
        # Keep running until interrupted
        while True:
            time.sleep(10)
            # Check if services are still running
            running_count = sum(1 for _, proc, _ in services if proc.poll() is None)
            if running_count == 0:
                print("⚠️  All services stopped")
                break
    except KeyboardInterrupt:
        print("\n🛑 Stopping all services...")
        for name, process, _ in services:
            try:
                process.terminate()
                print(f"✅ Stopped {name}")
            except:
                pass

if __name__ == "__main__":
    main()
