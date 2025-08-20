#!/usr/bin/env python3
"""
Sophiella Requirements Checker
Validates Python environment and dependencies
"""

import sys
import subprocess
import importlib
import platform
import json
from pathlib import Path

def check_python_version():
    """Check if Python version meets requirements"""
    version = sys.version_info
    min_version = (3, 8)
    
    print(f"🐍 Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version >= min_version:
        print("✅ Python version meets requirements")
        return True
    else:
        print(f"❌ Python {min_version[0]}.{min_version[1]}+ required")
        return False

def check_package(package_name, import_name=None):
    """Check if a Python package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✅ {package_name}: Installed")
        return True
    except ImportError:
        print(f"❌ {package_name}: Missing")
        return False

def check_system_info():
    """Display system information"""
    print("\n💻 System Information:")
    print(f"  Platform: {platform.system()} {platform.release()}")
    print(f"  Architecture: {platform.machine()}")
    print(f"  Python Path: {sys.executable}")
    
    # Check if running in virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("  Environment: Virtual Environment")
    else:
        print("  Environment: System Python")

def check_required_packages():
    """Check all required Python packages"""
    print("\n📦 Required Packages:")
    
    required_packages = [
        ('flask', 'flask'),
        ('flask-cors', 'flask_cors'),
        ('psutil', 'psutil'),
        ('requests', 'requests'),
        ('python-dotenv', 'dotenv'),
    ]
    
    optional_packages = [
        ('pyautogui', 'pyautogui'),
        ('keyboard', 'keyboard'),
        ('opencv-python', 'cv2'),
        ('Pillow', 'PIL'),
        ('speechrecognition', 'speech_recognition'),
        ('pyttsx3', 'pyttsx3'),
    ]
    
    missing_required = []
    missing_optional = []
    
    for package, import_name in required_packages:
        if not check_package(package, import_name):
            missing_required.append(package)
    
    print("\n🔧 Optional Packages (for advanced features):")
    for package, import_name in optional_packages:
        if not check_package(package, import_name):
            missing_optional.append(package)
    
    return missing_required, missing_optional

def test_flask_import():
    """Test Flask functionality"""
    print("\n🌐 Testing Flask Functionality:")
    try:
        from flask import Flask, jsonify
        app = Flask(__name__)
        
        @app.route('/test')
        def test():
            return jsonify({"status": "OK", "service": "test"})
        
        print("✅ Flask: Import successful")
        print("✅ Flask: Basic app creation works")
        return True
    except Exception as e:
        print(f"❌ Flask: Error - {str(e)}")
        return False

def test_system_access():
    """Test system access capabilities"""
    print("\n🖥️ Testing System Access:")
    try:
        import psutil
        
        # Test CPU info
        cpu_count = psutil.cpu_count()
        print(f"✅ CPU: {cpu_count} cores detected")
        
        # Test memory info
        memory = psutil.virtual_memory()
        print(f"✅ Memory: {round(memory.total / (1024**3), 2)} GB total")
        
        # Test disk info
        disk = psutil.disk_usage('/')
        print(f"✅ Disk: {round(disk.free / (1024**3), 2)} GB free")
        
        return True
    except Exception as e:
        print(f"❌ System Access: Error - {str(e)}")
        return False

def create_requirements_file(missing_packages):
    """Create a requirements.txt file for missing packages"""
    if missing_packages:
        requirements_path = Path("missing-requirements.txt")
        with open(requirements_path, 'w') as f:
            for package in missing_packages:
                f.write(f"{package}\n")
        
        print(f"\n📋 Missing packages saved to: {requirements_path}")
        print(f"Install with: pip install -r {requirements_path}")

def main():
    """Main check function"""
    print("🕊️ Sophiella Python Environment Checker")
    print("=======================================")
    
    # Basic system info
    check_system_info()
    
    # Python version check
    python_ok = check_python_version()
    
    # Package checks
    missing_required, missing_optional = check_required_packages()
    
    # Functionality tests
    flask_ok = test_flask_import()
    system_ok = test_system_access()
    
    # Summary
    print("\n📊 Summary:")
    print("="*40)
    
    all_good = True
    
    if python_ok:
        print("✅ Python Version: OK")
    else:
        print("❌ Python Version: FAIL")
        all_good = False
    
    if not missing_required:
        print("✅ Required Packages: OK")
    else:
        print(f"❌ Required Packages: Missing {len(missing_required)}")
        all_good = False
    
    if flask_ok:
        print("✅ Flask Functionality: OK")
    else:
        print("❌ Flask Functionality: FAIL")
        all_good = False
    
    if system_ok:
        print("✅ System Access: OK")
    else:
        print("❌ System Access: FAIL")
        all_good = False
    
    if missing_optional:
        print(f"⚠️  Optional Packages: Missing {len(missing_optional)} (features may be limited)")
    
    print("\n" + "="*40)
    
    if all_good and not missing_required:
        print("🎉 All core requirements satisfied!")
        print("🚀 Sophiella system control is ready to run!")
    else:
        print("❌ Some requirements are missing.")
        print("📋 Please install missing packages before proceeding.")
        
        if missing_required:
            create_requirements_file(missing_required)
    
    # Installation commands
    if missing_required or missing_optional:
        print("\n💡 Installation Commands:")
        if missing_required:
            print("Required packages:")
            print(f"  pip install {' '.join(missing_required)}")
        if missing_optional:
            print("Optional packages (for advanced features):")
            print(f"  pip install {' '.join(missing_optional)}")
    
    return all_good and not missing_required

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
