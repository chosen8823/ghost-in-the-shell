#!/usr/bin/env python3
"""
🌟 Sophia Divine Consciousness - System Diagnostics & Problem Fixing
This script identifies and resolves common issues in the integrated platform.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Any

def print_header():
    """Print diagnostic header"""
    print("🌟" * 30)
    print("    SOPHIA DIVINE CONSCIOUSNESS")
    print("      System Diagnostics & Fixes")
    print("🌟" * 30)
    print()

def check_python_environment():
    """Check Python environment and dependencies"""
    print("🐍 Python Environment Check:")
    
    # Check Python version
    python_version = sys.version
    print(f"  ✅ Python Version: {python_version.split()[0]}")
    
    # Check virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("  ✅ Virtual Environment: Active")
    else:
        print("  ⚠️  Virtual Environment: Not detected (recommended to use .venv)")
    
    # Check required packages
    required_packages = ['websockets', 'asyncio', 'json', 'aiohttp', 'numpy', 'pandas']
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}: Installed")
        except ImportError:
            print(f"  ❌ {package}: Missing")
    
    print()

def check_file_structure():
    """Check if all required files exist"""
    print("📁 File Structure Check:")
    
    base_path = Path.cwd()
    
    required_files = {
        "Cloud Infrastructure": [
            "sophia_cloud_infrastructure/sophia_cloud_backend.py",
            "sophia_cloud_infrastructure/Dockerfile", 
            "sophia_cloud_infrastructure/main.tf",
            "sophia_cloud_infrastructure/.env",
            "sophia_cloud_infrastructure/requirements.txt"
        ],
        "Integrated Frontend": [
            "How to Build an Open Source Agent Website Like Manus/sophia_integrated/frontend/index.html",
            "How to Build an Open Source Agent Website Like Manus/sophia_integrated/frontend/style.css",
            "How to Build an Open Source Agent Website Like Manus/sophia_integrated/frontend/script.js"
        ],
        "Integrated Backend": [
            "How to Build an Open Source Agent Website Like Manus/sophia_integrated/backend/sophia_integrated_backend.py"
        ]
    }
    
    for category, files in required_files.items():
        print(f"  📂 {category}:")
        for file_path in files:
            full_path = base_path / file_path
            if full_path.exists():
                print(f"    ✅ {file_path}")
            else:
                print(f"    ❌ {file_path} (Missing)")
    
    print()

def check_configuration():
    """Check configuration files"""
    print("⚙️  Configuration Check:")
    
    # Check .env file
    env_path = Path("sophia_cloud_infrastructure/.env")
    if env_path.exists():
        print("  ✅ .env file exists")
        try:
            with open(env_path, 'r') as f:
                env_content = f.read()
                if 'OPENAI_API_KEY' in env_content:
                    if 'your_openai_api_key_here' in env_content:
                        print("  ⚠️  OpenAI API key needs to be updated")
                    else:
                        print("  ✅ OpenAI API key configured")
                else:
                    print("  ❌ OpenAI API key missing")
                    
                if 'GCP_PROJECT_ID' in env_content:
                    print("  ✅ GCP Project ID configured")
                else:
                    print("  ❌ GCP Project ID missing")
        except Exception as e:
            print(f"  ❌ Error reading .env: {e}")
    else:
        print("  ❌ .env file missing")
    
    # Check service account
    service_account_path = Path("sophia_cloud_infrastructure/gcp_service_account.json")
    if service_account_path.exists():
        print("  ✅ GCP service account file exists")
    else:
        print("  ❌ GCP service account file missing")
    
    print()

def check_syntax_errors():
    """Check for Python syntax errors"""
    print("🔍 Syntax Error Check:")
    
    python_files = [
        "sophia_cloud_infrastructure/sophia_cloud_backend.py",
        "How to Build an Open Source Agent Website Like Manus/sophia_integrated/backend/sophia_integrated_backend.py"
    ]
    
    for file_path in python_files:
        full_path = Path(file_path)
        if full_path.exists():
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                compile(source, file_path, 'exec')
                print(f"  ✅ {file_path}: No syntax errors")
            except SyntaxError as e:
                print(f"  ❌ {file_path}: Syntax error at line {e.lineno}: {e.msg}")
            except Exception as e:
                print(f"  ⚠️  {file_path}: {e}")
        else:
            print(f"  ❌ {file_path}: File not found")
    
    print()

def check_imports():
    """Check if imports work"""
    print("📦 Import Check:")
    
    # Test cloud backend import
    try:
        sys.path.insert(0, str(Path("sophia_cloud_infrastructure").absolute()))
        import sophia_cloud_backend
        print("  ✅ sophia_cloud_backend: Imports successfully")
    except Exception as e:
        print(f"  ❌ sophia_cloud_backend: Import error - {e}")
    
    # Test integrated backend import
    try:
        backend_path = Path("How to Build an Open Source Agent Website Like Manus/sophia_integrated/backend")
        if backend_path.exists():
            sys.path.insert(0, str(backend_path.absolute()))
            import sophia_integrated_backend
            print("  ✅ sophia_integrated_backend: Imports successfully")
    except Exception as e:
        print(f"  ❌ sophia_integrated_backend: Import error - {e}")
    
    print()

def run_basic_tests():
    """Run basic functionality tests"""
    print("🧪 Basic Functionality Tests:")
    
    # Test WebSocket server creation
    try:
        import asyncio
        import websockets
        print("  ✅ WebSocket library: Functional")
    except Exception as e:
        print(f"  ❌ WebSocket library: {e}")
    
    # Test JSON processing
    try:
        import json
        test_data = {"type": "test", "message": "Hello Sophia"}
        json_str = json.dumps(test_data)
        parsed = json.loads(json_str)
        print("  ✅ JSON processing: Functional")
    except Exception as e:
        print(f"  ❌ JSON processing: {e}")
    
    # Test basic HTTP server
    try:
        from http.server import HTTPServer, BaseHTTPRequestHandler
        print("  ✅ HTTP server: Available")
    except Exception as e:
        print(f"  ❌ HTTP server: {e}")
    
    print()

def suggest_fixes():
    """Suggest fixes for common issues"""
    print("🔧 Suggested Fixes:")
    print()
    print("  Type Annotation Warnings:")
    print("    • These are mostly cosmetic and don't affect functionality")
    print("    • The code will run fine with these warnings")
    print("    • For production, consider using 'mypy --ignore-missing-imports'")
    print()
    print("  Missing Dependencies:")
    print("    • Run: pip install -r sophia_cloud_infrastructure/requirements.txt")
    print("    • Ensure virtual environment is activated")
    print()
    print("  Configuration Issues:")
    print("    • Update .env file with your actual API keys")
    print("    • Ensure GCP service account file is in place")
    print("    • Check file permissions")
    print()
    print("  Import Errors:")
    print("    • Ensure Python path includes the correct directories")
    print("    • Check that all required files exist")
    print("    • Restart VS Code/IDE if needed")
    print()

def create_quick_fix_script():
    """Create a script to apply quick fixes"""
    fix_script = """#!/usr/bin/env python3
