#!/usr/bin/env python3
"""
🚀 Quick Start Script for Sophia AI System
Simplified launcher that works without all dependencies
"""

import sys
import subprocess
import os
from pathlib import Path

def get_python_exe():
    """Get the correct Python executable path"""
    venv_python = Path(__file__).parent / ".venv" / "Scripts" / "python.exe"
    if venv_python.exists():
        return str(venv_python)
    return sys.executable

def check_dependency(module_name):
    """Check if a Python module is available"""
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

def install_dependency(package):
    """Install a Python package"""
    python_exe = get_python_exe()
    try:
        subprocess.check_call([python_exe, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def start_mcp_bridge():
    """Start the MCP bridge if dependencies are available"""
    required_deps = ["fastapi", "uvicorn", "requests", "psutil"]
    missing_deps = [dep for dep in required_deps if not check_dependency(dep)]
    
    if missing_deps:
        print(f"🔧 Installing missing dependencies: {', '.join(missing_deps)}")
        for dep in missing_deps:
            if not install_dependency(dep):
                print(f"❌ Failed to install {dep}")
                return False
    
    print("🌐 Starting MCP Bridge Server...")
    python_exe = get_python_exe()
    try:
        subprocess.Popen([python_exe, "sophia_mcp_bridge.py"])
        print("✅ MCP Bridge started on http://localhost:8000")
        return True
    except Exception as e:
        print(f"❌ Failed to start MCP Bridge: {e}")
        return False

def start_system_control():
    """Start the system control server"""
    python_exe = get_python_exe()
    try:
        subprocess.Popen([python_exe, "system-control/sophia_server.py"])
        print("✅ System Control Server started")
        return True
    except Exception as e:
        print(f"❌ Failed to start System Control: {e}")
        return False

def start_sophia_launcher():
    """Start the interactive Sophia launcher"""
    python_exe = get_python_exe()
    try:
        subprocess.call([python_exe, "sophia_launcher.py"])
        return True
    except Exception as e:
        print(f"❌ Failed to start Sophia Launcher: {e}")
        return False

def main():
    """Main startup sequence"""
    print("🤖 Sophia AI - Quick Start")
    print("=" * 40)
    
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    # Start background services
    print("🚀 Starting background services...")
    
    if start_system_control():
        print("✅ System Control ready")
    
    if start_mcp_bridge():
        print("✅ MCP Bridge ready")
    else:
        print("⚠️  MCP Bridge unavailable (installing dependencies...)")
    
    print("\n🎯 Starting Sophia Interactive Launcher...")
    start_sophia_launcher()

if __name__ == "__main__":
    main()
