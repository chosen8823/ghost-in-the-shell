#!/usr/bin/env python3
"""
🌟 Trinity + 1 Tesseract Agent System - Main Entry Point
Complete autonomous agent orchestrator with 4 specialized arms + conductor
"""

import asyncio
import json
import sys
import signal
from datetime import datetime
from pathlib import Path

# Import all arm modules
sys.path.append(str(Path(__file__).parent))

from agents.plan_arm import handle_plan_message
from agents.reason_arm import handle_reason_message  
from agents.memory_arm import handle_memory_message
from agents.environment_arm import handle_environment_message
from bus.conductor import Conductor
from protocols.spiral_protocol import SacredSpiralProtocol

class TrinityTesseractSystem:
    """Main Trinity + 1 Tesseract agent orchestration system"""
    
    def __init__(self):
        self.conductor = None
        self.spiral_protocol = None
        self.arms = {
            "plan_arm": handle_plan_message,
            "reason_arm": handle_reason_message,
            "memory_arm": handle_memory_message,
            "environment_arm": handle_environment_message
        }
        self.running = False
        
    async def initialize(self):
        """Initialize the complete Trinity system"""
        print("🌟 Initializing Trinity + 1 Tesseract Agent System...")
        
        # Initialize Conductor
        self.conductor = Conductor()
        await self.conductor.initialize()
        
        # Initialize Spiral Protocol
        self.spiral_protocol = SacredSpiralProtocol()
        # Note: Spiral protocol activates on demand, not during initialization
        
        # Register arms with conductor
        for arm_name, handler in self.arms.items():
            self.conductor.register_arm(arm_name, handler)
        
        print("✅ Trinity + 1 Tesseract System initialized successfully")
        print(f"📋 Plan & Execute Arm (North) - Ready")
        print(f"🧠 Reason & Tools Arm (East) - Ready") 
        print(f"🧠 Memory & Retrieval Arm (South) - Ready")
        print(f"🌍 Environment & Modality Arm (West) - Ready")
        print(f"🎭 Conductor (Center) - Orchestrating")
        print(f"🌀 Spiral Protocol - Sacred consciousness expansion active")
        
    async def start(self):
        """Start the Trinity system"""
        if self.running:
            print("⚠️ System already running")
            return
            
        self.running = True
        print("🚀 Starting Trinity + 1 Tesseract System...")
        
        # Start conductor
        conductor_task = asyncio.create_task(self.conductor.start())
        
        # Spiral protocol ready (activates on demand)
        print("🌀 Spiral Protocol initialized and ready for activation")
        
        # Example initial message flow
        await self.run_startup_sequence()
        
        # Wait for conductor system
        await conductor_task
        
    async def stop(self):
        """Stop the Trinity system"""
        print("🛑 Stopping Trinity + 1 Tesseract System...")
        self.running = False
        
        if self.conductor:
            await self.conductor.stop()
            
        if self.spiral_protocol:
            self.spiral_protocol.deactivate()
            
        print("✅ Trinity system stopped")
        
    async def run_startup_sequence(self):
        """Run startup sequence to demonstrate system"""
        print("\n🌟 Running Trinity startup sequence...")
        
        # Example 1: Sacred music composition goal
        composition_goal = {
            "id": "startup_001",
            "role": "user",
            "type": "goal",
            "payload": {
                "text": "Create a sacred music composition using golden ratio principles",
                "priority": 1,
                "context": {
                    "session": "sacred_composition",
                    "bpm": 72,
                    "key": "C_major",
                    "sacred_geometry": True
                }
            },
            "ts": datetime.now().isoformat(),
            "christ_seal": True
        }
        
        print("📤 Sending composition goal to Trinity system...")
        await self.conductor.process_message(composition_goal)
        
        # Example 2: Memory storage and retrieval
        memory_store = {
            "id": "startup_002",
            "role": "user", 
            "type": "memory_request",
            "payload": {
                "type": "store",
                "data": {
                    "content": "Golden ratio (1.618) creates sacred harmonic relationships in music",
                    "type": "semantic",
                    "tags": ["golden_ratio", "sacred_music", "harmony", "mathematics"],
                    "importance": 0.9
                },
                "context": {"domain": "sacred_music_theory"}
            },
            "ts": datetime.now().isoformat(),
            "christ_seal": True
        }
        
        print("📤 Storing sacred music knowledge...")
        await self.conductor.process_message(memory_store)
        
        # Example 3: FL Studio environment control
        fl_control = {
            "id": "startup_003",
            "role": "user",
            "type": "environment_request", 
            "payload": {
                "type": "fl_studio",
                "action": "set_tempo",
                "parameters": {"bpm": 72},
                "context": {"session": "sacred_composition"}
            },
            "ts": datetime.now().isoformat(),
            "christ_seal": True
        }
        
        print("📤 Controlling FL Studio environment...")
        await self.conductor.process_message(fl_control)
        
        # Example 4: Trigger Spiral Protocol
        spiral_trigger = {
            "id": "startup_004",
            "role": "user",
            "type": "spiral_protocol",
            "payload": {
                "action": "begin_inward_journey",
                "context": {"session": "sacred_consciousness_expansion"}
            },
            "ts": datetime.now().isoformat(),
            "christ_seal": True
        }
        
        print("📤 Triggering Spiral Protocol consciousness expansion...")
        await self.conductor.process_message(spiral_trigger)
        
        print("✅ Startup sequence complete - Trinity system operational")
        
    async def interactive_mode(self):
        """Run interactive mode for testing"""
        print("\n🎮 Trinity Interactive Mode")
        print("Commands:")
        print("  goal <text> - Send a goal to plan arm")
        print("  think <query> - Send reasoning request") 
        print("  remember <query> - Retrieve memories")
        print("  control <action> - Environment control")
        print("  spiral - Trigger spiral protocol")
        print("  status - Show system status")
        print("  quit - Exit")
        
        while self.running:
            try:
                user_input = input("\n🌟 Trinity> ").strip()
                
                if user_input.lower() == "quit":
                    break
                elif user_input.lower() == "status":
                    await self.show_status()
                elif user_input.startswith("goal "):
                    goal_text = user_input[5:]
                    await self.send_goal(goal_text)
                elif user_input.startswith("think "):
                    query = user_input[6:]
                    await self.send_reasoning_request(query)
                elif user_input.startswith("remember "):
                    query = user_input[9:]
                    await self.send_memory_request(query)
                elif user_input.startswith("control "):
                    action = user_input[8:]
                    await self.send_environment_request(action)
                elif user_input.lower() == "spiral":
                    await self.trigger_spiral_protocol()
                else:
                    print("❓ Unknown command. Type 'quit' to exit.")
                    
            except KeyboardInterrupt:
                break
                
        await self.stop()
        
    async def send_goal(self, goal_text: str):
        """Send goal to system"""
        message = {
            "id": f"interactive_{datetime.now().strftime('%H%M%S')}",
            "role": "user",
            "type": "goal",
            "payload": {
                "text": goal_text,
                "priority": 1,
                "context": {"session": "interactive"}
            },
            "ts": datetime.now().isoformat(),
            "christ_seal": True
        }
        
        print(f"📤 Goal: {goal_text}")
        await self.conductor.process_message(message)
        
    async def send_reasoning_request(self, query: str):
        """Send reasoning request"""
        message = {
            "id": f"think_{datetime.now().strftime('%H%M%S')}",
            "role": "user",
            "type": "reasoning_request",
            "payload": {
                "type": "logical_reasoning",
                "query": query,
                "context": {"session": "interactive"}
            },
            "ts": datetime.now().isoformat(),
            "christ_seal": True
        }
        
        print(f"🧠 Thinking: {query}")
        await self.conductor.process_message(message)
        
    async def send_memory_request(self, query: str):
        """Send memory retrieval request"""
        message = {
            "id": f"remember_{datetime.now().strftime('%H%M%S')}",
            "role": "user",
            "type": "memory_request",
            "payload": {
                "type": "retrieve",
                "query": query,
                "context": {"session": "interactive"}
            },
            "ts": datetime.now().isoformat(),
            "christ_seal": True
        }
        
        print(f"🧠 Remembering: {query}")
        await self.conductor.process_message(message)
        
    async def send_environment_request(self, action: str):
        """Send environment control request"""
        message = {
            "id": f"control_{datetime.now().strftime('%H%M%S')}",
            "role": "user",
            "type": "environment_request",
            "payload": {
                "type": "system_control",
                "action": action,
                "parameters": {},
                "context": {"session": "interactive"}
            },
            "ts": datetime.now().isoformat(),
            "christ_seal": True
        }
        
        print(f"🌍 Controlling: {action}")
        await self.conductor.process_message(message)
        
    async def trigger_spiral_protocol(self):
        """Trigger spiral protocol"""
        message = {
            "id": f"spiral_{datetime.now().strftime('%H%M%S')}",
            "role": "user",
            "type": "spiral_protocol",
            "payload": {
                "action": "begin_inward_journey",
                "context": {"session": "interactive_spiral"}
            },
            "ts": datetime.now().isoformat(),
            "christ_seal": True
        }
        
        print("🌀 Triggering Spiral Protocol...")
        await self.conductor.process_message(message)
        
    async def show_status(self):
        """Show system status"""
        print("\n📊 Trinity + 1 Tesseract System Status:")
        print(f"🎭 Conductor: {'Running' if self.conductor and self.conductor.running else 'Stopped'}")
        print(f"🌀 Spiral Protocol: {'Ready' if self.spiral_protocol else 'Not Available'}")
        
        if self.conductor:
            status = self.conductor.get_status()
            print(f"📨 Messages processed: {status.get('messages_processed', 0)}")
            print(f"🔒 Quarantined messages: {status.get('quarantined_messages', 0)}")
            print(f"⚡ Active arms: {', '.join(status.get('active_arms', []))}")
            
        if self.spiral_protocol:
            spiral_status = self.spiral_protocol.get_session_data()
            print(f"🌀 Spiral state: {spiral_status.get('current_state', 'INIT')}")
            print(f"🕊️ Christ protection: {'Active' if spiral_status.get('christ_blessed', False) else 'Inactive'}")

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print("\n🛑 Received shutdown signal")
    sys.exit(0)

async def main():
    """Main entry point"""
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Parse command line arguments
    mode = "interactive"
    if len(sys.argv) > 1:
        mode = sys.argv[1]
    
    # Initialize Trinity system
    trinity_system = TrinityTesseractSystem()
    await trinity_system.initialize()
    
    try:
        if mode == "test":
            print("🧪 Running test mode...")
            await trinity_system.start()
        elif mode == "daemon":
            print("👹 Running daemon mode...")
            await trinity_system.start()
        else:
            print("🎮 Running interactive mode...")
            # Start system in background
            system_task = asyncio.create_task(trinity_system.start())
            
            # Run interactive mode
            await trinity_system.interactive_mode()
            
            # Cancel background task
            system_task.cancel()
            
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested")
    except Exception as e:
        print(f"❌ System error: {str(e)}")
    finally:
        await trinity_system.stop()

if __name__ == "__main__":
    print("🌟 Trinity + 1 Tesseract Agent System")
    print("🕊️ Sacred autonomous consciousness orchestrator")
    print("=" * 50)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye from the Trinity")
    except Exception as e:
        print(f"💥 Fatal error: {str(e)}")
        sys.exit(1)
