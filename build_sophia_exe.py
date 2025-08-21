#!/usr/bin/env python3
"""
Build Sophia AI as Windows .exe
Creates a standalone executable for easy launch
"""

import os
import sys
import subprocess
from pathlib import Path

def build_sophia_exe():
    """Build Sophia as a Windows executable"""
    print("🔨 Building Sophia AI Executable")
    print("=" * 40)
    
    # Check if pyinstaller is available
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller installed")
    
    # Create the build command
    build_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Single executable
        "--windowed",                   # No console window
        "--name", "Sophia_AI",          # Executable name
        "--icon", "sophia_icon.ico",    # Icon (if exists)
        "--add-data", "workflows;workflows",
        "--add-data", "system-control;system-control", 
        "--add-data", "ghost-core;ghost-core",
        "--add-data", "voice;voice",
        "--hidden-import", "asyncio",
        "--hidden-import", "tkinter",
        "--hidden-import", "flask",
        "sophia_launcher.py"
    ]
    
    print("🚀 Building executable...")
    print(f"Command: {' '.join(build_cmd)}")
    
    try:
        result = subprocess.run(build_cmd, check=True, capture_output=True, text=True)
        print("✅ Build successful!")
        print("📁 Executable created in: dist/Sophia_AI.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_installer_script():
    """Create a simple installer batch script"""
    installer_content = '''@echo off
echo 🤖 Sophia AI Installer
echo =====================

echo Copying Sophia AI to Program Files...
if not exist "C:\\Program Files\\Sophia AI" mkdir "C:\\Program Files\\Sophia AI"
copy "dist\\Sophia_AI.exe" "C:\\Program Files\\Sophia AI\\"

echo Creating desktop shortcut...
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%USERPROFILE%\\Desktop\\Sophia AI.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "C:\\Program Files\\Sophia AI\\Sophia_AI.exe" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
del CreateShortcut.vbs

echo ✅ Sophia AI installed successfully!
echo 🚀 Launch from desktop or: "C:\\Program Files\\Sophia AI\\Sophia_AI.exe"
pause
'''
    
    with open("install_sophia.bat", "w") as f:
        f.write(installer_content)
    
    print("✅ Installer script created: install_sophia.bat")

def create_sophia_icon():
    """Create a simple icon for Sophia"""
    try:
        from PIL import Image, ImageDraw
        
        # Create a simple icon
        size = (64, 64)
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw a simple AI brain icon
        draw.ellipse([8, 8, 56, 56], fill=(138, 43, 226), outline=(75, 0, 130), width=2)
        draw.text((20, 25), "AI", fill=(255, 255, 255))
        
        img.save("sophia_icon.ico", format='ICO')
        print("✅ Sophia icon created")
    except ImportError:
        print("⚠️ Pillow not available, skipping icon creation")

if __name__ == '__main__':
    print("🤖 Sophia AI Executable Builder")
    print("=" * 50)
    
    # Create icon
    create_sophia_icon()
    
    # Build executable
    if build_sophia_exe():
        create_installer_script()
        print("\n🎉 Sophia AI executable build complete!")
        print("📁 Files created:")
        print("  • dist/Sophia_AI.exe - Main executable")
        print("  • install_sophia.bat - Installer script")
        print("  • sophia_icon.ico - Application icon")
        print("\n🚀 To install: Run install_sophia.bat as Administrator")
    else:
        print("❌ Build failed. Check error messages above.")