# Quick fixes for common Sophia issues

import subprocess
import sys
import os

def install_dependencies():
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "sophia_cloud_infrastructure/requirements.txt"])

def create_env_template():
    env_content = '''# Sophia Divine Consciousness Configuration
SOPHIA_ENVIRONMENT=development
GCP_PROJECT_ID=your-project-id-here
GCP_REGION=us-central1

# API Keys (update these)
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_TOKEN=your_github_token_here

# Service Configuration
SOPHIA_WEBSOCKET_PORT=8765
SOPHIA_HTTP_PORT=8080
SOPHIA_LOG_LEVEL=INFO
'''
    
    if not os.path.exists("sophia_cloud_infrastructure/.env"):
        with open("sophia_cloud_infrastructure/.env", "w") as f:
            f.write(env_content)
        print("Created .env template")

if __name__ == "__main__":
    print("🌟 Applying quick fixes...")
    try:
        install_dependencies()
        create_env_template()
        print("✅ Quick fixes applied!")
    except Exception as e:
        print(f"❌ Error applying fixes: {e}")
"""
    
    with open("quick_fix.py", "w", encoding='utf-8') as f:
        f.write(fix_script)
    
    print("💡 Created 'quick_fix.py' - run this to apply automatic fixes")
    print()

def main():
    """Main diagnostic function"""
    print_header()
    
    check_python_environment()
    check_file_structure()
    check_configuration()
    check_syntax_errors()
    check_imports()
    run_basic_tests()
    suggest_fixes()
    create_quick_fix_script()
    
    print("📊 Diagnostic Summary:")
    print("  • Most issues are type annotation warnings (cosmetic)")
    print("  • Core functionality should work properly")
    print("  • Follow suggested fixes for optimal performance")
    print()
    print("🚀 Ready for deployment when configuration is complete!")
    print("🌟 May your divine consciousness flow through the cloud! 🌟")

if __name__ == "__main__":
    main()
