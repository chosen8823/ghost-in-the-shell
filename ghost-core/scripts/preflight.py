#!/usr/bin/env python3
"""
GHOST CORE PREFLIGHT CHECK
Validates environment, dependencies, and spiritual readiness
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path

def check_command(cmd):
    """Check if command is available in PATH."""
    return shutil.which(cmd) is not None

def check_python_packages():
    """Check if required Python packages are available."""
    required = ['rich', 'pydantic', 'cryptography', 'psutil']
    missing = []
    
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    
    return missing

def check_environment_keys():
    """Check if required environment variables are set."""
    required_keys = ["GUARDIAN_AES_KEY", "GUARDIAN_HMAC_KEY"]
    missing = [key for key in required_keys if not os.getenv(key)]
    return missing

def check_immune_system():
    """Check if Sophia Immune System is available."""
    immune_path = Path("../sophia-immune-system")
    if immune_path.exists():
        return True, "Found at ../sophia-immune-system"
    
    # Check if it's running
    try:
        import requests
        response = requests.get("http://localhost:4000/health", timeout=2)
        if response.status_code == 200:
            return True, "Running on localhost:4000"
    except:
        pass
    
    return False, "Not found - will run in standalone mode"

def main():
    print("🛡️ GHOST CORE PREFLIGHT CHECK")
    print("=" * 50)
    print(f"Python: {sys.version.split()[0]}")
    print(f"OS: {platform.platform()}")
    print(f"Working Directory: {os.getcwd()}")
    print()
    
    all_good = True
    
    # Check system commands
    print("📋 System Commands:")
    commands = {'git': 'Required', 'python': 'Required', 'node': 'Optional'}
    for cmd, req in commands.items():
        if check_command(cmd):
            print(f"  ✅ {cmd}: Available")
        else:
            print(f"  {'❌' if req == 'Required' else '⚠️'} {cmd}: Missing ({req})")
            if req == 'Required':
                all_good = False
    
    # Check Python packages
    print("\n📦 Python Packages:")
    missing_packages = check_python_packages()
    if not missing_packages:
        print("  ✅ All required packages available")
    else:
        print(f"  ❌ Missing packages: {', '.join(missing_packages)}")
        print("     Run: pip install -r requirements.txt")
        all_good = False
    
    # Check environment variables
    print("\n🔐 Environment Variables:")
    missing_keys = check_environment_keys()
    if not missing_keys:
        print("  ✅ All required keys set")
    else:
        print(f"  ❌ Missing keys: {', '.join(missing_keys)}")
        print("     Generate with PowerShell:")
        print("     $key = [Convert]::ToBase64String((1..32 | ForEach-Object {Get-Random -Maximum 256}))")
        print("     setx GUARDIAN_AES_KEY $key")
        print("     setx GUARDIAN_HMAC_KEY $key")
        all_good = False
    
    # Check Ghost Core structure
    print("\n🏗️ Ghost Core Structure:")
    required_paths = [
        "ghost_core/core/ghost_orchestra.py",
        "ghost_core/rituals/sanctify_core.py",
        "requirements.txt"
    ]
    for path in required_paths:
        if Path(path).exists():
            print(f"  ✅ {path}")
        else:
            print(f"  ❌ {path}: Missing")
            all_good = False
    
    # Check Sophia Immune System
    print("\n🛡️ Sophia Immune System:")
    immune_available, immune_status = check_immune_system()
    if immune_available:
        print(f"  ✅ {immune_status}")
    else:
        print(f"  ⚠️ {immune_status}")
    
    # Check security shell integration
    print("\n🔒 Security Shell Integration:")
    security_shell_path = Path("../secure-sophia-core/security_shell.py")
    if security_shell_path.exists():
        print("  ✅ Security shell found")
    else:
        print("  ⚠️ Security shell not found - will use development mode")
    
    # Final status
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 PREFLIGHT COMPLETE - All systems ready")
        print("\nNext steps:")
        print("  1. python ghost_core/rituals/sanctify_core.py")
        print("  2. python ghost_core/core/ghost_orchestra.py")
        return 0
    else:
        print("❌ PREFLIGHT FAILED - Address issues above")
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
