#!/usr/bin/env python3
"""
🧠 Memory & Retrieval Arm (South) - Trinity + 1 Tesseract - Simplified Version
Long-term memory, knowledge retrieval, learning, and context management
"""

import json
import asyncio
import sqlite3
import hashlib
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

class MemoryState(Enum):
    ACTIVE = "active"
    DORMANT = "dormant"
    ARCHIVED = "archived"
    FORGOTTEN = "forgotten"

@dataclass
class MemoryNode:
    """Individual memory node"""
    id: str
    content: Dict[str, Any]
    memory_type: str  # episodic, semantic, procedural
    importance: float
    created_at: str
    last_accessed: str
    access_count: int
    tags: List[str]
    connections: List[str]
    embedding: Optional[List[float]] = None
    state: MemoryState = MemoryState.ACTIVE

class MemoryRetrievalArm:
    """Memory & Retrieval Arm - Long-term memory and knowledge management"""
    
    def __init__(self):
        self.memory_db_path = Path("memory/sophia_memory.db")
        self.memory_db_path.parent.mkdir(exist_ok=True)
        
        # In-memory caches
        self.episodic_memory = []
        self.semantic_memory = {}
        self.procedural_memory = {}
        
        # Initialize database
        self.init_database()
        
    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().isoformat()
        symbol = {"INFO": "🧠", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}.get(level, "🧠")
        print(f"{symbol} [{timestamp}] [MEMORY-ARM] {message}")

    def init_database(self):
        """Initialize SQLite database"""
        try:
            conn = sqlite3.connect(self.memory_db_path)
            conn.execute('''
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    content TEXT,
                    memory_type TEXT,
                    importance REAL,
                    created_at TEXT,
                    last_accessed TEXT,
                    access_count INTEGER,
                    tags TEXT,
                    connections TEXT,
                    embedding TEXT,
                    state TEXT DEFAULT 'active'
                )
            ''')
            conn.commit()
            conn.close()
        except Exception as e:
            self.log(f"Database initialization error: {e}", "ERROR")

    async def handle_memory_message(self, request_msg: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming memory/retrieval request - Main entry point"""
        self.log(f"Received memory request: {request_msg.get('type', 'unknown')}", "INFO")
        
        payload = request_msg.get("payload", {})
        request_type = payload.get("type", "retrieve")
        
        try:
            if request_type == "store":
                data = payload.get("data", {})
                context = payload.get("context", {})
                result = await self.store_memory(data, context)
            elif request_type == "retrieve":
                query = payload.get("query", "")
                context = payload.get("context", {})
                result = await self.retrieve_memory(query, context)
            elif request_type == "search":
                query = payload.get("query", "")
                context = payload.get("context", {})
                result = await self.search_memory(query, context)
            else:
                result = {"success": False, "error": f"Unknown request type: {request_type}"}
                
            return {
                "id": f"memory_response_{datetime.now().isoformat()}",
                "role": "memory_arm",
                "type": "memory_response",
                "payload": result,
                "ts": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.log(f"Error handling memory request: {e}", "ERROR")
            return {
                "id": f"memory_error_{datetime.now().isoformat()}",
                "role": "memory_arm", 
                "type": "memory_response",
                "payload": {"success": False, "error": str(e)},
                "ts": datetime.now().isoformat()
            }

    async def store_memory(self, data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Store new memory"""
        if context is None:
            context = {}
            
        self.log(f"Storing memory: {data.get('type', 'unknown memory')}", "INFO")
        
        # Create memory node
        memory_id = hashlib.md5(str(data).encode()).hexdigest()
        memory_node = MemoryNode(
            id=memory_id,
            content=data,
            memory_type=data.get("type", "episodic"),
            importance=data.get("importance", 0.5),
            created_at=datetime.now().isoformat(),
            last_accessed=datetime.now().isoformat(),
            access_count=1,
            tags=data.get("tags", []),
            connections=[]
        )
        
        # Store based on memory type
        if memory_node.memory_type == "episodic":
            await self.store_episodic_memory(memory_node, context)
        elif memory_node.memory_type == "semantic":
            await self.store_semantic_memory(memory_node, context)
        elif memory_node.memory_type == "procedural":
            await self.store_procedural_memory(memory_node, context)
        
        # Persist to database
        self.persist_memory(memory_node)
        
        self.log("Memory stored successfully", "SUCCESS")
        return {
            "success": True,
            "memory_id": memory_id,
            "type": memory_node.memory_type,
            "importance": memory_node.importance
        }

    async def retrieve_memory(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Retrieve memory based on query"""
        if context is None:
            context = {}
            
        self.log(f"Retrieving memory for: {query[:50]}...", "INFO")
        
        # Simple keyword-based retrieval for now
        results = []
        
        # Search episodic memory
        for memory in self.episodic_memory[-10:]:  # Recent memories
            if any(word.lower() in str(memory.content).lower() for word in query.split()):
                results.append({
                    "id": memory.id,
                    "content": memory.content,
                    "type": memory.memory_type,
                    "relevance": 0.8,
                    "created_at": memory.created_at
                })
        
        # Search semantic memory
        for concept, memories in self.semantic_memory.items():
            if query.lower() in concept.lower():
                for memory in memories[-3:]:  # Recent semantic memories
                    results.append({
                        "id": memory.id,
                        "content": memory.content,
                        "type": memory.memory_type,
                        "relevance": 0.7,
                        "concept": concept
                    })
        
        self.log(f"Retrieved {len(results)} memories", "SUCCESS")
        return {
            "success": True,
            "query": query,
            "results": results,
            "count": len(results)
        }

    async def search_memory(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Search memory with more detailed criteria"""
        if context is None:
            context = {}
            
        self.log(f"Searching memory: {query}", "INFO")
        
        # For now, delegate to retrieve_memory
        return await self.retrieve_memory(query, context)

    async def store_episodic_memory(self, memory: MemoryNode, context: Dict):
        """Store episodic (event-based) memory"""
        self.episodic_memory.append(memory)
        
        # Keep only recent episodic memories in cache
        if len(self.episodic_memory) > 100:
            self.episodic_memory = self.episodic_memory[-100:]

    async def store_semantic_memory(self, memory: MemoryNode, context: Dict):
        """Store semantic (concept-based) memory"""
        concept = self.extract_concept(memory.content)
        
        if concept not in self.semantic_memory:
            self.semantic_memory[concept] = []
        self.semantic_memory[concept].append(memory)

    async def store_procedural_memory(self, memory: MemoryNode, context: Dict):
        """Store procedural (skill-based) memory"""
        skill = memory.content.get("skill", "general")
        
        if skill not in self.procedural_memory:
            self.procedural_memory[skill] = []
        self.procedural_memory[skill].append(memory)

    def extract_concept(self, content: Dict[str, Any]) -> str:
        """Extract concept from content for semantic memory"""
        if "concept" in content:
            return content["concept"]
        elif "subject" in content:
            return content["subject"]
        elif "topic" in content:
            return content["topic"]
        else:
            # Simple keyword extraction
            text = str(content)
            words = text.lower().split()
            return words[0] if words else "general"

    def persist_memory(self, memory: MemoryNode):
        """Persist memory to database"""
        try:
            conn = sqlite3.connect(self.memory_db_path)
            conn.execute('''
                INSERT OR REPLACE INTO memories 
                (id, content, memory_type, importance, created_at, last_accessed, 
                 access_count, tags, connections, embedding, state)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                memory.id,
                json.dumps(memory.content),
                memory.memory_type,
                memory.importance,
                memory.created_at,
                memory.last_accessed,
                memory.access_count,
                json.dumps(memory.tags),
                json.dumps(memory.connections),
                json.dumps(memory.embedding) if memory.embedding else None,
                memory.state.value
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            self.log(f"Database persistence error: {e}", "ERROR")

# Global instance
memory_arm = MemoryRetrievalArm()

async def handle_memory_message(message: Dict[str, Any]) -> Dict[str, Any]:
    """Handle memory message - Entry point for conductor"""
    return await memory_arm.handle_memory_message(message)

if __name__ == "__main__":
    # Test the memory arm
    async def test_memory_arm():
        test_msg = {
            "id": "test_memory",
            "role": "test",
            "type": "memory_request",
            "payload": {
                "type": "store",
                "data": {"content": "test memory content", "type": "episodic"},
                "context": {}
            },
            "ts": datetime.now().isoformat()
        }
        
        result = await handle_memory_message(test_msg)
        print("Test result:", json.dumps(result, indent=2))
    
    asyncio.run(test_memory_arm())
