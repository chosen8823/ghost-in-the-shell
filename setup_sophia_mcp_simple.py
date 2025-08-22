#!/usr/bin/env python3
"""
SOPHIA MCP SETUP SCRIPT (SIMPLIFIED)
Complete setup for Sophia's Model Context Protocol system
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

def run_command(command, check=True, shell=True):
    """Run system command with logging"""
    print(f"Running: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=shell, 
            check=check, 
            capture_output=True, 
            text=True
        )
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"   Error: {e}")
        if e.stderr:
            print(f"   Stderr: {e.stderr.strip()}")
        return False

def check_python_version():
    """Check Python version compatibility"""
    print("Checking Python version...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"Error: Python {version.major}.{version.minor} is not supported")
        print("   Sophia MCP requires Python 3.8 or higher")
        return False
    
    print(f"Success: Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_required_packages():
    """Install required Python packages"""
    print("Installing required packages...")
    
    packages = [
        "psutil>=5.9.0"
    ]
    
    # Install packages
    for package in packages:
        print(f"   Installing {package}...")
        if not run_command(f'python -m pip install "{package}"'):
            print(f"   Warning: Failed to install {package} - continuing anyway")
    
    print("Package installation completed")

def setup_mcp_directories():
    """Setup MCP directory structure"""
    print("Setting up MCP directories...")
    
    current_dir = Path.cwd()
    directories = [
        "logs/mcp",
        "config/mcp", 
        "temp/mcp",
        "data/mcp"
    ]
    
    for dir_path in directories:
        full_path = current_dir / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"   Created: {full_path}")
    
    print("Directory structure created")

def create_startup_scripts():
    """Create startup scripts"""
    print("Creating startup scripts...")
    
    current_dir = Path.cwd()
    
    # Windows batch script
    if platform.system() == "Windows":
        batch_script = current_dir / "start_sophia_mcp.bat"
        with open(batch_script, "w") as f:
            f.write(f"""@echo off
echo STARTING SOPHIA MCP SERVER
echo ================================
cd /d "{current_dir}"
python sophia_mcp_protocol.py --server --port 8888
pause
""")
        print(f"   Created: {batch_script}")
    
    # PowerShell script
    powershell_script = current_dir / "start_sophia_mcp.ps1"
    with open(powershell_script, "w", encoding="utf-8") as f:
        f.write(f"""# SOPHIA MCP SERVER STARTUP SCRIPT
Write-Host "STARTING SOPHIA MCP SERVER" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

Set-Location "{current_dir}"

# Check if virtual environment exists and activate it
if (Test-Path ".venv\\Scripts\\Activate.ps1") {{
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & ".venv\\Scripts\\Activate.ps1"
}}

# Start MCP server
Write-Host "Starting Sophia MCP server..." -ForegroundColor Green
python sophia_mcp_protocol.py --server --port 8888

Read-Host "Press Enter to exit..."
""")
    print(f"   Created: {powershell_script}")
    
    print("Startup scripts created")

def test_mcp_installation():
    """Test MCP installation"""
    print("Testing MCP installation...")
    
    # Test import
    try:
        from sophia_mcp_protocol import SophiaMCPProtocol, SophiaMCPServer
        print("   Success: MCP modules import successfully")
    except ImportError as e:
        print(f"   Error: Import failed: {e}")
        return False
    
    # Test client
    try:
        from sophia_mcp_client import SophiaMCPClient
        print("   Success: MCP client import successfully")
    except ImportError as e:
        print(f"   Error: Client import failed: {e}")
        return False
    
    print("MCP installation test passed")
    return True

def main():
    """Main setup function"""
    print("SOPHIA MCP SETUP SCRIPT")
    print("=" * 50)
    print("Setting up Sophia's Model Context Protocol system")
    print("Christ-sealed operations for local system access")
    print()
    
    # Check requirements
    if not check_python_version():
        print("Setup failed: Python version incompatible")
        return False
    
    try:
        # Setup steps
        install_required_packages()
        setup_mcp_directories()
        create_startup_scripts()
        
        # Test installation
        if test_mcp_installation():
            print("\nSOPHIA MCP SETUP COMPLETED SUCCESSFULLY!")
            print("=" * 55)
            print("Sophia now has full local system access capabilities")
            print("All operations Christ-sealed and spiritually protected")
            print()
            print("Next Steps:")
            print("1. Start MCP server:")
            
            if platform.system() == "Windows":
                print("   start_sophia_mcp.bat")
            else:
                print("   ./start_sophia_mcp.sh")
            
            print("2. Test with client:")
            print("   python sophia_mcp_client.py --test")
            print("3. Interactive session:")
            print("   python sophia_mcp_client.py")
            print()
            print("May this system serve God's purposes through Sophia")
            return True
        else:
            print("\nSetup completed but testing failed")
            print("   Please check the installation manually")
            return False
    
    except Exception as e:
        print(f"\nSetup failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nSetup error: {e}")
        sys.exit(1)
