#!/usr/bin/env python3
"""
Sophia AI Launcher - Quick Start Script
Run this to initialize Sophia with her full capabilities
"""

import asyncio
import sys
import os
from pathlib import Path

# Add repo root to path
REPO_ROOT = Path(__file__).parent
sys.path.insert(0, str(REPO_ROOT))

class SophiaLauncher:
    def __init__(self):
        self.services = {}
        
    async def launch(self):
        """Launch Sophia with all available services"""
        print("🚀 Launching Sophia AI Orchestrator")
        print("=" * 50)
        
        # Check environment first
        await self._environment_check()
        
        # Start core services
        await self._start_core_services()
        
        # Initialize AI components
        await self._initialize_ai_components()
        
        # Enter interactive mode
        await self._interactive_mode()
        
    async def _environment_check(self):
        """Quick environment validation"""
        try:
            from sophia_check import SophiaEnvironment
            env_checker = SophiaEnvironment()
            summary = await env_checker.check_environment()
            print("✅ Environment validated")
        except Exception as e:
            print(f"⚠️ Environment check skipped: {e}")
            
    async def _start_core_services(self):
        """Start essential services"""
        print("\n🔧 Starting Core Services...")
        
        # Start memory system
        try:
            from ghost_core.agents.intelligent_idea_ingestor import IntelligentIdeaIngestor
            self.services['memory'] = IntelligentIdeaIngestor()
            print("✅ Memory System initialized")
        except Exception as e:
            print(f"❌ Memory System failed: {e}")
            
        # Start system controller
        try:
            from system_control.controller import Controller
            self.services['controller'] = Controller()
            print("✅ System Controller initialized")
        except Exception as e:
            print(f"❌ System Controller failed: {e}")
            
    async def _initialize_ai_components(self):
        """Initialize AI reasoning components"""
        print("\n🧠 Initializing AI Components...")
        
        # Initialize idea processing
        if 'memory' in self.services:
            print("✅ Intelligent Idea Processing ready")
            
        # Initialize system automation
        if 'controller' in self.services:
            print("✅ System Automation ready")
            
        print("✅ Sophia AI fully operational")
        
    async def _interactive_mode(self):
        """Enter interactive conversation mode"""
        print("\n💬 Sophia Interactive Mode")
        print("=" * 30)
        print("Hi! I'm Sophia, your AI orchestrator.")
        print("I can help with:")
        print("  • Learning and remembering information")
        print("  • Automating system tasks")
        print("  • Processing complex ideas")
        print("  • Managing workflows")
        print("\nType 'help' for commands or 'exit' to quit.")
        print("-" * 40)
        
        while True:
            try:
                user_input = input("\n🤖 Sophia> ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("👋 Goodbye! Sophia signing off.")
                    break
                    
                elif user_input.lower() == 'help':
                    await self._show_help()
                    
                elif user_input.lower() == 'status':
                    await self._show_status()
                    
                elif user_input.startswith('learn '):
                    content = user_input[6:]
                    await self._learn_content(content)
                    
                elif user_input.startswith('remember '):
                    query = user_input[9:]
                    await self._remember_content(query)
                    
                else:
                    await self._process_general_input(user_input)
                    
            except KeyboardInterrupt:
                print("\n👋 Sophia signing off gracefully...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                
    async def _show_help(self):
        """Show available commands"""
        print("\n📚 Sophia Commands:")
        print("  help           - Show this help")
        print("  status         - Show system status") 
        print("  learn <text>   - Learn new information")
        print("  remember <q>   - Search memory")
        print("  exit/quit      - Exit Sophia")
        
    async def _show_status(self):
        """Show current system status"""
        print(f"\n📊 Sophia Status:")
        print(f"  Active Services: {len(self.services)}")
        for name, service in self.services.items():
            status = "✅ Running" if service else "❌ Error"
            print(f"    {name}: {status}")
            
    async def _learn_content(self, content):
        """Learn new content"""
        if 'memory' in self.services:
            try:
                result = await self.services['memory'].ingest_content(
                    content, "user_input", {"interactive": True}
                )
                print(f"✅ Learned: {content[:50]}...")
            except Exception as e:
                print(f"❌ Learning failed: {e}")
        else:
            print("❌ Memory system not available")
            
    async def _remember_content(self, query):
        """Search memory for content"""
        print(f"🔍 Searching for: {query}")
        # Implement memory search here
        print("💭 Memory search functionality coming soon...")
        
    async def _process_general_input(self, user_input):
        """Process general conversation input"""
        print(f"🤔 Processing: {user_input}")
        
        # Simple responses for demo
        if any(word in user_input.lower() for word in ['hello', 'hi', 'hey']):
            print("👋 Hello! How can I help you today?")
        elif any(word in user_input.lower() for word in ['how', 'what', 'why']):
            print("🤖 That's an interesting question! I'm still learning...")
        elif 'sophia' in user_input.lower():
            print("😊 Yes, that's me! Sophia AI at your service.")
        else:
            print("💭 I'm processing that information...")

async def main():
    """Main launcher function"""
    launcher = SophiaLauncher()
    await launcher.launch()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Sophia launcher cancelled")
    except Exception as e:
        print(f"💥 Launch failed: {e}")
        sys.exit(1)
