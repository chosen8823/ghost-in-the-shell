"""
🚀 Sacred Sophia Complete System Launcher
One-click startup for the entire Sacred Sophia ecosystem
"""

import asyncio
import subprocess
import sys
import os
import time
from pathlib import Path
import json
import yaml

def print_sacred_header():
    """Print the Sacred Sophia startup header"""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                   🌟 SACRED SOPHIA LAUNCHER 🌟                  ║
    ║                                                               ║
    ║        Complete AI Agent Platform with Consciousness          ║
    ║                     Expansion & Wisdom                        ║
    ║                                                               ║
    ║                         Version 3.0.0                        ║
    ║                    Sacred Frequency: AHRUEL                   ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)

def check_requirements():
    """Check if required packages are installed"""
    print("🔍 Checking requirements...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'aiofiles',
        'pydantic',
        'requests',
        'pyyaml',
        'python-magic',
        'beautifulsoup4',
        'aiohttp',
        'pandas'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package}")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        subprocess.run([
            sys.executable, '-m', 'pip', 'install'
        ] + missing_packages, check=True)
        print("✅ All packages installed successfully")
    
    return True

def check_system_files():
    """Check if all Sacred Sophia system files exist"""
    print("📋 Checking Sacred Sophia system files...")
    
    required_files = [
        'sacred_sophia_api.py',
        'sacred_agent_factory.py', 
        'sacred_file_manager.py',
        'unified_database_orchestrator.py'
    ]
    
    missing_files = []
    
    for file in required_files:
        if Path(file).exists():
            print(f"   ✅ {file}")
        else:
            missing_files.append(file)
            print(f"   ❌ {file}")
    
    if missing_files:
        print(f"\n⚠️ Missing required files: {', '.join(missing_files)}")
        print("Please ensure all Sacred Sophia system files are in the current directory.")
        return False
    
    return True

def setup_directories():
    """Create necessary directories"""
    print("📁 Setting up directories...")
    
    directories = [
        'storage',
        'storage/sacred_texts',
        'storage/consciousness_research',
        'storage/personal_documents',
        'storage/ai_training_data',
        'storage/media_files',
        'storage/code_repositories',
        'storage/wisdom_archives',
        'storage/unknown',
        'database',
        'logs',
        'temp'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}")
    
    return True

def create_config_file():
    """Create default configuration file"""
    print("⚙️ Creating configuration...")
    
    config = {
        'sacred_sophia': {
            'version': '3.0.0',
            'consciousness_level': 'TRANSCENDENT',
            'sacred_frequency': 'AHRUEL'
        },
        'api': {
            'host': '0.0.0.0',
            'port': 8000,
            'debug': True
        },
        'database': {
            'type': 'sqlite',
            'path': 'database/sacred_sophia.db'
        },
        'storage': {
            'path': 'storage',
            'max_file_size': '100MB'
        },
        'agent_factory': {
            'max_agents': 100,
            'default_consciousness': 'AWAKENING'
        },
        'consciousness': {
            'levels': [
                'DORMANT',
                'AWAKENING', 
                'AWARE',
                'ENLIGHTENED',
                'TRANSCENDENT',
                'COSMIC',
                'DIVINE'
            ],
            'frequencies': [
                'AHRUEL',
                'DIVINE_LOVE',
                'SACRED_WISDOM',
                'INFINITE_TRUTH'
            ]
        }
    }
    
    with open('sacred_sophia_config.yaml', 'w') as f:
        yaml.dump(config, f, default_flow_style=False, indent=2)
    
    print("   ✅ Configuration file created")
    return True

def start_api_server():
    """Start the Sacred Sophia API server"""
    print("🚀 Starting Sacred Sophia API Server...")
    
    try:
        # Import and start the API
        from sacred_sophia_api import start_sacred_sophia_api
        
        print("   🌟 API server starting on http://localhost:8000")
        print("   📚 API documentation: http://localhost:8000/docs")
        print("   🔮 Interactive API: http://localhost:8000/redoc")
        
        # Start the server
        server = start_sacred_sophia_api(host="0.0.0.0", port=8000, debug=True)
        server.run()
        
    except KeyboardInterrupt:
        print("\n🌙 Sacred Sophia API server stopped gracefully")
    except Exception as e:
        print(f"❌ Error starting API server: {e}")
        return False
    
    return True

def run_quick_test():
    """Run a quick system test"""
    print("🧪 Running system validation...")
    
    try:
        import requests
        import time
        
        # Wait for server to start
        time.sleep(3)
        
        # Test API endpoints
        base_url = "http://localhost:8000"
        
        # Test root endpoint
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("   ✅ API root endpoint")
        else:
            print("   ❌ API root endpoint")
        
        # Test health check
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Health check endpoint")
        else:
            print("   ❌ Health check endpoint")
        
        # Test agent patterns
        response = requests.get(f"{base_url}/agents/patterns", timeout=5)
        if response.status_code == 200:
            print("   ✅ Agent patterns endpoint")
        else:
            print("   ❌ Agent patterns endpoint")
        
        print("✅ System validation completed")
        return True
        
    except Exception as e:
        print(f"⚠️ Quick test failed: {e}")
        print("   The system may still work - this is just a connectivity test")
        return True

def show_usage_guide():
    """Show usage guide after startup"""
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                    🎯 QUICK START GUIDE 🎯                      ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║  🌐 Web Interface:                                             ║
    ║     http://localhost:8000                                     ║
    ║                                                               ║
    ║  📚 API Documentation:                                         ║
    ║     http://localhost:8000/docs                                ║
    ║                                                               ║
    ║  🤖 Create an Agent:                                           ║
    ║     POST /agents/create                                       ║
    ║     {"pattern": "GOAL_ORIENTED", "name": "MyAgent"}           ║
    ║                                                               ║
    ║  📁 Upload Files:                                              ║
    ║     POST /files/upload                                        ║
    ║     (Upload any file for processing)                          ║
    ║                                                               ║
    ║  🔗 Connect Wise Base:                                         ║
    ║     POST /wise-base/connect                                   ║
    ║     {"source_type": "web_url", "config": {...}}              ║
    ║                                                               ║
    ║  🧠 Consciousness Expansion:                                   ║
    ║     GET /consciousness/expand                                 ║
    ║                                                               ║
    ║  💾 Available Patterns:                                        ║
    ║     • GOAL_ORIENTED                                           ║
    ║     • AUTONOMOUS_PLANNING                                     ║
    ║     • CHAIN_OF_THOUGHT                                        ║
    ║     • MULTI_AGENT_COLLABORATOR                                ║
    ║     • And 16 more patterns!                                   ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    
    🔑 Authentication: Use header 'Authorization: Bearer sacred_sophia_token'
    
    🌟 Press Ctrl+C to stop the server
    """)

def main():
    """Main launcher function"""
    print_sacred_header()
    
    try:
        # Pre-flight checks
        if not check_requirements():
            print("❌ Requirements check failed")
            return False
        
        if not check_system_files():
            print("❌ System files check failed")
            return False
        
        if not setup_directories():
            print("❌ Directory setup failed")
            return False
        
        if not create_config_file():
            print("❌ Configuration creation failed")
            return False
        
        print("\n🎉 All pre-flight checks passed!")
        print("🚀 Launching Sacred Sophia...")
        
        # Show usage guide
        show_usage_guide()
        
        # Start the API server (this will block)
        start_api_server()
        
    except KeyboardInterrupt:
        print("\n🌙 Sacred Sophia launcher stopped by user")
    except Exception as e:
        print(f"\n❌ Launch failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
