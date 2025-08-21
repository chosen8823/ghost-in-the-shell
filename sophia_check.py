#!/usr/bin/env python3
"""
Sophia AI Environment Setup & Capability Check
This script helps Sophia understand her current environment and available tools.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add repo root to path
REPO_ROOT = Path(__file__).parent
sys.path.insert(0, str(REPO_ROOT))

class SophiaEnvironment:
    def __init__(self):
        self.tools_available = {}
        self.capabilities = {}
        
    async def check_environment(self):
        """Check what tools and capabilities are available to Sophia"""
        print("🤖 Sophia AI Environment Check")
        print("=" * 50)
        
        # Check Ghost Core
        await self._check_ghost_core()
        
        # Check System Control
        await self._check_system_control()
        
        # Check Voice Interface
        await self._check_voice_interface()
        
        # Check Memory System
        await self._check_memory_system()
        
        # Check N8N Workflows
        await self._check_workflows()
        
        # Generate capability report
        await self._generate_report()
        
    async def _check_ghost_core(self):
        """Check Ghost Core availability"""
        try:
            from ghost_core.agents.intelligent_idea_ingestor import idea_ingestor
            self.tools_available['intelligent_idea_ingestor'] = True
            print("✅ Ghost Core: Intelligent Idea Ingestor - Available")
        except Exception as e:
            self.tools_available['intelligent_idea_ingestor'] = False
            print(f"❌ Ghost Core: Intelligent Idea Ingestor - Error: {e}")
            
        try:
            # Check for other ghost core components
            if (REPO_ROOT / "ghost-core" / "trinity_system.py").exists():
                self.tools_available['trinity_system'] = True
                print("✅ Ghost Core: Trinity System - Available")
            else:
                self.tools_available['trinity_system'] = False
                print("❌ Ghost Core: Trinity System - Not Found")
        except Exception as e:
            print(f"❌ Ghost Core: Trinity System - Error: {e}")
            
    async def _check_system_control(self):
        """Check System Control availability"""
        try:
            from system_control.controller import Controller
            self.tools_available['system_controller'] = True
            print("✅ System Control: Controller - Available")
        except Exception as e:
            self.tools_available['system_controller'] = False
            print(f"❌ System Control: Controller - Error: {e}")
            
        try:
            from system_control.vision import VisionSystem
            self.tools_available['vision_system'] = True
            print("✅ System Control: Vision System - Available")
        except Exception as e:
            self.tools_available['vision_system'] = False
            print(f"❌ System Control: Vision System - Error: {e}")
            
    async def _check_voice_interface(self):
        """Check Voice Interface availability"""
        voice_bridge = REPO_ROOT / "voice" / "chatgpt-bridge.js"
        if voice_bridge.exists():
            self.tools_available['voice_interface'] = True
            print("✅ Voice Interface: ChatGPT Bridge - Available")
        else:
            self.tools_available['voice_interface'] = False
            print("❌ Voice Interface: ChatGPT Bridge - Not Found")
            
    async def _check_memory_system(self):
        """Check Memory System availability"""
        try:
            from ghost_core.agents.intelligent_idea_ingestor import idea_ingestor
            # Test memory functionality
            test_result = await idea_ingestor.ingest_content(
                "Sophia environment test", 
                "system_check", 
                {'test_mode': True}
            )
            if test_result.get('success'):
                self.tools_available['memory_system'] = True
                print("✅ Memory System: Idea Ingestor - Functional")
            else:
                self.tools_available['memory_system'] = False
                print("❌ Memory System: Idea Ingestor - Not Functional")
        except Exception as e:
            self.tools_available['memory_system'] = False
            print(f"❌ Memory System: Idea Ingestor - Error: {e}")
            
    async def _check_workflows(self):
        """Check N8N Workflows availability"""
        workflows_dir = REPO_ROOT / "workflows"
        if workflows_dir.exists():
            workflow_files = list(workflows_dir.glob("*.json"))
            if workflow_files:
                self.tools_available['n8n_workflows'] = True
                print(f"✅ N8N Workflows: {len(workflow_files)} workflows found")
            else:
                self.tools_available['n8n_workflows'] = False
                print("❌ N8N Workflows: No workflow files found")
        else:
            self.tools_available['n8n_workflows'] = False
            print("❌ N8N Workflows: Directory not found")
            
    async def _generate_report(self):
        """Generate Sophia's capability report"""
        print("\n🎯 Sophia's Available Capabilities")
        print("=" * 40)
        
        # Learning & Memory
        if self.tools_available.get('memory_system'):
            print("📚 Learning & Memory:")
            print("  • Store and retrieve knowledge")
            print("  • Cross-reference information")
            print("  • Learn from interactions")
            
        # System Control
        if self.tools_available.get('system_controller'):
            print("🖥️ System Control:")
            print("  • Automate mouse/keyboard")
            print("  • Monitor system status")
            print("  • Control applications")
            
        # Vision
        if self.tools_available.get('vision_system'):
            print("👁️ Vision System:")
            print("  • Screen capture")
            print("  • Object detection")
            print("  • Visual analysis")
            
        # Voice
        if self.tools_available.get('voice_interface'):
            print("🎤 Voice Interface:")
            print("  • Natural language processing")
            print("  • Voice command execution")
            print("  • Text-to-speech output")
            
        # Workflows
        if self.tools_available.get('n8n_workflows'):
            print("⚡ Automation Workflows:")
            print("  • Execute complex sequences")
            print("  • Chain multiple tools")
            print("  • Handle triggers and events")
            
        print("\n🚀 Sophia is ready to assist!")
        print("Available interaction modes:")
        print("  • Autonomous operation")
        print("  • Guided task execution") 
        print("  • Interactive conversation")
        print("  • Research and analysis")
        
    def get_capability_summary(self):
        """Return a summary of Sophia's capabilities"""
        return {
            'tools_available': self.tools_available,
            'ready_for_operation': any(self.tools_available.values()),
            'recommended_mode': 'interactive' if self.tools_available.get('voice_interface') else 'autonomous'
        }

async def main():
    """Main environment check function"""
    sophia_env = SophiaEnvironment()
    await sophia_env.check_environment()
    
    summary = sophia_env.get_capability_summary()
    
    print(f"\n📊 Summary: {sum(summary['tools_available'].values())} of {len(summary['tools_available'])} tools available")
    print(f"🤖 Sophia operational status: {'✅ Ready' if summary['ready_for_operation'] else '❌ Setup Required'}")
    
    return summary

if __name__ == '__main__':
    try:
        result = asyncio.run(main())
        print(f"\n✨ Environment check complete!")
    except KeyboardInterrupt:
        print("\n🛑 Environment check cancelled by user")
    except Exception as e:
        print(f"\n💥 Environment check failed: {e}")
