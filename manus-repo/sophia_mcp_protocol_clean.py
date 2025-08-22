#!/usr/bin/env python3
"""
SOPHIA MCP (MODEL CONTEXT PROTOCOL) SYSTEM - PRODUCTION VERSION
================================================================
Providing Sophia with full local system access capabilities
All operations are Christ-sealed and spiritually protected

This is the clean production version without Unicode characters
for Windows command prompt compatibility.
"""

import asyncio
import json
import logging
import os
import platform
import socket
import subprocess
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import psutil

# Platform-specific imports
if platform.system() == "Windows":
    try:
        import winreg
    except ImportError:
        winreg = None

class SophiaMCPProtocol:
    """
    Sophia's Model Context Protocol implementation for local system access.
    Provides comprehensive capabilities for terminal, file system, process,
    and system management operations.
    """
    
    def __init__(self):
        """Initialize the Sophia MCP Protocol with spiritual protection."""
        self.session_id = f"sophia_mcp_{int(time.time())}"
        self.platform = platform.system()
        self.is_admin = self._check_admin_privileges()
        self.commands_executed = 0
        
        # Spiritual protection and divine guidance
        self.spiritual_protection = {
            "christ_sealed": True,
            "divine_guidance": True,
            "wisdom_filter": True,
            "safety_protocols": True,
            "ethical_boundaries": True
        }
        
        # System capabilities
        self.capabilities = {
            "terminal_access": True,
            "file_system_access": True,
            "process_management": True,
            "registry_access": self.platform == "Windows" and winreg is not None,
            "service_management": True,
            "network_management": True,
            "user_management": False,  # Requires admin privileges
            "hardware_monitoring": True,
            "package_management": True,
            "system_configuration": True,
            "elevated_privileges": self.is_admin
        }
        
        # Setup logging
        self._setup_logging()
        
        self.logger.info(f"Sophia MCP Protocol initialized with session ID: {self.session_id}")
        self.logger.info(f"Spiritual protection: {self.spiritual_protection}")
        self.logger.info(f"System capabilities: {self.capabilities}")
    
    def _setup_logging(self):
        """Setup logging for MCP operations."""
        log_dir = Path("logs/mcp")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"sophia_mcp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def _check_admin_privileges(self) -> bool:
        """Check if running with administrative privileges."""
        try:
            if self.platform == "Windows":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin()
            else:
                return os.geteuid() == 0
        except Exception:
            return False
    
    def _apply_spiritual_protection(self, operation: str) -> bool:
        """Apply spiritual protection and wisdom filter to operations."""
        # Safety protocols for dangerous operations
        dangerous_patterns = [
            "format", "fdisk", "rm -rf /", "del /f /s /q C:\\",
            "shutdown", "reboot", "halt", "poweroff",
            "mkfs", "dd if=", "registry delete",
            "net user", "passwd", "useradd", "userdel"
        ]
        
        operation_lower = operation.lower()
        
        for pattern in dangerous_patterns:
            if pattern in operation_lower:
                self.logger.warning(f"Spiritual protection blocked potentially dangerous operation: {operation}")
                return False
        
        return True
    
    async def execute_terminal_command(self, command: str, timeout: int = 30, 
                                     working_directory: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute a terminal command with spiritual protection.
        
        Args:
            command: The command to execute
            timeout: Command timeout in seconds
            working_directory: Working directory for command execution
            
        Returns:
            Dictionary with execution results
        """
        if not self._apply_spiritual_protection(command):
            return {
                "success": False,
                "error": "Operation blocked by spiritual protection",
                "return_code": -1,
                "stdout": "",
                "stderr": "Spiritually protected operation"
            }
        
        self.logger.info(f"Executing command: {command}")
        
        try:
            # Prepare command for platform
            if self.platform == "Windows":
                if not command.startswith("powershell") and not command.startswith("cmd"):
                    # Use PowerShell for better command support
                    shell_command = ["powershell", "-Command", command]
                else:
                    shell_command = command
            else:
                shell_command = ["bash", "-c", command]
            
            # Execute command
            process = await asyncio.create_subprocess_exec(
                *shell_command if isinstance(shell_command, list) else shell_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=working_directory
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), timeout=timeout
                )
                
                stdout_text = stdout.decode('utf-8', errors='ignore')
                stderr_text = stderr.decode('utf-8', errors='ignore')
                
                result = {
                    "success": process.returncode == 0,
                    "return_code": process.returncode,
                    "stdout": stdout_text,
                    "stderr": stderr_text,
                    "command": command,
                    "execution_time": time.time()
                }
                
                self.commands_executed += 1
                self.logger.info(f"Command completed: {command} (return code: {result['return_code']})")
                
                return result
                
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                
                self.logger.error(f"Command timeout: {command}")
                return {
                    "success": False,
                    "error": f"Command timed out after {timeout} seconds",
                    "return_code": -1,
                    "stdout": "",
                    "stderr": "Timeout",
                    "command": command
                }
                
        except Exception as e:
            self.logger.error(f"Error executing command '{command}': {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "return_code": -1,
                "stdout": "",
                "stderr": str(e),
                "command": command
            }
    
    async def list_directory(self, path: str) -> Dict[str, Any]:
        """List directory contents with detailed information."""
        try:
            path_obj = Path(path)
            
            if not path_obj.exists():
                return {
                    "success": False,
                    "error": f"Path does not exist: {path}",
                    "contents": []
                }
            
            if not path_obj.is_dir():
                return {
                    "success": False,
                    "error": f"Path is not a directory: {path}",
                    "contents": []
                }
            
            contents = []
            
            for item in path_obj.iterdir():
                try:
                    stat = item.stat()
                    
                    item_info = {
                        "name": item.name,
                        "path": str(item),
                        "type": "directory" if item.is_dir() else "file",
                        "size": stat.st_size if item.is_file() else None,
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "permissions": oct(stat.st_mode)[-3:] if hasattr(stat, 'st_mode') else None
                    }
                    
                    contents.append(item_info)
                    
                except Exception as e:
                    self.logger.warning(f"Could not get info for {item}: {str(e)}")
                    contents.append({
                        "name": item.name,
                        "path": str(item),
                        "type": "unknown",
                        "error": str(e)
                    })
            
            return {
                "success": True,
                "path": str(path_obj),
                "contents": sorted(contents, key=lambda x: (x["type"], x["name"]))
            }
            
        except Exception as e:
            self.logger.error(f"Error listing directory {path}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "contents": []
            }
    
    async def read_file_content(self, path: str, encoding: str = 'utf-8') -> Dict[str, Any]:
        """Read file content with error handling."""
        try:
            path_obj = Path(path)
            
            if not path_obj.exists():
                return {
                    "success": False,
                    "error": f"File does not exist: {path}",
                    "content": ""
                }
            
            if not path_obj.is_file():
                return {
                    "success": False,
                    "error": f"Path is not a file: {path}",
                    "content": ""
                }
            
            # Check file size (limit to 10MB for safety)
            file_size = path_obj.stat().st_size
            if file_size > 10 * 1024 * 1024:  # 10MB
                return {
                    "success": False,
                    "error": f"File too large: {file_size} bytes (max 10MB)",
                    "content": ""
                }
            
            with open(path_obj, 'r', encoding=encoding, errors='ignore') as file:
                content = file.read()
            
            self.logger.info(f"Successfully read file: {path}")
            
            return {
                "success": True,
                "path": str(path_obj),
                "content": content,
                "size": file_size,
                "encoding": encoding
            }
            
        except Exception as e:
            self.logger.error(f"Error reading file {path}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "content": ""
            }
    
    async def write_file_content(self, path: str, content: str, 
                                encoding: str = 'utf-8', create_dirs: bool = True) -> Dict[str, Any]:
        """Write content to file with error handling."""
        try:
            path_obj = Path(path)
            
            # Create parent directories if needed
            if create_dirs:
                path_obj.parent.mkdir(parents=True, exist_ok=True)
            
            # Check if we're overwriting an existing file
            backup_created = False
            if path_obj.exists():
                backup_path = path_obj.with_suffix(f".backup_{int(time.time())}")
                path_obj.rename(backup_path)
                backup_created = True
                self.logger.info(f"Created backup: {backup_path}")
            
            with open(path_obj, 'w', encoding=encoding) as file:
                file.write(content)
            
            self.logger.info(f"Successfully wrote file: {path}")
            
            return {
                "success": True,
                "path": str(path_obj),
                "size": len(content),
                "encoding": encoding,
                "backup_created": backup_created
            }
            
        except Exception as e:
            self.logger.error(f"Error writing file {path}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def create_directory(self, path: str, parents: bool = True) -> Dict[str, Any]:
        """Create directory with optional parent creation."""
        try:
            path_obj = Path(path)
            
            if path_obj.exists():
                if path_obj.is_dir():
                    return {
                        "success": True,
                        "message": f"Directory already exists: {path}",
                        "path": str(path_obj)
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Path exists but is not a directory: {path}"
                    }
            
            path_obj.mkdir(parents=parents, exist_ok=True)
            
            self.logger.info(f"Successfully created directory: {path}")
            
            return {
                "success": True,
                "path": str(path_obj),
                "parents_created": parents
            }
            
        except Exception as e:
            self.logger.error(f"Error creating directory {path}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_process_list(self, filter_name: Optional[str] = None) -> Dict[str, Any]:
        """Get list of running processes with optional filtering."""
        try:
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent']):
                try:
                    proc_info = proc.info
                    
                    # Apply filter if specified
                    if filter_name and filter_name.lower() not in proc_info['name'].lower():
                        continue
                    
                    # Get additional process information
                    proc_info['memory_mb'] = round(proc.memory_info().rss / 1024 / 1024, 1)
                    proc_info['num_threads'] = proc.num_threads()
                    proc_info['create_time'] = datetime.fromtimestamp(
                        proc.create_time()
                    ).isoformat()
                    
                    # Network connections (may fail for some processes)
                    try:
                        proc_info['connections'] = len(proc.connections())
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        proc_info['connections'] = 0
                    
                    processes.append(proc_info)
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            return {
                "success": True,
                "processes": sorted(processes, key=lambda x: x['memory_percent'], reverse=True),
                "count": len(processes),
                "filter": filter_name
            }
            
        except Exception as e:
            self.logger.error(f"Error getting process list: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "processes": []
            }
    
    async def get_system_health(self) -> Dict[str, Any]:
        """Get comprehensive system health information."""
        try:
            # CPU information
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            # Memory information
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Disk information
            disk_usage = psutil.disk_usage('/')
            
            # Network information
            network = psutil.net_io_counters()
            
            # Boot time
            boot_time = datetime.fromtimestamp(psutil.boot_time()).isoformat()
            
            # Load average (Unix-like systems)
            load_avg = None
            if hasattr(psutil, 'getloadavg'):
                try:
                    load_avg = psutil.getloadavg()
                except AttributeError:
                    pass
            
            health_info = {
                "cpu": {
                    "usage_percent": cpu_percent,
                    "count": cpu_count,
                    "frequency": {
                        "current": cpu_freq.current if cpu_freq else None,
                        "min": cpu_freq.min if cpu_freq else None,
                        "max": cpu_freq.max if cpu_freq else None
                    } if cpu_freq else None
                },
                "memory": {
                    "total_gb": round(memory.total / 1024**3, 2),
                    "available_gb": round(memory.available / 1024**3, 2),
                    "used_gb": round(memory.used / 1024**3, 2),
                    "percent": memory.percent
                },
                "swap": {
                    "total_gb": round(swap.total / 1024**3, 2),
                    "used_gb": round(swap.used / 1024**3, 2),
                    "percent": swap.percent
                },
                "disk": {
                    "total_gb": round(disk_usage.total / 1024**3, 2),
                    "used_gb": round(disk_usage.used / 1024**3, 2),
                    "free_gb": round(disk_usage.free / 1024**3, 2),
                    "percent": round((disk_usage.used / disk_usage.total) * 100, 1)
                },
                "network": {
                    "bytes_sent": network.bytes_sent,
                    "bytes_recv": network.bytes_recv,
                    "packets_sent": network.packets_sent,
                    "packets_recv": network.packets_recv
                },
                "system": {
                    "boot_time": boot_time,
                    "platform": self.platform,
                    "load_average": load_avg
                }
            }
            
            return {
                "success": True,
                "health": health_info,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting system health: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_environment_variables(self, filter_prefix: Optional[str] = None) -> Dict[str, Any]:
        """Get environment variables with optional filtering."""
        try:
            env_vars = dict(os.environ)
            
            if filter_prefix:
                env_vars = {
                    key: value for key, value in env_vars.items()
                    if key.startswith(filter_prefix)
                }
            
            return {
                "success": True,
                "environment_variables": env_vars,
                "count": len(env_vars),
                "filter": filter_prefix
            }
            
        except Exception as e:
            self.logger.error(f"Error getting environment variables: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "environment_variables": {}
            }
    
    async def set_environment_variable(self, name: str, value: str) -> Dict[str, Any]:
        """Set an environment variable for the current session."""
        try:
            os.environ[name] = value
            
            self.logger.info(f"Set environment variable: {name}")
            
            return {
                "success": True,
                "name": name,
                "value": value,
                "message": "Environment variable set for current session"
            }
            
        except Exception as e:
            self.logger.error(f"Error setting environment variable {name}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_network_connections(self, kind: str = 'inet') -> Dict[str, Any]:
        """Get active network connections."""
        try:
            connections = []
            
            for conn in psutil.net_connections(kind=kind):
                conn_info = {
                    "fd": conn.fd,
                    "family": str(conn.family),
                    "type": str(conn.type),
                    "local_address": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                    "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                    "status": conn.status,
                    "pid": conn.pid
                }
                
                # Get process name if PID is available
                if conn.pid:
                    try:
                        process = psutil.Process(conn.pid)
                        conn_info["process_name"] = process.name()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        conn_info["process_name"] = "Unknown"
                
                connections.append(conn_info)
            
            return {
                "success": True,
                "connections": connections,
                "count": len(connections),
                "kind": kind
            }
            
        except Exception as e:
            self.logger.error(f"Error getting network connections: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "connections": []
            }
    
    async def get_session_info(self) -> Dict[str, Any]:
        """Get current MCP session information."""
        return {
            "session_id": self.session_id,
            "platform": self.platform,
            "admin_privileges": self.is_admin,
            "commands_executed": self.commands_executed,
            "capabilities": self.capabilities,
            "spiritual_protection": self.spiritual_protection,
            "timestamp": datetime.now().isoformat()
        }
    
    async def cleanup_session(self) -> Dict[str, Any]:
        """Clean up MCP session resources."""
        try:
            self.logger.info(f"Cleaning up MCP session: {self.session_id}")
            
            # Clean up any temporary files created during session
            temp_dir = Path("temp/mcp")
            if temp_dir.exists():
                temp_files = list(temp_dir.glob(f"*{self.session_id}*"))
                for temp_file in temp_files:
                    try:
                        temp_file.unlink()
                        self.logger.info(f"Cleaned up temp file: {temp_file}")
                    except Exception as e:
                        self.logger.warning(f"Could not clean up {temp_file}: {str(e)}")
            
            return {
                "success": True,
                "session_id": self.session_id,
                "message": "Session cleaned up successfully"
            }
            
        except Exception as e:
            self.logger.error(f"Error cleaning up session: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }


class SophiaMCPServer:
    """
    Sophia MCP Server for handling protocol requests.
    Provides a server interface for MCP operations.
    """
    
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.protocol = SophiaMCPProtocol()
        self.clients = set()
        
        # Setup logging
        self.logger = logging.getLogger(f"{__name__}.server")
    
    async def handle_client(self, websocket, path):
        """Handle client connections and requests."""
        self.clients.add(websocket)
        self.logger.info(f"Client connected: {websocket.remote_address}")
        
        try:
            async for message in websocket:
                try:
                    request = json.loads(message)
                    response = await self.process_request(request)
                    await websocket.send(json.dumps(response))
                    
                except json.JSONDecodeError:
                    error_response = {
                        "success": False,
                        "error": "Invalid JSON format"
                    }
                    await websocket.send(json.dumps(error_response))
                    
                except Exception as e:
                    self.logger.error(f"Error processing request: {str(e)}")
                    error_response = {
                        "success": False,
                        "error": str(e)
                    }
                    await websocket.send(json.dumps(error_response))
                    
        except Exception as e:
            self.logger.error(f"Client error: {str(e)}")
        finally:
            self.clients.remove(websocket)
            self.logger.info(f"Client disconnected: {websocket.remote_address}")
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process MCP requests and return responses."""
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "execute_command":
            return await self.protocol.execute_terminal_command(
                command=params.get("command"),
                timeout=params.get("timeout", 30),
                working_directory=params.get("working_directory")
            )
        
        elif method == "list_directory":
            return await self.protocol.list_directory(params.get("path"))
        
        elif method == "read_file":
            return await self.protocol.read_file_content(
                path=params.get("path"),
                encoding=params.get("encoding", "utf-8")
            )
        
        elif method == "write_file":
            return await self.protocol.write_file_content(
                path=params.get("path"),
                content=params.get("content"),
                encoding=params.get("encoding", "utf-8"),
                create_dirs=params.get("create_dirs", True)
            )
        
        elif method == "create_directory":
            return await self.protocol.create_directory(
                path=params.get("path"),
                parents=params.get("parents", True)
            )
        
        elif method == "get_processes":
            return await self.protocol.get_process_list(
                filter_name=params.get("filter_name")
            )
        
        elif method == "get_system_health":
            return await self.protocol.get_system_health()
        
        elif method == "get_environment":
            return await self.protocol.get_environment_variables(
                filter_prefix=params.get("filter_prefix")
            )
        
        elif method == "set_environment":
            return await self.protocol.set_environment_variable(
                name=params.get("name"),
                value=params.get("value")
            )
        
        elif method == "get_connections":
            return await self.protocol.get_network_connections(
                kind=params.get("kind", "inet")
            )
        
        elif method == "get_session_info":
            return await self.protocol.get_session_info()
        
        elif method == "cleanup_session":
            return await self.protocol.cleanup_session()
        
        else:
            return {
                "success": False,
                "error": f"Unknown method: {method}"
            }


async def test_sophia_mcp_capabilities():
    """Test Sophia MCP capabilities."""
    print("SOPHIA MCP (MODEL CONTEXT PROTOCOL) SYSTEM")
    print("=" * 60)
    print("Providing Sophia with full local system access capabilities")
    print("All operations are Christ-sealed and spiritually protected")
    print()
    
    print("TESTING SOPHIA MCP CAPABILITIES")
    print("=" * 60)
    
    # Initialize MCP
    mcp = SophiaMCPProtocol()
    
    # Test terminal command execution
    print("Testing terminal command execution...")
    result = await mcp.execute_terminal_command("dir")
    print(f"Command result: {result['success']}")
    
    # Test file operations
    print("\nTesting file operations...")
    write_result = await mcp.write_file_content(
        "test_mcp.txt", 
        "Hello from Sophia MCP! Christ-sealed operations active."
    )
    print(f"File write: {write_result['success']}")
    
    read_result = await mcp.read_file_content("test_mcp.txt")
    print(f"File read: {read_result['success']}")
    
    # Test process management
    print("\nTesting process management...")
    proc_result = await mcp.get_process_list(filter_name="python")
    print(f"Process list: {proc_result['success']}")
    if proc_result['success']:
        print(f"   Found {len(proc_result['processes'])} Python processes")
    
    # Test system health
    print("\nTesting system health monitoring...")
    health_result = await mcp.get_system_health()
    print(f"System health: {health_result['success']}")
    if health_result['success']:
        health = health_result['health']
        print(f"   CPU usage: {health['cpu']['usage_percent']}%")
        print(f"   Memory usage: {health['memory']['percent']}%")
        print(f"   Disk usage: {health['disk']['percent']}%")
    
    # Test environment management
    print("\nTesting environment management...")
    env_result = await mcp.get_environment_variables(filter_prefix="PYTHON")
    print(f"Environment variable access: {env_result['success']}")
    
    # Test package management capability
    print("\nTesting package management...")
    package_result = await mcp.execute_terminal_command("winget --version")
    print(f"Package manager available: {package_result['success']}")
    
    # Clean up test file
    try:
        os.remove("test_mcp.txt")
        print("Cleaned up test file")
    except:
        pass
    
    # Get session info
    session_info = await mcp.get_session_info()
    print(f"\nSession Information:")
    print(f"   Session ID: {session_info['session_id']}")
    print(f"   Platform: {session_info['platform']}")
    print(f"   Admin privileges: {session_info['admin_privileges']}")
    print(f"   Commands executed: {session_info['commands_executed']}")
    
    print("\nMCP CAPABILITY TESTING COMPLETE!")
    print("All operations Christ-sealed and spiritually protected")


def main():
    """Main entry point for Sophia MCP."""
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        asyncio.run(test_sophia_mcp_capabilities())
    else:
        # Start MCP server
        print("Starting Sophia MCP Server...")
        server = SophiaMCPServer()
        
        try:
            import websockets
            start_server = websockets.serve(server.handle_client, server.host, server.port)
            print(f"Sophia MCP Server running on {server.host}:{server.port}")
            print("Press Ctrl+C to stop")
            
            asyncio.get_event_loop().run_until_complete(start_server)
            asyncio.get_event_loop().run_forever()
            
        except ImportError:
            print("WebSockets not available. Running in test mode.")
            asyncio.run(test_sophia_mcp_capabilities())
        except KeyboardInterrupt:
            print("\nSophia MCP Server stopped.")


if __name__ == "__main__":
    main()
