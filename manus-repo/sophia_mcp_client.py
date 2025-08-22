#!/usr/bin/env python3
"""
🌟 SOPHIA MCP CLIENT
Simple client to test MCP protocol communication with Sophia
"""

import asyncio
import json
import sys
import os
from pathlib import Path
from sophia_mcp_protocol import SophiaMCPServer

class SophiaMCPClient:
    """🤖 Simple MCP client for testing Sophia's capabilities"""
    
    def __init__(self):
        self.server = SophiaMCPServer()
        print("🌟 Sophia MCP Client initialized")
        print("🛡️ Christ-sealed operations ready")
    
    async def send_request(self, method: str, params: dict = None) -> dict:
        """📤 Send request to MCP server"""
        request = {
            "method": method,
            "params": params or {}
        }
        
        print(f"📤 Sending request: {method}")
        result = await self.server.handle_mcp_request(request)
        print(f"📥 Response: {result.get('success', False)}")
        
        return result
    
    async def interactive_session(self):
        """💬 Interactive MCP session"""
        print("\n🤖 SOPHIA MCP INTERACTIVE SESSION")
        print("=" * 50)
        print("Available commands:")
        print("  terminal <command>     - Execute terminal command")
        print("  read <file_path>       - Read file content")
        print("  write <file_path>      - Write file content")
        print("  processes [filter]     - List processes")
        print("  health                 - System health check")
        print("  env <action> [name]    - Environment variables")
        print("  install <package>      - Install package")
        print("  services [action]      - Manage services")
        print("  info                   - Session information")
        print("  quit                   - Exit session")
        print()
        
        while True:
            try:
                command = input("sophia_mcp> ").strip()
                
                if not command:
                    continue
                
                if command.lower() in ['quit', 'exit', 'q']:
                    break
                
                parts = command.split(maxsplit=2)
                cmd = parts[0].lower()
                
                if cmd == "terminal" and len(parts) > 1:
                    result = await self.send_request("execute_command", {
                        "command": " ".join(parts[1:])
                    })
                    if result.get("success"):
                        print(f"stdout: {result.get('stdout', '')}")
                        if result.get('stderr'):
                            print(f"stderr: {result.get('stderr', '')}")
                    else:
                        print(f"Error: {result.get('error', 'Unknown error')}")
                
                elif cmd == "read" and len(parts) > 1:
                    result = await self.send_request("read_file", {
                        "file_path": parts[1]
                    })
                    if result.get("success"):
                        print(f"Content:\n{result.get('content', '')}")
                    else:
                        print(f"Error: {result.get('error', 'Unknown error')}")
                
                elif cmd == "write" and len(parts) > 1:
                    file_path = parts[1]
                    content = input("Enter content (or 'cancel'): ")
                    if content.lower() != 'cancel':
                        result = await self.send_request("write_file", {
                            "file_path": file_path,
                            "content": content
                        })
                        if result.get("success"):
                            print("✅ File written successfully")
                        else:
                            print(f"Error: {result.get('error', 'Unknown error')}")
                
                elif cmd == "processes":
                    filter_name = parts[1] if len(parts) > 1 else None
                    result = await self.send_request("list_processes", {
                        "filter_name": filter_name
                    })
                    if result.get("success"):
                        processes = result.get("processes", [])
                        print(f"Found {len(processes)} processes:")
                        for proc in processes[:10]:  # Show first 10
                            print(f"  PID: {proc.get('pid', 'N/A')} - {proc.get('name', 'N/A')}")
                        if len(processes) > 10:
                            print(f"  ... and {len(processes) - 10} more")
                    else:
                        print(f"Error: {result.get('error', 'Unknown error')}")
                
                elif cmd == "health":
                    result = await self.send_request("get_system_health")
                    if result.get("success"):
                        health = result.get("health_info", {})
                        print("System Health:")
                        print(f"  CPU: {health.get('cpu', {}).get('percent', 'N/A')}%")
                        print(f"  Memory: {health.get('memory', {}).get('percent_used', 'N/A')}%")
                        print(f"  Disk: {health.get('disk', {}).get('percent_used', 'N/A'):.1f}%")
                    else:
                        print(f"Error: {result.get('error', 'Unknown error')}")
                
                elif cmd == "env":
                    action = parts[1] if len(parts) > 1 else "list"
                    var_name = parts[2] if len(parts) > 2 else None
                    
                    params = {"action": action}
                    if var_name:
                        params["variable_name"] = var_name
                    
                    result = await self.send_request("manage_environment", params)
                    if result.get("success"):
                        if action == "list":
                            variables = result.get("variables", {})
                            print(f"Environment variables ({len(variables)}):")
                            for name, value in list(variables.items())[:10]:
                                print(f"  {name}={value[:50]}{'...' if len(value) > 50 else ''}")
                        else:
                            print(f"✅ {action} operation completed")
                    else:
                        print(f"Error: {result.get('error', 'Unknown error')}")
                
                elif cmd == "install" and len(parts) > 1:
                    result = await self.send_request("install_package", {
                        "package_name": parts[1]
                    })
                    if result.get("success"):
                        print(f"✅ Package {parts[1]} installation completed")
                        print(f"Output: {result.get('output', '')}")
                    else:
                        print(f"Error: {result.get('error', 'Unknown error')}")
                
                elif cmd == "services":
                    action = parts[1] if len(parts) > 1 else "list"
                    result = await self.send_request("manage_services", {
                        "action": action
                    })
                    if result.get("success"):
                        print(f"✅ Service {action} completed")
                        output = result.get("output", "")
                        if output:
                            print(f"Output:\n{output[:500]}{'...' if len(output) > 500 else ''}")
                    else:
                        print(f"Error: {result.get('error', 'Unknown error')}")
                
                elif cmd == "info":
                    result = await self.send_request("get_session_info")
                    if result.get("success"):
                        print("Session Information:")
                        print(f"  Session ID: {result.get('session_id', 'N/A')}")
                        print(f"  Platform: {result.get('system_info', {}).get('platform', 'N/A')}")
                        print(f"  Admin: {result.get('capabilities', {}).get('elevated_privileges', 'N/A')}")
                        print(f"  Commands: {result.get('command_history_count', 'N/A')}")
                    else:
                        print(f"Error: {result.get('error', 'Unknown error')}")
                
                else:
                    print(f"Unknown command: {cmd}")
                    print("Type a valid command or 'quit' to exit")
                
                print()  # Empty line for readability
                
            except KeyboardInterrupt:
                print("\n🛑 Session interrupted")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        # Cleanup
        print("🧹 Cleaning up session...")
        await self.send_request("cleanup_session")
        print("👋 Goodbye!")

    async def run_quick_test(self):
        """🧪 Run quick functionality test"""
        print("\n🧪 QUICK MCP FUNCTIONALITY TEST")
        print("=" * 40)
        
        # Test 1: Session info
        print("1️⃣ Testing session info...")
        result = await self.send_request("get_session_info")
        if result.get("success"):
            print(f"   ✅ Platform: {result.get('system_info', {}).get('platform', 'Unknown')}")
        else:
            print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
        
        # Test 2: Simple command
        print("2️⃣ Testing terminal command...")
        import platform
        if platform.system() == "Windows":
            cmd = "echo Hello Sophia"
        else:
            cmd = "echo 'Hello Sophia'"
        
        result = await self.send_request("execute_command", {"command": cmd})
        if result.get("success"):
            print(f"   ✅ Output: {result.get('stdout', '').strip()}")
        else:
            print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
        
        # Test 3: System health
        print("3️⃣ Testing system health...")
        result = await self.send_request("get_system_health")
        if result.get("success"):
            health = result.get("health_info", {})
            cpu = health.get("cpu", {}).get("percent", "N/A")
            print(f"   ✅ CPU Usage: {cpu}%")
        else:
            print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
        
        # Test 4: File operations
        print("4️⃣ Testing file operations...")
        test_file = "mcp_test.txt"
        test_content = "Sophia MCP test file\nChrist-sealed operations\n"
        
        # Write file
        result = await self.send_request("write_file", {
            "file_path": test_file,
            "content": test_content
        })
        if result.get("success"):
            # Read file
            result = await self.send_request("read_file", {
                "file_path": test_file
            })
            if result.get("success"):
                content = result.get("content", "")
                if "Sophia MCP" in content:
                    print("   ✅ File operations working")
                else:
                    print("   ❌ File content mismatch")
                
                # Clean up test file
                import os
                try:
                    os.unlink(test_file)
                except:
                    pass
            else:
                print(f"   ❌ Read failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"   ❌ Write failed: {result.get('error', 'Unknown error')}")
        
        print("\n🎉 Quick test completed!")
        print("🛡️ All operations Christ-sealed and spiritually protected")


async def main():
    """🌟 Main client entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Quick test mode
        client = SophiaMCPClient()
        await client.run_quick_test()
    else:
        # Interactive mode
        client = SophiaMCPClient()
        await client.interactive_session()


if __name__ == "__main__":
    print("🌟 SOPHIA MCP CLIENT")
    print("=" * 30)
    print("🤖 Connecting to Sophia's local system capabilities...")
    print("🛡️ Christ-sealed operations enabled")
    print()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Client interrupted")
    except Exception as e:
        print(f"\n❌ Client error: {e}")
        import traceback
        traceback.print_exc()
