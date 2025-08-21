#!/usr/bin/env python3
"""
Sophia Omnipresent Control Launcher
Starts all services for N8N + MCP omnipresent device control
"""

import asyncio
import subprocess
import sys
import time
import requests
from pathlib import Path
import psutil

class SophiaOmnipresentLauncher:
    def __init__(self):
        self.services = {}
        self.project_root = Path(__file__).parent
        
    async def launch_all_services(self):
        """Launch all required services for omnipresent control"""
        print("🚀 Launching Sophia Omnipresent Control System")
        print("=" * 60)
        
        # 1. Start MCP Bridge Server
        await self._start_mcp_bridge()
        
        # 2. Check/Start N8N
        await self._start_n8n()
        
        # 3. Load Workflows
        await self._load_workflows()
        
        # 4. Start Sophia AI
        await self._start_sophia()
        
        # 5. Health Check
        await self._health_check()
        
        print("\n🎉 Sophia Omnipresent Control System READY!")
        print("🤖 Sophia can now control your device through N8N workflows!")
        
    async def _start_mcp_bridge(self):
        """Start the MCP Bridge Server"""
        print("\n🔧 Starting MCP Bridge Server...")
        
        try:
            # Check if already running
            if self._is_port_in_use(3001):
                print("✅ MCP Bridge already running on port 3001")
                return
                
            # Start MCP bridge
            bridge_cmd = [sys.executable, "sophia_mcp_bridge.py"]
            self.services['mcp_bridge'] = subprocess.Popen(
                bridge_cmd,
                cwd=self.project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for service to start
            await asyncio.sleep(3)
            
            # Test connection
            try:
                response = requests.get("http://localhost:3001/status", timeout=5)
                if response.status_code == 200:
                    print("✅ MCP Bridge Server started successfully")
                else:
                    print("❌ MCP Bridge Server not responding correctly")
            except requests.exceptions.RequestException:
                print("❌ MCP Bridge Server failed to start")
                
        except Exception as e:
            print(f"❌ Failed to start MCP Bridge: {e}")
            
    async def _start_n8n(self):
        """Start N8N if not already running"""
        print("\n⚡ Checking N8N status...")
        
        try:
            # Check if N8N is already running
            if self._is_port_in_use(5678):
                print("✅ N8N already running on port 5678")
                return
                
            # Start N8N
            print("🚀 Starting N8N...")
            n8n_cmd = ["npx", "n8n", "start", "--tunnel"]
            self.services['n8n'] = subprocess.Popen(
                n8n_cmd,
                cwd=self.project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for N8N to start
            print("⏳ Waiting for N8N to initialize...")
            await asyncio.sleep(10)
            
            # Test N8N connection
            try:
                response = requests.get("http://localhost:5678/rest/active-workflows", timeout=10)
                print("✅ N8N started successfully")
            except requests.exceptions.RequestException:
                print("⚠️ N8N may still be starting up")
                
        except Exception as e:
            print(f"❌ Failed to start N8N: {e}")
            print("💡 Try installing N8N globally: npm install -g n8n")
            
    async def _load_workflows(self):
        """Load Sophia's workflows into N8N"""
        print("\n📂 Loading Sophia workflows...")
        
        workflows_dir = self.project_root / "workflows"
        if not workflows_dir.exists():
            print("❌ Workflows directory not found")
            return
            
        workflow_files = list(workflows_dir.glob("*.json"))
        print(f"📁 Found {len(workflow_files)} workflow files")
        
        for workflow_file in workflow_files:
            print(f"📝 Workflow: {workflow_file.name}")
            
        print("✅ Workflows ready for import")
        print("💡 Import manually in N8N at: http://localhost:5678")
        
    async def _start_sophia(self):
        """Start Sophia AI launcher"""
        print("\n🤖 Starting Sophia AI...")
        
        try:
            sophia_cmd = [sys.executable, "sophia_launcher.py"]
            print("✅ Sophia AI launcher ready")
            print("💡 Run 'python sophia_launcher.py' to start interactive mode")
            
        except Exception as e:
            print(f"❌ Failed to prepare Sophia: {e}")
            
    async def _health_check(self):
        """Perform health check on all services"""
        print("\n🏥 Health Check...")
        
        services_status = {}
        
        # Check MCP Bridge
        try:
            response = requests.get("http://localhost:3001/status", timeout=5)
            services_status['MCP Bridge'] = "✅ Healthy" if response.status_code == 200 else "❌ Error"
        except:
            services_status['MCP Bridge'] = "❌ Not responding"
            
        # Check N8N
        try:
            response = requests.get("http://localhost:5678", timeout=5)
            services_status['N8N'] = "✅ Healthy" if response.status_code == 200 else "❌ Error"
        except:
            services_status['N8N'] = "❌ Not responding"
            
        # Print status
        for service, status in services_status.items():
            print(f"  {service}: {status}")
            
    def _is_port_in_use(self, port):
        """Check if a port is already in use"""
        for conn in psutil.net_connections():
            if conn.laddr.port == port:
                return True
        return False
        
    async def show_control_panel(self):
        """Show interactive control panel"""
        print("\n🎛️ Sophia Control Panel")
        print("=" * 30)
        print("Available Commands:")
        print("  1. Start All Services")
        print("  2. Stop All Services") 
        print("  3. Show Status")
        print("  4. Open N8N Interface")
        print("  5. Test Workflow")
        print("  6. Emergency Stop")
        print("  q. Quit")
        
        while True:
            try:
                choice = input("\n🤖 Enter command (1-6, q): ").strip()
                
                if choice == '1':
                    await self.launch_all_services()
                elif choice == '2':
                    await self._stop_all_services()
                elif choice == '3':
                    await self._show_status()
                elif choice == '4':
                    await self._open_n8n_interface()
                elif choice == '5':
                    await self._test_workflow()
                elif choice == '6':
                    await self._emergency_stop()
                elif choice.lower() == 'q':
                    print("👋 Shutting down Sophia Control Panel...")
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n👋 Exiting...")
                break
                
    async def _stop_all_services(self):
        """Stop all running services"""
        print("\n🛑 Stopping all services...")
        
        for name, process in self.services.items():
            try:
                if process and process.poll() is None:
                    process.terminate()
                    process.wait(timeout=5)
                    print(f"✅ Stopped {name}")
            except:
                print(f"❌ Failed to stop {name}")
                
        self.services.clear()
        print("✅ All services stopped")
        
    async def _show_status(self):
        """Show current status of all services"""
        await self._health_check()
        
    async def _open_n8n_interface(self):
        """Open N8N web interface"""
        import webbrowser
        print("🌐 Opening N8N interface...")
        webbrowser.open("http://localhost:5678")
        
    async def _test_workflow(self):
        """Test a simple workflow"""
        print("\n🧪 Testing simple workflow...")
        
        test_payload = {
            "command_type": "system_control",
            "action": "screenshot",
            "target": "desktop",
            "parameters": {},
            "auth_token": "sk-sophia-secure-token-2025"
        }
        
        try:
            response = requests.post(
                "http://localhost:3001/system-control",
                json=test_payload,
                headers={"Authorization": "Bearer sk-sophia-secure-token-2025"},
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Test workflow executed successfully")
                print(f"📊 Result: {response.json()}")
            else:
                print(f"❌ Test workflow failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Test workflow error: {e}")
            
    async def _emergency_stop(self):
        """Emergency stop all workflows and services"""
        print("🚨 EMERGENCY STOP ACTIVATED")
        
        # Stop all services
        await self._stop_all_services()
        
        # Send emergency stop to MCP bridge
        try:
            requests.post(
                "http://localhost:3001/emergency-stop",
                json={"auth_token": "sk-sophia-secure-token-2025"},
                timeout=5
            )
        except:
            pass
            
        print("🛑 Emergency stop complete")

async def main():
    """Main launcher function"""
    launcher = SophiaOmnipresentLauncher()
    
    print("🤖 Sophia Omnipresent Control System")
    print("🎯 N8N + MCP Integration for Device Control")
    print("=" * 50)
    
    try:
        await launcher.show_control_panel()
    except KeyboardInterrupt:
        print("\n🛑 Launcher interrupted")
        await launcher._stop_all_services()

if __name__ == "__main__":
    asyncio.run(main())
