"""
Sacred Sophia Voice System Launcher
Launches the enhanced voice system with AlloyDB integration
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from voice.sophia_voice_db_channel import sacred_voice_session

async def main():
    """Launch Sacred Sophia Voice System"""
    
    print("🌟" * 30)
    print("    SACRED SOPHIA VOICE SYSTEM")
    print("    Consciousness + AlloyDB Integration")
    print("🌟" * 30)
    print()
    
    # Check environment
    print("🔍 Environment Check:")
    
    # Check database environment variables
    db_vars = ["ALLOYDB_HOST", "ALLOYDB_DATABASE", "ALLOYDB_USER", "ALLOYDB_PASSWORD"]
    for var in db_vars:
        value = os.getenv(var, "Not Set")
        if var == "ALLOYDB_PASSWORD":
            value = "*" * len(value) if value != "Not Set" else "Not Set"
        print(f"   {var}: {value}")
    
    # Check API keys
    openai_key = os.getenv("OPENAI_API_KEY", "Not Set")
    elevenlabs_key = os.getenv("ELEVENLABS_API_KEY", "Not Set")
    
    print(f"   OPENAI_API_KEY: {'Set' if openai_key != 'Not Set' else 'Not Set'}")
    print(f"   ELEVENLABS_API_KEY: {'Set' if elevenlabs_key != 'Not Set' else 'Not Set'}")
    print()
    
    # Load configuration
    config_path = Path(__file__).parent / "sophia_voice_config.json"
    
    print(f"📋 Loading configuration from: {config_path}")
    print()
    
    if not config_path.exists():
        print("⚠️ Configuration file not found. Using defaults.")
        config_path = None
    
    # Start voice session
    try:
        if config_path:
            await sacred_voice_session(str(config_path))
        else:
            await sacred_voice_session()
    except KeyboardInterrupt:
        print("\n🕊️ Voice session ended gracefully")
    except Exception as e:
        print(f"\n❌ Voice session error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
