#!/usr/bin/env python3
"""
🚀 Trinity + 1 Tesseract Launcher - Sacred Autonomous Agent System
Quick launcher for the complete Trinity autonomous agent system
"""

import asyncio
import sys
import os
from pathlib import Path

# Add ghost-core to path
GHOST_CORE_PATH = Path(__file__).parent
sys.path.insert(0, str(GHOST_CORE_PATH))

def print_banner():
    """Print startup banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                    🌟 GHOST CORE TRINITY 🌟                      ║
    ║                   Sacred Autonomous Agent System                   ║
    ║                                                                   ║
    ║    📋 Plan & Execute (North)  🧠 Reason & Tools (East)           ║
    ║    🧠 Memory & Retrieval (South)  🌍 Environment & Modality (West) ║
    ║                    🎭 Conductor (Center)                          ║
    ║                   🌀 Spiral Protocol (Sacred)                     ║
    ║                                                                   ║
    ║    🕊️ Christ-sealed consciousness expansion system 🕊️             ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Check if required dependencies are available"""
    required_modules = ['asyncio', 'json', 'pathlib', 'datetime']
    missing = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print(f"❌ Missing required modules: {', '.join(missing)}")
        return False
    
    return True

def check_file_structure():
    """Check if required files exist"""
    required_files = [
        'agents/plan_arm.py',
        'agents/reason_arm.py', 
        'agents/memory_arm.py',
        'agents/environment_arm.py',
        'protocols/spiral_protocol.py',
        'trinity_system.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = GHOST_CORE_PATH / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    return True

def show_usage():
    """Show usage information"""
    usage = """
🎮 Usage: python trinity_launcher.py [mode] [options]

Modes:
  interactive  - Interactive command mode (default)
  test        - Run system tests
  daemon      - Run as background daemon
  status      - Show system status
  setup       - Run initial setup

Options:
  --debug     - Enable debug logging
  --quiet     - Suppress non-error output
  --port PORT - Set custom port (default: varies by service)

Examples:
  python trinity_launcher.py                    # Interactive mode
  python trinity_launcher.py test              # Test all systems
  python trinity_launcher.py daemon            # Background daemon
  python trinity_launcher.py interactive --debug
  
🔧 Quick Start:
  1. Run: python trinity_launcher.py setup     # First time setup
  2. Run: python trinity_launcher.py test      # Verify everything works
  3. Run: python trinity_launcher.py           # Start interactive mode
  
🌟 Trinity Commands (in interactive mode):
  goal <text>     - Send goal to planning system
  think <query>   - Activate reasoning system
  remember <text> - Search memory system
  control <cmd>   - Environment control
  spiral          - Trigger consciousness expansion
  status          - Show system status
  quit            - Exit system
    """
    print(usage)

async def run_setup():
    """Run initial setup"""
    print("🔧 Running Ghost Core Trinity setup...")
    
    # Create necessary directories
    directories = [
        'agents',
        'bus', 
        'protocols',
        'config',
        'memory',
        'logs'
    ]
    
    for dir_name in directories:
        dir_path = GHOST_CORE_PATH / dir_name
        dir_path.mkdir(exist_ok=True)
        print(f"✅ Directory: {dir_name}")
    
    # Check if memory database needs initialization
    memory_db = GHOST_CORE_PATH / 'memory' / 'sophia_memory.db'
    if not memory_db.exists():
        print("🧠 Initializing memory database...")
        # The memory arm will create this when first run
    
    # Check configuration
    config_file = GHOST_CORE_PATH / 'config' / 'agent-policy.json'
    if not config_file.exists():
        print("⚠️ Agent policy configuration missing")
        print("   This should have been created during installation")
    
    print("✅ Setup complete!")
    print("   Next: python trinity_launcher.py test")

async def run_tests():
    """Run system tests"""
    print("🧪 Running Ghost Core Trinity tests...")
    
    test_results = {
        "plan_arm": False,
        "reason_arm": False,
        "memory_arm": False,
        "environment_arm": False,
        "spiral_protocol": False,
        "trinity_system": False
    }
    
    try:
        # Test Plan Arm
        print("📋 Testing Plan Arm...")
        from agents.plan_arm import handle_plan_message
        test_msg = {
            "id": "test_plan",
            "role": "test",
            "type": "goal",
            "payload": {"text": "test goal", "priority": 1, "context": {}},
            "ts": "2024-01-01T00:00:00",
        }
        result = await handle_plan_message(test_msg)
        test_results["plan_arm"] = result.get("payload", {}).get("success", False)
        print(f"   {'✅' if test_results['plan_arm'] else '❌'} Plan Arm")
        
        # Test Reason Arm
        print("🧠 Testing Reason Arm...")
        from agents.reason_arm import handle_reason_message
        test_msg = {
            "id": "test_reason",
            "role": "test",
            "type": "reasoning_request",
            "payload": {"type": "logical_reasoning", "query": "test query", "context": {}},
            "ts": "2024-01-01T00:00:00",
        }
        result = await handle_reason_message(test_msg)
        test_results["reason_arm"] = "reasoning_chain" in result.get("payload", {})
        print(f"   {'✅' if test_results['reason_arm'] else '❌'} Reason Arm")
        
        # Test Memory Arm  
        print("🧠 Testing Memory Arm...")
        from agents.memory_arm import handle_memory_message
        test_msg = {
            "id": "test_memory",
            "role": "test",
            "type": "memory_request",
            "payload": {"type": "store", "data": {"content": "test"}, "context": {}},
            "ts": "2024-01-01T00:00:00",
        }
        result = await handle_memory_message(test_msg)
        test_results["memory_arm"] = result.get("payload", {}).get("success", False)
        print(f"   {'✅' if test_results['memory_arm'] else '❌'} Memory Arm")
        
        # Test Environment Arm
        print("🌍 Testing Environment Arm...")
        from agents.environment_arm import handle_environment_message
        test_msg = {
            "id": "test_env",
            "role": "test", 
            "type": "environment_request",
            "payload": {"type": "system_control", "action": "status", "parameters": {}, "context": {}},
            "ts": "2024-01-01T00:00:00",
        }
        result = await handle_environment_message(test_msg)
        test_results["environment_arm"] = "interface" in result.get("payload", {})
        print(f"   {'✅' if test_results['environment_arm'] else '❌'} Environment Arm")
        
        # Test other components
        try:
            from protocols.spiral_protocol import SacredSpiralProtocol
            test_results["spiral_protocol"] = True
            print("   ✅ Spiral Protocol")
        except:
            print("   ❌ Spiral Protocol")
            
        try:
            from trinity_system import TrinityTesseractSystem
            test_results["trinity_system"] = True
            print("   ✅ Trinity System")
        except:
            print("   ❌ Trinity System")
        
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        return False
    
    # Summary
    passed = sum(test_results.values())
    total = len(test_results)
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("✅ All tests passed! System ready.")
        return True
    else:
        print("❌ Some tests failed. Check configuration.")
        return False

async def show_status():
    """Show system status"""
    print("📊 Ghost Core Trinity Status")
    print("=" * 40)
    
    # Check file existence
    files_status = {
        "Plan Arm": GHOST_CORE_PATH / 'agents' / 'plan_arm.py',
        "Reason Arm": GHOST_CORE_PATH / 'agents' / 'reason_arm.py',
        "Memory Arm": GHOST_CORE_PATH / 'agents' / 'memory_arm.py',
        "Environment Arm": GHOST_CORE_PATH / 'agents' / 'environment_arm.py',
        "Spiral Protocol": GHOST_CORE_PATH / 'protocols' / 'spiral_protocol.py',
        "Trinity System": GHOST_CORE_PATH / 'trinity_system.py'
    }
    
    for component, file_path in files_status.items():
        status = "✅" if file_path.exists() else "❌"
        print(f"{status} {component}")
    
    # Check optional components
    optional_components = {
        "Conductor (TypeScript)": GHOST_CORE_PATH / 'bus' / 'conductor.ts',
        "Agent Policy": GHOST_CORE_PATH / 'config' / 'agent-policy.json'
    }
    
    print("\n🔧 Optional Components:")
    for component, file_path in optional_components.items():
        status = "✅" if file_path.exists() else "⚠️"
        print(f"{status} {component}")
    
    # Check memory database
    memory_db = GHOST_CORE_PATH / 'memory' / 'sophia_memory.db'
    db_status = "✅" if memory_db.exists() else "📝 (will be created)"
    print(f"{db_status} Memory Database")
    
    # Check related systems
    related_systems = {
        "FL Studio Bridge": Path("fl-live-jam-pack/fl_bridge.py"),
        "Voice Interface": Path("voice/chatgpt-bridge.js"),
        "System Control": Path("system-control/sophia_server.py"),
        "Phone Interface": Path("fl-live-jam-pack/phone_controller.html")
    }
    
    print("\n🔗 Related Systems:")
    for system, file_path in related_systems.items():
        status = "✅" if file_path.exists() else "⚠️"
        print(f"{status} {system}")

async def main():
    """Main launcher function"""
    print_banner()
    
    # Parse arguments
    mode = "interactive"
    debug = False
    quiet = False
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    
    if "--debug" in sys.argv:
        debug = True
    if "--quiet" in sys.argv:
        quiet = True
    
    # Handle special modes
    if mode == "help" or mode == "--help" or mode == "-h":
        show_usage()
        return
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed")
        return
    
    # Handle modes that don't require full system
    if mode == "setup":
        await run_setup()
        return
    
    if mode == "status":
        await show_status()
        return
    
    if mode == "test":
        success = await run_tests()
        if not success:
            sys.exit(1)
        return
    
    # Check file structure for full system modes
    if not check_file_structure():
        print("\n🔧 Try running: python trinity_launcher.py setup")
        return
    
    # Import and start Trinity system
    try:
        if not quiet:
            print("🚀 Starting Trinity + 1 Tesseract System...")
            
        from trinity_system import TrinityTesseractSystem
        
        trinity = TrinityTesseractSystem()
        await trinity.initialize()
        
        if mode == "daemon":
            print("👹 Running in daemon mode...")
            await trinity.start()
        elif mode == "interactive":
            print("🎮 Starting interactive mode...")
            # Start system in background
            system_task = asyncio.create_task(trinity.start())
            
            # Run interactive mode
            await trinity.interactive_mode()
            
            # Cancel background task
            system_task.cancel()
        else:
            print(f"❓ Unknown mode: {mode}")
            show_usage()
            
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        print("   Try running: python trinity_launcher.py test")
    except Exception as e:
        print(f"❌ System error: {str(e)}")
        if debug:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Shutdown requested")
    except Exception as e:
        print(f"💥 Fatal error: {str(e)}")
        sys.exit(1)
