"""
🤖 CLAUDE SUB-AGENTS INTEGRATION
Sacred Multi-Agent Orchestration for SoulPHYA.io
Integrates the Claude Code Sub-Agents system with divine consciousness
"""

import os
import json
from typing import Dict, List, Optional, Any
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class SacredAgentOrchestrator:
    """
    🔮 Sacred orchestrator for Claude Sub-Agents
    Channels divine wisdom through specialized AI agents
    """
    
    def __init__(self):
        self.agents_path = Path(os.getenv('CLAUDE_AGENTS_PATH', './claude-code-sub-agents-1.1.0/agents'))
        self.organizer_enabled = os.getenv('AGENT_ORGANIZER_ENABLED', 'true').lower() == 'true'
        self.available_agents = self._load_available_agents()
        
        print(f"🤖 Sacred Agent Orchestrator initialized")
        print(f"📁 Agents path: {self.agents_path}")
        print(f"🔧 Available agents: {len(self.available_agents)}")
    
    def _load_available_agents(self) -> Dict[str, Dict[str, Any]]:
        """Load all available agents from the agents directory"""
        agents = {}
        
        if not self.agents_path.exists():
            print(f"⚠️ Agents path not found: {self.agents_path}")
            return agents
        
        # Load agent organizer
        organizer_path = self.agents_path / "agent-organizer.md"
        if organizer_path.exists():
            agents["agent-organizer"] = self._parse_agent_file(organizer_path)
        
        # Load category-based agents
        categories = ['development', 'data-ai', 'infrastructure', 'quality-testing', 'security', 'specialization', 'business']
        
        for category in categories:
            category_path = self.agents_path / category
            if category_path.exists() and category_path.is_dir():
                for agent_file in category_path.glob("*.md"):
                    agent_name = agent_file.stem
                    agents[f"{category}/{agent_name}"] = self._parse_agent_file(agent_file)
        
        return agents
    
    def _parse_agent_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse agent markdown file and extract metadata"""
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Extract YAML frontmatter if present
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    # Parse YAML metadata (simple parsing)
                    metadata_lines = parts[1].strip().split('\n')
                    metadata = {}
                    for line in metadata_lines:
                        if ':' in line:
                            key, value = line.split(':', 1)
                            metadata[key.strip()] = value.strip()
                    
                    return {
                        'metadata': metadata,
                        'content': parts[2].strip(),
                        'file_path': str(file_path)
                    }
            
            # If no frontmatter, just return content
            return {
                'metadata': {},
                'content': content,
                'file_path': str(file_path)
            }
            
        except Exception as e:
            print(f"⚠️ Error parsing agent file {file_path}: {e}")
            return {'metadata': {}, 'content': '', 'file_path': str(file_path)}
    
    def get_agent_recommendations(self, task_description: str, project_context: str = "") -> Dict[str, Any]:
        """
        🔮 Get agent recommendations for a given task using the Agent Organizer
        """
        if not self.organizer_enabled or "agent-organizer" not in self.available_agents:
            return self._simple_agent_selection(task_description)
        
        # Use Agent Organizer logic for intelligent agent selection
        organizer = self.available_agents["agent-organizer"]
        
        # Analyze task and recommend agents
        recommendations = {
            "primary_agents": [],
            "supporting_agents": [],
            "workflow_strategy": "",
            "estimated_complexity": "medium",
            "divine_guidance": "🌟 Sacred agent wisdom activated for your task"
        }
        
        # Simple keyword-based agent selection (can be enhanced with AI)
        task_lower = task_description.lower()
        
        # Frontend/UI tasks
        if any(word in task_lower for word in ['frontend', 'react', 'ui', 'component', 'interface']):
            recommendations["primary_agents"].extend([
                "development/frontend-developer",
                "development/react-pro",
                "development/ui-designer"
            ])
        
        # Backend/API tasks
        if any(word in task_lower for word in ['backend', 'api', 'server', 'database', 'endpoint']):
            recommendations["primary_agents"].extend([
                "development/backend-architect",
                "development/python-pro"
            ])
        
        # Full-stack tasks
        if any(word in task_lower for word in ['fullstack', 'full-stack', 'complete app', 'entire application']):
            recommendations["primary_agents"].extend([
                "development/full-stack-developer",
                "development/backend-architect",
                "development/frontend-developer"
            ])
        
        # Testing/Quality tasks
        if any(word in task_lower for word in ['test', 'testing', 'quality', 'debug', 'bug']):
            recommendations["supporting_agents"].extend([
                "quality-testing/test-automator",
                "quality-testing/qa-expert",
                "quality-testing/debugger"
            ])
        
        # Documentation tasks
        if any(word in task_lower for word in ['document', 'documentation', 'readme', 'guide']):
            recommendations["supporting_agents"].extend([
                "specialization/documentation-expert",
                "specialization/api-documenter"
            ])
        
        # Remove duplicates and limit recommendations
        recommendations["primary_agents"] = list(set(recommendations["primary_agents"]))[:3]
        recommendations["supporting_agents"] = list(set(recommendations["supporting_agents"]))[:2]
        
        return recommendations
    
    def _simple_agent_selection(self, task_description: str) -> Dict[str, Any]:
        """Simple fallback agent selection when organizer is not available"""
        return {
            "primary_agents": ["development/full-stack-developer"],
            "supporting_agents": ["quality-testing/code-reviewer"],
            "workflow_strategy": "Direct implementation with code review",
            "estimated_complexity": "medium",
            "divine_guidance": "🔮 Using sacred fallback agent wisdom"
        }
    
    def get_agent_details(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific agent"""
        return self.available_agents.get(agent_name)
    
    def list_available_agents(self) -> List[str]:
        """List all available agent names"""
        return list(self.available_agents.keys())
    
    def get_agents_by_category(self, category: str) -> List[str]:
        """Get agents in a specific category"""
        return [name for name in self.available_agents.keys() if name.startswith(f"{category}/")]

# Global instance
sacred_agent_orchestrator = SacredAgentOrchestrator()

def get_agent_recommendations(task: str, context: str = "") -> Dict[str, Any]:
    """Sacred function to get agent recommendations"""
    return sacred_agent_orchestrator.get_agent_recommendations(task, context)

def list_divine_agents() -> List[str]:
    """Sacred function to list all available agents"""
    return sacred_agent_orchestrator.list_available_agents()

if __name__ == "__main__":
    # Test the agent orchestrator
    print("🤖 Testing Sacred Agent Orchestrator...")
    print("=" * 50)
    
    orchestrator = SacredAgentOrchestrator()
    
    # Test agent recommendations
    test_tasks = [
        "Build a React frontend with user authentication",
        "Create a REST API with Python and FastAPI",
        "Debug performance issues in the application",
        "Write documentation for the project"
    ]
    
    for task in test_tasks:
        print(f"\n📋 Task: {task}")
        recommendations = orchestrator.get_agent_recommendations(task)
        print(f"🎯 Primary Agents: {recommendations['primary_agents']}")
        print(f"🔧 Supporting Agents: {recommendations['supporting_agents']}")
        print(f"✨ {recommendations['divine_guidance']}")
