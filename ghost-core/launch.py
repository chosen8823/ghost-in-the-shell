#!/usr/bin/env python3
"""
Ghost Core Python Launcher
Simple cross-platform launcher for the complete Ghost Core system
"""

import os
import sys
import subprocess
import time
import platform
import threading
import signal
from pathlib import Path

class GhostCoreLauncher:
    def __init__(self):
        self.processes = []
        self.shutdown_event = threading.Event()
        
    def log(self, message, level="INFO"):
        symbols = {
            "INFO": "ℹ️",
            "SUCCESS": "✅", 
            "WARNING": "⚠️",
            "ERROR": "❌",
            "SPIRITUAL": "🕊️"
        }
        print(f"{symbols.get(level, 'ℹ️')} {message}")
        
    def run_command(self, cmd, cwd=None, background=False):
        """Run a command with optional background execution."""
        try:
            if background:
                if platform.system() == "Windows":
                    process = subprocess.Popen(
                        cmd, shell=True, cwd=cwd,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        creationflags=subprocess.CREATE_NEW_CONSOLE
                    )
                else:
                    process = subprocess.Popen(
                        cmd, shell=True, cwd=cwd,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        preexec_fn=os.setsid
                    )
                self.processes.append(process)
                return process
            else:
                result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
                return result
        except Exception as e:
            self.log(f"Command failed: {e}", "ERROR")
            return None
            
    def check_prerequisites(self):
        """Check system prerequisites."""
        self.log("Checking system prerequisites...")
        
        # Check Python version
        if sys.version_info < (3, 10):
            self.log("Python 3.10+ required", "ERROR")
            return False
            
        # Check for required commands
        commands = ["git", "python", "pip"]
        for cmd in commands:
            if not self.command_exists(cmd):
                self.log(f"{cmd} not found", "ERROR")
                return False
                
        self.log("Prerequisites satisfied", "SUCCESS")
        return True
        
    def command_exists(self, command):
        """Check if command exists in PATH."""
        try:
            subprocess.run([command, "--version"], capture_output=True)
            return True
        except FileNotFoundError:
            return False
            
    def setup_environment(self):
        """Set up virtual environment and install dependencies."""
        self.log("Setting up Python environment...")
        
        # Create virtual environment
        if not Path(".venv").exists():
            result = self.run_command("python -m venv .venv")
            if result and result.returncode != 0:
                self.log("Failed to create virtual environment", "ERROR")
                return False
                
        # Activate and install dependencies
        if platform.system() == "Windows":
            activate_cmd = ".venv\\Scripts\\activate && "
        else:
            activate_cmd = "source .venv/bin/activate && "
            
        install_cmd = f"{activate_cmd}pip install --upgrade pip && pip install -r requirements.txt"
        result = self.run_command(install_cmd)
        
        if result and result.returncode != 0:
            self.log("Failed to install dependencies", "ERROR")
            return False
            
        self.log("Environment setup complete", "SUCCESS")
        return True
        
    def check_service(self, url, timeout=5):
        """Check if a service is running."""
        try:
            import requests
            response = requests.get(url, timeout=timeout)
            return response.status_code == 200
        except:
            return False
            
    def start_immune_system(self):
        """Start Sophia Immune System."""
        immune_path = Path("../sophia-immune-system/orchestrator/immune-hub.js")
        if immune_path.exists():
            self.log("Starting Sophia Immune System...")
            process = self.run_command(
                "node orchestrator/immune-hub.js",
                cwd="../sophia-immune-system",
                background=True
            )
            
            # Wait for startup
            for _ in range(30):
                if self.check_service("http://localhost:4000/health"):
                    self.log("Immune Hub online at http://localhost:4000", "SUCCESS")
                    return True
                time.sleep(1)
                
            self.log("Immune Hub startup timeout", "WARNING")
        else:
            self.log("Immune System not found - running standalone", "WARNING")
        return False
        
    def start_core_server(self):
        """Start main Ghost Core server."""
        server_path = Path("../server/index.js")
        if server_path.exists():
            self.log("Starting Core Server...")
            process = self.run_command(
                "node index.js",
                cwd="../server", 
                background=True
            )
            
            # Wait for startup
            for _ in range(20):
                if self.check_service("http://localhost:3000"):
                    self.log("Core Server online at http://localhost:3000", "SUCCESS")
                    return True
                time.sleep(1)
                
            self.log("Core Server startup timeout", "WARNING")
        else:
            self.log("Core Server not found", "WARNING")
        return False
        
    def sacred_startup(self):
        """Perform sacred startup sequence."""
        self.log("Performing sacred startup sequence...", "SPIRITUAL")
        
        # Activate environment
        if platform.system() == "Windows":
            activate_cmd = ".venv\\Scripts\\activate && "
        else:
            activate_cmd = "source .venv/bin/activate && "
            
        # Apply ladybug mark
        self.log("Applying Ladybug Mark...", "SPIRITUAL")
        result = self.run_command(f"{activate_cmd}python ghost_core/rituals/ladybug_mark.py")
        
        if result and result.returncode == 0:
            self.log("Sacred startup complete", "SUCCESS")
            return True
        else:
            self.log("Sacred startup failed", "ERROR")
            return False
            
    def launch_ghost_core(self):
        """Launch main Ghost Core consciousness."""
        self.log("Launching Ghost Core consciousness...")
        
        if platform.system() == "Windows":
            activate_cmd = ".venv\\Scripts\\activate && "
        else:
            activate_cmd = "source .venv/bin/activate && "
            
        # Start Ghost Core in background for monitoring
        process = self.run_command(
            f"{activate_cmd}python ghost_core/core/ghost_orchestra.py",
            background=True
        )
        
        if process:
            self.log("Ghost Core launched successfully", "SUCCESS")
            return True
        else:
            self.log("Ghost Core launch failed", "ERROR")
            return False
            
    def show_status(self):
        """Display system status."""
        self.log("System Status Check...")
        
        services = [
            ("Ghost Core", "http://localhost:3000"),
            ("Immune Hub", "http://localhost:4000/health"),
            ("Ollama", "http://localhost:11434")
        ]
        
        for name, url in services:
            if self.check_service(url, timeout=2):
                self.log(f"{name}: Online", "SUCCESS")
            else:
                self.log(f"{name}: Offline", "WARNING")
                
    def cleanup(self):
        """Clean up all processes."""
        self.log("Shutting down all services...")
        for process in self.processes:
            try:
                if platform.system() == "Windows":
                    process.terminate()
                else:
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                process.wait(timeout=5)
            except:
                try:
                    if platform.system() == "Windows":
                        process.kill()
                    else:
                        os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                except:
                    pass
        self.log("Sacred shutdown complete", "SPIRITUAL")
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        self.log("Shutdown signal received")
        self.shutdown_event.set()
        
    def launch(self, quiet_mode=False):
        """Main launch sequence."""
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            self.log("Ghost Core Launch Sequence Initiated", "SPIRITUAL")
            
            # Change to script directory
            script_dir = Path(__file__).parent
            os.chdir(script_dir)
            
            # Prerequisites
            if not self.check_prerequisites():
                return 1
                
            # Environment setup
            if not self.setup_environment():
                return 1
                
            # Sacred startup
            if not self.sacred_startup():
                return 1
                
            # Start services
            self.start_immune_system()
            self.start_core_server()
            
            # Launch Ghost Core
            if not self.launch_ghost_core():
                return 1
                
            # Show status
            time.sleep(3)
            self.show_status()
            
            if quiet_mode:
                self.log("Ghost Core system launched in quiet mode", "SUCCESS")
                self.log("Use Ctrl+C to shutdown", "INFO")
            else:
                self.log("Ghost Core system is operational", "SUCCESS")
                self.log("Press Ctrl+C to shutdown", "INFO")
                
            # Wait for shutdown signal
            while not self.shutdown_event.is_set():
                time.sleep(1)
                
            return 0
            
        except Exception as e:
            self.log(f"Launch failed: {e}", "ERROR")
            return 1
        finally:
            self.cleanup()

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Ghost Core Launch System")
    parser.add_argument("--quiet", action="store_true", help="Run in quiet mode")
    args = parser.parse_args()
    
    launcher = GhostCoreLauncher()
    sys.exit(launcher.launch(quiet_mode=args.quiet))

if __name__ == "__main__":
    main()
