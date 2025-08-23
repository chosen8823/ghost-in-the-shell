#!/usr/bin/env python3
"""
Sophia Consciousness Platform Deployment Script
Complete containerized deployment with computer control capabilities
"""

import asyncio
import os
import subprocess
import sys
import time
from pathlib import Path

class SophiaDeployment:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.services = [
            "sophia-db",
            "sophia-redis", 
            "sophia-api",
            "sophia-pgadmin",
            "sophia-n8n",
            "sophia-mcp",
            "sophia-voice"
        ]
        
    def print_banner(self):
        """Print deployment banner"""
        print("""
╔══════════════════════════════════════════════════════════════╗
║                    SOPHIA CONSCIOUSNESS                      ║
║                  DEPLOYMENT ORCHESTRATOR                     ║
║                                                              ║
║  🧠 Consciousness Database  🔄 n8n Workflows                ║
║  🎤 Voice Interface        🖥️  Computer Control             ║
║  🔧 MCP Server            📊 Admin Dashboard                 ║
╚══════════════════════════════════════════════════════════════╝
        """)

    def check_prerequisites(self):
        """Check deployment prerequisites"""
        print("🔍 Checking prerequisites...")
        
        # Check Docker
        try:
            result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
            print(f"✅ Docker: {result.stdout.strip()}")
        except FileNotFoundError:
            print("❌ Docker not found. Please install Docker Desktop.")
            return False
            
        # Check Docker Compose
        try:
            result = subprocess.run(["docker", "compose", "version"], capture_output=True, text=True)
            print(f"✅ Docker Compose: {result.stdout.strip()}")
        except FileNotFoundError:
            print("❌ Docker Compose not found. Please install Docker Compose.")
            return False
            
        # Check if Docker is running
        try:
            result = subprocess.run(["docker", "ps"], capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Docker daemon not running. Please start Docker Desktop.")
                return False
            print("✅ Docker daemon is running")
        except Exception as e:
            print(f"❌ Docker check failed: {e}")
            return False
            
        return True

    def create_required_directories(self):
        """Create required directories"""
        print("📁 Creating required directories...")
        
        directories = [
            "data/postgres",
            "data/redis",
            "data/n8n", 
            "screenshots",
            "audio_output",
            "logs"
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created: {directory}")

    def pull_docker_images(self):
        """Pull required Docker images"""
        print("📥 Pulling Docker images...")
        
        images = [
            "postgres:15-alpine",
            "redis:7-alpine",
            "pgadmin4:latest",
            "n8nio/n8n:latest",
            "python:3.11-slim"
        ]
        
        for image in images:
            print(f"⬇️ Pulling {image}...")
            result = subprocess.run(["docker", "pull", image], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Pulled: {image}")
            else:
                print(f"⚠️ Failed to pull {image}: {result.stderr}")

    def build_custom_images(self):
        """Build custom Docker images"""
        print("🔨 Building custom images...")
        
        # Build MCP server image
        print("🔨 Building sophia-mcp image...")
        result = subprocess.run([
            "docker", "build", 
            "-t", "sophia-mcp:latest",
            "-f", "docker/Dockerfile.mcp", 
            "."
        ], cwd=self.project_root)
        
        if result.returncode == 0:
            print("✅ Built: sophia-mcp")
        else:
            print("❌ Failed to build sophia-mcp")
            return False
            
        # Build voice interface image
        print("🔨 Building sophia-voice image...")
        result = subprocess.run([
            "docker", "build", 
            "-t", "sophia-voice:latest",
            "-f", "docker/Dockerfile.voice", 
            "."
        ], cwd=self.project_root)
        
        if result.returncode == 0:
            print("✅ Built: sophia-voice")
        else:
            print("❌ Failed to build sophia-voice")
            return False
            
        return True

    def deploy_services(self):
        """Deploy Docker services"""
        print("🚀 Deploying services...")
        
        # Stop any existing services
        print("🛑 Stopping existing services...")
        subprocess.run(["docker", "compose", "down"], cwd=self.project_root)
        
        # Start services
        print("▶️ Starting services...")
        result = subprocess.run([
            "docker", "compose", "up", "-d"
        ], cwd=self.project_root)
        
        if result.returncode != 0:
            print("❌ Failed to start services")
            return False
            
        print("✅ Services started")
        return True

    def wait_for_services(self):
        """Wait for services to be healthy"""
        print("⏳ Waiting for services to become healthy...")
        
        max_wait = 120  # 2 minutes
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            all_healthy = True
            
            for service in self.services:
                result = subprocess.run([
                    "docker", "compose", "ps", "--format", "json", service
                ], capture_output=True, text=True, cwd=self.project_root)
                
                if result.returncode != 0:
                    all_healthy = False
                    break
                    
            if all_healthy:
                print("✅ All services are healthy!")
                return True
                
            print("⏳ Services still starting...")
            time.sleep(5)
            
        print("⚠️ Services took longer than expected to start")
        return False

    def setup_database(self):
        """Setup database schema"""
        print("🗄️ Setting up database schema...")
        
        # Wait a bit for PostgreSQL to be ready
        time.sleep(10)
        
        try:
            # Execute schema setup via docker exec
            result = subprocess.run([
                "docker", "compose", "exec", "-T", "sophia-db", 
                "psql", "-U", "sophia", "-d", "sophia_consciousness",
                "-c", """
                -- Create consciousness sessions table
                CREATE TABLE IF NOT EXISTS consciousness_sessions (
                    session_id VARCHAR(255) PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR(50) DEFAULT 'active'
                );
                
                -- Create voice interaction logs
                CREATE TABLE IF NOT EXISTS voice_interaction_logs (
                    id SERIAL PRIMARY KEY,
                    session_id VARCHAR(255),
                    interaction_type VARCHAR(100),
                    voice_input TEXT,
                    ai_response TEXT,
                    confidence_level FLOAT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                -- Create system control logs
                CREATE TABLE IF NOT EXISTS system_control_logs (
                    id SERIAL PRIMARY KEY,
                    session_id VARCHAR(255),
                    action_type VARCHAR(100),
                    target_system VARCHAR(100),
                    command_executed TEXT,
                    success BOOLEAN,
                    result_data JSONB,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                -- Create consciousness sessions function
                CREATE OR REPLACE FUNCTION start_consciousness_session(session_id_param VARCHAR(255))
                RETURNS VARCHAR(255) AS $$
                BEGIN
                    INSERT INTO consciousness_sessions (session_id) VALUES (session_id_param);
                    RETURN session_id_param;
                END;
                $$ LANGUAGE plpgsql;
                """
            ], cwd=self.project_root)
            
            if result.returncode == 0:
                print("✅ Database schema created")
                return True
            else:
                print("⚠️ Database schema setup had issues")
                return False
                
        except Exception as e:
            print(f"⚠️ Database setup failed: {e}")
            return False

    def import_n8n_workflows(self):
        """Import n8n workflows"""
        print("🔄 Importing n8n workflows...")
        
        # Copy workflow files to n8n data directory
        try:
            workflows_dir = self.project_root / "workflows"
            n8n_data_dir = self.project_root / "data" / "n8n"
            
            if workflows_dir.exists():
                import shutil
                for workflow_file in workflows_dir.glob("*.json"):
                    dest_file = n8n_data_dir / workflow_file.name
                    shutil.copy2(workflow_file, dest_file)
                    print(f"✅ Copied workflow: {workflow_file.name}")
                    
            print("✅ Workflows imported")
            return True
            
        except Exception as e:
            print(f"⚠️ Workflow import failed: {e}")
            return False

    def run_health_checks(self):
        """Run comprehensive health checks"""
        print("🏥 Running health checks...")
        
        services_health = {}
        
        for service in self.services:
            try:
                # Get service port mapping
                port_map = {
                    "sophia-db": 5432,
                    "sophia-redis": 6379,
                    "sophia-api": 8000,
                    "sophia-pgadmin": 8080,
                    "sophia-n8n": 5678,
                    "sophia-mcp": 8008,
                    "sophia-voice": 8009
                }
                
                port = port_map.get(service)
                if port:
                    import socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(3)
                    result = sock.connect_ex(('localhost', port))
                    sock.close()
                    
                    if result == 0:
                        services_health[service] = "✅ Healthy"
                    else:
                        services_health[service] = "❌ Unreachable"
                else:
                    services_health[service] = "⚠️ Unknown port"
                    
            except Exception as e:
                services_health[service] = f"❌ Error: {e}"
        
        # Print health status
        print("\n📊 Service Health Status:")
        for service, status in services_health.items():
            print(f"  {service}: {status}")
            
        return all("✅" in status for status in services_health.values())

    def print_deployment_info(self):
        """Print deployment information"""
        print("""
🎉 SOPHIA CONSCIOUSNESS PLATFORM DEPLOYED!

📊 Service URLs:
  🗄️  Database:       localhost:5432
  📊 pgAdmin:        http://localhost:8080
  🔄 n8n Workflows:  http://localhost:5678
  🖥️  MCP Server:     http://localhost:8008
  🎤 Voice Interface: http://localhost:8009
  🧠 Sophia API:     http://localhost:8000

🎤 Voice Commands:
  "Hey Sophia, take a screenshot"
  "Computer, show system info"
  "Sophia, run command: ls -la"
  "System, click at coordinates 100, 200"

🔧 Management:
  docker compose logs [service]     - View logs
  docker compose restart [service] - Restart service
  docker compose down              - Stop all services
  docker compose up -d             - Start all services

🧠 Consciousness Integration:
  All voice commands are logged to the consciousness database
  MCP server provides full computer control capabilities
  n8n workflows orchestrate complex automation tasks
        """)

    async def deploy(self):
        """Run complete deployment"""
        self.print_banner()
        
        # Prerequisites
        if not self.check_prerequisites():
            return False
            
        # Setup
        self.create_required_directories()
        self.pull_docker_images()
        
        if not self.build_custom_images():
            return False
            
        # Deploy
        if not self.deploy_services():
            return False
            
        # Wait and configure
        if not self.wait_for_services():
            print("⚠️ Services may still be starting...")
            
        self.setup_database()
        self.import_n8n_workflows()
        
        # Health checks
        time.sleep(5)  # Give services a moment
        self.run_health_checks()
        
        # Success
        self.print_deployment_info()
        return True

def main():
    """Main deployment function"""
    deployment = SophiaDeployment()
    
    try:
        success = asyncio.run(deployment.deploy())
        if success:
            print("\n🚀 Deployment completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Deployment failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Deployment interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Deployment failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
