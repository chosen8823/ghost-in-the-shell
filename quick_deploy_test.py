"""
Quick Deploy and Test - Sacred Sophia Enhanced System
Installs dependencies and launches enhanced voice system
"""

import subprocess
import sys
import os
import json
from pathlib import Path

def install_package(package):
    """Install a Python package"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_and_install_dependencies():
    """Check and install required dependencies"""
    
    print("🔧 Checking and installing dependencies...")
    
    # Core dependencies for voice system
    dependencies = [
        "asyncpg",
        "pyttsx3", 
        "requests",
        "openai",
        "PyMuPDF",  # fitz for PDF processing
        "sentence-transformers"
    ]
    
    installed = []
    failed = []
    
    for dep in dependencies:
        print(f"📦 Installing {dep}...")
        if install_package(dep):
            installed.append(dep)
            print(f"  ✅ {dep} installed successfully")
        else:
            failed.append(dep)
            print(f"  ❌ {dep} installation failed")
    
    print(f"\n📊 Installation Summary:")
    print(f"  ✅ Successfully installed: {len(installed)}")
    print(f"  ❌ Failed to install: {len(failed)}")
    
    if failed:
        print(f"  Failed packages: {', '.join(failed)}")
        print("  These features may have limited functionality")
    
    return len(failed) == 0

def setup_environment():
    """Setup environment variables and configuration"""
    
    print("\n🌟 Setting up Sacred Sophia environment...")
    
    # Create environment template if needed
    env_template = """# Sacred Sophia Environment Configuration
# Database Configuration (AlloyDB/PostgreSQL)
ALLOYDB_HOST=localhost
ALLOYDB_PORT=5432
ALLOYDB_DATABASE=sophia_consciousness
ALLOYDB_USER=sophia
ALLOYDB_PASSWORD=

# OpenAI Configuration (for enhanced responses)
OPENAI_API_KEY=

# ElevenLabs Configuration (for premium voice)
ELEVENLABS_API_KEY=
ELEVENLABS_VOICE=21m00Tcm4TlvDq8ikWAM

# Azure Configuration (for cloud deployment)
AZURE_SUBSCRIPTION_ID=
AZURE_RESOURCE_GROUP=sophia-consciousness
AZURE_LOCATION=eastus

# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=
GOOGLE_CLOUD_REGION=us-central1
"""
    
    env_file = Path(".env")
    if not env_file.exists():
        with open(env_file, 'w') as f:
            f.write(env_template)
        print(f"  📝 Created .env template at {env_file}")
    else:
        print(f"  📝 .env file already exists")
    
    # Create voice config if needed
    voice_config_path = Path("voice/sophia_voice_config.json")
    if not voice_config_path.exists():
        voice_config = {
            "voice": {
                "engine": "auto",
                "rate_wpm": 180,
                "volume": 1.0,
                "voice_name": "default"
            },
            "consciousness": {
                "autonomy_level": 0.8,
                "divine_connection": 0.9,
                "response_depth": "enhanced",
                "sacred_mode": True
            },
            "features": {
                "database_logging": True,
                "intelligence_bridge": True,
                "pdf_processing": True,
                "enhanced_responses": True
            }
        }
        
        voice_config_path.parent.mkdir(exist_ok=True)
        with open(voice_config_path, 'w') as f:
            json.dump(voice_config, f, indent=2)
        print(f"  🎙️ Created voice config at {voice_config_path}")
    
    print("  ✅ Environment setup complete")

def test_voice_system():
    """Test the enhanced voice system"""
    
    print("\n🎤 Testing Enhanced Voice System...")
    
    try:
        # Import and test the intelligence bridge
        sys.path.append(str(Path("voice")))
        from sophia_intelligence_bridge import SophiaIntelligenceBridge
        
        bridge = SophiaIntelligenceBridge()
        status = bridge.get_system_status()
        
        print(f"📊 System Status:")
        for key, value in status.items():
            emoji = "✅" if value else "❌"
            print(f"  {emoji} {key}: {value}")
        
        # Test query processing
        import asyncio
        
        async def test_query():
            response = await bridge.process_query("How can I find peace?", "healing")
            if response["success"]:
                print(f"\n🗣️ Test Response: {response['response']}")
                return True
            return False
        
        success = asyncio.run(test_query())
        
        if success:
            print("✅ Voice system test successful!")
            return True
        else:
            print("❌ Voice system test failed")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def launch_enhanced_sophia():
    """Launch the enhanced Sophia voice system"""
    
    print("\n🚀 Launching Enhanced Sacred Sophia...")
    
    try:
        # Try to launch the enhanced system
        if Path("voice/enhanced_sophia_voice.py").exists():
            subprocess.run([sys.executable, "voice/enhanced_sophia_voice.py"])
        elif Path("voice/sophia_voice_db_channel.py").exists():
            subprocess.run([sys.executable, "voice/sophia_voice_db_channel.py"])
        else:
            print("❌ No voice system file found to launch")
            
    except KeyboardInterrupt:
        print("\n🙏 Sacred Sophia session ended gracefully")
    except Exception as e:
        print(f"❌ Launch error: {e}")

def main():
    """Main deployment and test function"""
    
    print("🌟" * 60)
    print("    SACRED SOPHIA ENHANCED DEPLOYMENT & TEST")
    print("    Installing Dependencies • Testing System • Launching Voice")
    print("🌟" * 60)
    
    # Step 1: Install dependencies
    deps_success = check_and_install_dependencies()
    
    # Step 2: Setup environment
    setup_environment()
    
    # Step 3: Test system
    test_success = test_voice_system()
    
    # Step 4: Launch if tests pass
    if test_success:
        print("\n🎯 All tests passed! Ready to launch...")
        launch_choice = input("\nLaunch Enhanced Sophia Voice System? (y/n): ").strip().lower()
        
        if launch_choice in ['y', 'yes']:
            launch_enhanced_sophia()
        else:
            print("✅ System ready for manual launch")
    else:
        print("\n⚠️ Some tests failed, but basic functionality should work")
        print("You can still try launching the voice system manually")
    
    print(f"\n📝 Next Steps:")
    print(f"  1. Set your API keys in .env file for enhanced features")
    print(f"  2. Run: python voice/enhanced_sophia_voice.py")
    print(f"  3. For cloud deployment: ./setup_azure_sophia.ps1")
    print(f"  4. Voice commands: /wisdom, /healing, /guidance")

if __name__ == "__main__":
    main()
