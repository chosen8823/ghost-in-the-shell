#!/usr/bin/env python3
"""
🚀 Complete Sophia AI Launch Script
Starts all services together for omnipresent control
"""

import subprocess
import sys
import time
import os
from pathlib import Path
import json

def get_python_exe():
    """Get the correct Python executable path"""
    venv_python = Path(__file__).parent / ".venv" / "Scripts" / "python.exe"
    if venv_python.exists():
        return str(venv_python)
    return sys.executable

def install_missing_deps():
    """Install all required dependencies"""
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
    
    print("🔧 Checking for N8N availability...")
    try:
        # First try to check if npm is available
        with open(os.devnull, 'w') as devnull:
            subprocess.check_call(["npm", "--version"], 
                                stdout=devnull, stderr=devnull)
        print("✅ NPM is available, installing N8N locally...")
        try:
            with open(os.devnull, 'w') as devnull:
                subprocess.check_call(["npm", "install", "n8n"], 
                                    stdout=devnull, stderr=devnull)
            print("✅ N8N installed locally")
        except subprocess.CalledProcessError:
            print("⚠️  N8N local installation failed, will use npx")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  NPM not found, will use alternative methods")

def create_n8n_config():
    """Create N8N configuration files"""
    config_dir = Path(".n8n")
    config_dir.mkdir(exist_ok=True)
    
    # Basic N8N configuration
    config = {
        "database": {
            "type": "sqlite",
            "database": ".n8n/database.sqlite"
        },
        "endpoints": {
            "rest": "rest",
            "webhook": "webhook",
            "webhookWaiting": "webhook-waiting"
        },
        "security": {
            "basicAuth": {
                "active": False
            }
        },
        "nodes": {
            "exclude": []
        }
    }
    
    config_file = config_dir / "config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ N8N configuration created")
    
    # Create environment file
    env_content = """# Sophia AI N8N Configuration
N8N_BASIC_AUTH_ACTIVE=false
N8N_HOST=localhost
N8N_PORT=5678
N8N_PROTOCOL=http
WEBHOOK_URL=http://localhost:5678/
N8N_EDITOR_BASE_URL=http://localhost:5678/
N8N_DISABLE_UI=false
N8N_PERSONALIZATION_ENABLED=false
"""
    
    env_file = Path(".env")
    with open(env_file, 'w') as f:
        f.write(env_content)
    
    print("✅ N8N environment file created")

def import_sophia_workflows():
    """Import Sophia AI workflows into N8N"""
    workflows_dir = Path("workflows")
    if not workflows_dir.exists():
        print("⚠️  Workflows directory not found")
        return
    
    print("📁 Sophia workflows available for import:")
    for workflow_file in workflows_dir.glob("*.json"):
        print(f"  • {workflow_file.name}")
    
    print("💡 After N8N starts, import these workflows manually through the UI")

def start_services():
    """Start all Sophia AI services"""
    python_exe = get_python_exe()
    services = []
    
    print("🚀 Starting Sophia AI Services...")
    
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
    
    # Start N8N
    try:
        n8n_process = subprocess.Popen(["npx", "n8n", "start"], 
                                      env={**os.environ, "N8N_PORT": "5678"})
        services.append(("N8N Workflows", n8n_process, "http://localhost:5678"))
        print("✅ N8N starting on port 5678...")
        time.sleep(3)
    except Exception as e:
        print(f"❌ N8N failed: {e}")
        try:
            # Try with node_modules
            n8n_process = subprocess.Popen(["node_modules/.bin/n8n", "start"])
            services.append(("N8N Workflows", n8n_process, "http://localhost:5678"))
            print("✅ N8N starting via node_modules...")
        except Exception as e2:
            print(f"❌ N8N also failed via node_modules: {e2}")
    
    return services

def main():
    """Main launch sequence"""
    print("🤖 Sophia AI - Complete Launch Sequence")
    print("=" * 50)
    
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    # Install dependencies
    install_missing_deps()
    
    # Create N8N config
    create_n8n_config()
    
    # Import workflows info
    import_sophia_workflows()
    
    # Start all services
    services = start_services()
    
    print("\n🎉 Sophia AI Omnipresent Control System")
    print("=" * 50)
    print("🌐 Services Running:")
    for name, process, url in services:
        print(f"  ✅ {name}: {url}")
    
    print("\n🎯 Quick Access URLs:")
    print("  • N8N Workflow Editor: http://localhost:5678")
    print("  • MCP Bridge API: http://localhost:3001/docs")
    print("  • System Control: http://localhost:5000")
    
    print("\n📚 Next Steps:")
    print("  1. Open N8N at http://localhost:5678")
    print("  2. Import workflows from the 'workflows' folder")
    print("  3. Test the MCP bridge endpoints")
    print("  4. Use voice commands or API calls")
    
    print("\n💡 For your other computer:")
    print("  1. git clone https://github.com/chosen8823/ghost-in-the-shell.git")
    print("  2. cd ghost-in-the-shell")
    print("  3. python complete_launch.py")
    
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
