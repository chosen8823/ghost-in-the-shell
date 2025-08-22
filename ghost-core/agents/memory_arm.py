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
        # Ensure parent directories are created (handle nested paths)
        self.memory_db_path.parent.mkdir(parents=True, exist_ok=True)

        # Load memory configuration if present
        self.config = {
            "default_importance": 0.5,
            "truncate_content_chars": 10000,
            "enable_db_fallback": True,
            "topic_tag_map": {
                "constructor theory": ["constructor-theory", "foundations"],
                "social physics": ["social-physics", "networks"],
                "belief": ["beliefs", "cultural"],
                "econom": ["economics", "policy"]
            }
        }
        # Simple geometry taxonomy map for multi-level categorization (4D-inspired labels)
        self.config.setdefault("geometry_map", {
            "tesseract": ["4d", "hypercube", "structured"],
            "hypersphere": ["continuous", "diffuse", "holistic"],
            "simplex4": ["hierarchy", "simplex", "causal-chain"],
            "hypercube-layered": ["modular", "layered", "compositional"]
        })
        try:
            cfg_path = Path(__file__).resolve().parent.parent / "config" / "memory_settings.json"
            if cfg_path.exists():
                with open(cfg_path, "r", encoding="utf-8") as f:
                    user_cfg = json.load(f)
                    self.config.update(user_cfg)
        except Exception as e:
            self.log(f"Failed to load memory config: {e}", "WARNING")

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
        # Use a stable JSON representation for hashing to avoid collisions from
        # differing dict ordering and to make ids reproducible.
        memory_id = hashlib.md5(json.dumps(data, sort_keys=True, default=str).encode()).hexdigest()
        # Enforce content truncation from configuration
        if isinstance(data.get("content"), str) and self.config.get("truncate_content_chars"):
            data["content"] = data.get("content")[: self.config.get("truncate_content_chars")]

        # map simple topic keywords to tags from config
        inferred_tags = list(data.get("tags", []))
        content_lower = str(data.get("content", "")).lower()
        for keyword, tags in self.config.get("topic_tag_map", {}).items():
            if keyword in content_lower or keyword in str(data.get("title", "")).lower():
                for t in tags:
                    if t not in inferred_tags:
                        inferred_tags.append(t)

        # Infer a geometry classification for high-level routing/categorization
        geometry = self.infer_geometry(content_lower, data)
        if geometry:
            data["geometry"] = geometry
            if geometry not in inferred_tags:
                inferred_tags.append(geometry)

        memory_node = MemoryNode(
            id=memory_id,
            content=data,
            memory_type=data.get("type", "episodic"),
            importance=data.get("importance", self.config.get("default_importance", 0.5)),
            created_at=datetime.now().isoformat(),
            last_accessed=datetime.now().isoformat(),
            access_count=1,
            tags=inferred_tags,
            connections=[]
        )
        

        # Store based on memory type
        if memory_node.memory_type == "episodic":
            await self.store_episodic_memory(memory_node, context)
        elif memory_node.memory_type == "semantic":
            await self.store_semantic_memory(memory_node, context)
        elif memory_node.memory_type == "procedural":
            await self.store_procedural_memory(memory_node, context)

        # Persist to database (async) and fail the store if persistence fails
        persisted = await self.persist_memory(memory_node)
        if not persisted:
            self.log("Memory persistence failed", "ERROR")
            return {"success": False, "error": "database_persistence_failed"}

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
        # If no results in cache, fallback to DB simple search
        if not results:
            db_results = await self._db_search(query, limit=10)
            for r in db_results:
                results.append({
                    "id": r.get("id"),
                    "content": r.get("content"),
                    "type": r.get("type"),
                    "relevance": 0.6,
                    "created_at": r.get("created_at")
                })

        self.log(f"Retrieved {len(results)} memories (after DB fallback)", "SUCCESS")
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

    async def persist_memory(self, memory: MemoryNode) -> bool:
        """Persist memory to database in a thread to avoid blocking the event loop.

        Performs a small upsert that preserves original created_at and increments
        access_count when a duplicate id is detected.
        """
        def _write():
            try:
                with sqlite3.connect(self.memory_db_path, timeout=5) as conn:
                    cur = conn.cursor()
                    # Check if memory exists to preserve created_at and accumulate access_count
                    cur.execute('SELECT created_at, access_count FROM memories WHERE id=?', (memory.id,))
                    row = cur.fetchone()
                    if row:
                        created_at, access_count = row
                        # preserve original created_at and increment access count
                        memory.created_at = created_at
                        memory.access_count = (access_count or 0) + 1

                    cur.execute('''
                        INSERT OR REPLACE INTO memories 
                        (id, content, memory_type, importance, created_at, last_accessed, 
                         access_count, tags, connections, embedding, state)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        memory.id,
                        json.dumps(memory.content, default=str),
                        memory.memory_type,
                        memory.importance,
                        memory.created_at,
                        memory.last_accessed,
                        memory.access_count,
                        json.dumps(memory.tags),
                        json.dumps(memory.connections),
                        json.dumps(memory.embedding) if memory.embedding is not None else None,
                        memory.state.value
                    ))
                    conn.commit()
                return True
            except Exception as e:
                # Can't call self.log from thread, so return error message
                return str(e)

        result = await asyncio.to_thread(_write)
        if result is True:
            return True
        else:
            self.log(f"Database persistence error: {result}", "ERROR")
            return False

    async def _db_search(self, raw_query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Fallback DB search using simple LIKE on stored JSON content and tags."""
        def _query():
            try:
                q = f"%{raw_query}%"
                with sqlite3.connect(self.memory_db_path, timeout=5) as conn:
                    cur = conn.cursor()
                    cur.execute('''
                        SELECT id, content, memory_type, importance, created_at, last_accessed, access_count, tags
                        FROM memories
                        WHERE content LIKE ? OR tags LIKE ?
                        ORDER BY created_at DESC
                        LIMIT ?
                    ''', (q, q, limit))
                    rows = cur.fetchall()
                    results = []
                    for r in rows:
                        cid, content_json, mtype, importance, created_at, last_accessed, access_count, tags_json = r
                        try:
                            content = json.loads(content_json)
                        except Exception:
                            content = content_json
                        try:
                            tags = json.loads(tags_json) if tags_json else []
                        except Exception:
                            tags = []
                        results.append({
                            "id": cid,
                            "content": content,
                            "type": mtype,
                            "importance": importance,
                            "created_at": created_at,
                            "last_accessed": last_accessed,
                            "access_count": access_count,
                            "tags": tags
                        })
                    return results
            except Exception as e:
                return []

        return await asyncio.to_thread(_query)

    def infer_geometry(self, content_lower: str, data: Dict[str, Any]) -> Optional[str]:
        """Infer a simple geometry label from content or title using keyword heuristics.

        This is a lightweight mapping to support multi-level categorization used by
        higher-level routing and UI. It's configurable in `memory_settings.json`.
        """
        # check for explicit topic/title signals first
        title = str(data.get("title", "")).lower()
        # heuristics: presence of keywords maps to geometry
        keyword_to_geom = {
            "constructor": "tesseract",
            "theory": "simplex4",
            "social": "hypersphere",
            "network": "hypercube-layered",
            "econom": "simplex4",
        }

        for k, g in keyword_to_geom.items():
            if k in content_lower or k in title:
                return g

        # fallback: choose based on length/structure
        try:
            if len(content_lower) > 4000:
                return "hypersphere"
        except Exception:
            pass
        if "chapter" in content_lower or "section" in content_lower:
            return "tesseract"
        return None

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
