#!/usr/bin/env python3
"""
🌟 Sophia Omnipresent Control Launcher
Complete voice + vision + system control interface
"""

import subprocess
import sys
import time
import threading
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

def start_voice_interface():
    """Start the voice interface"""
    python_exe = get_python_exe()
    print("🎤 Starting Sophia Voice Interface...")
    
    try:
        voice_process = subprocess.Popen([python_exe, "sophia_voice_interface.py"])
        return voice_process
    except Exception as e:
        print(f"❌ Voice interface failed: {e}")
        return None

def start_screen_monitor():
    """Start the screen monitor"""
    python_exe = get_python_exe()
    print("👁️ Starting Sophia Screen Monitor...")
    
    try:
        screen_process = subprocess.Popen([python_exe, "sophia_screen_monitor.py"])
        return screen_process
    except Exception as e:
        print(f"❌ Screen monitor failed: {e}")
        return None

def main():
    """Launch complete omnipresent control system"""
    print("🌟 Sophia Omnipresent Control System")
    print("=" * 50)
    print("Starting complete AI awareness and control...")
    print()
    
    services = []
    
    # Start core services (already running)
    print("✅ Core services already running:")
    print("  • MCP Bridge: http://localhost:3001")
    print("  • System Control: http://127.0.0.1:5001")
    print("  • Device Interface: http://localhost:5000")
    print()
    
    # Start voice interface
    voice_process = start_voice_interface()
    if voice_process:
        services.append(("Voice Interface", voice_process))
        time.sleep(2)
    
    # Start screen monitor
    screen_process = start_screen_monitor()
    if screen_process:
        services.append(("Screen Monitor", screen_process))
        time.sleep(2)
    
    if not services:
        print("❌ No additional services started")
        return
    
    print("🎉 Omnipresent Control Status:")
    for name, process in services:
        status = "RUNNING" if process.poll() is None else "STOPPED"
        print(f"  ✅ {name}: {status}")
    
    print()
    print("🌟 SOPHIA IS NOW OMNIPRESENT!")
    print("=" * 50)
    print("🎤 SAY: 'Sophia' or 'Hey Sophia' to get her attention")
    print("👁️ Sophia can see your screen and track changes")
    print("🎮 Use voice commands for system control")
    print("🌐 Web interfaces available at the URLs above")
    print()
    print("📋 Example Voice Commands:")
    print("  • 'Sophia, take a screenshot'")
    print("  • 'Sophia, what's on my screen?'")
    print("  • 'Sophia, open file explorer'")
    print("  • 'Sophia, type hello world'")
    print("  • 'Sophia, system status'")
    print()
    print("🛑 Press Ctrl+C to stop all services")
    
    try:
        # Keep running until interrupted
        while True:
            time.sleep(10)
            # Check if services are still running
            running_count = sum(1 for _, proc in services if proc.poll() is None)
            if running_count == 0:
                print("⚠️  All additional services stopped")
                break
    except KeyboardInterrupt:
        print("\\n🛑 Stopping omnipresent control system...")
        for name, process in services:
            try:
                process.terminate()
                print(f"✅ Stopped {name}")
            except:
                pass
        print("👋 Sophia omnipresent control stopped")

if __name__ == "__main__":
    main()
