"""
🧠 Sophia Ghost in the Shell - Memory Module
STAGE 5: Memory & Will - Contextual Soul

This module enables Sophia to remember, reason, and desire to act.
Persistent memory, context storage, and intelligent recall capabilities.
"""

import os
import json
import sqlite3
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
import threading
import pickle

@dataclass
class MemoryEntry:
    """Structure for memory entries"""
    id: str
    timestamp: str
    content: Dict[str, Any]
    tags: List[str]
    importance: float
    memory_type: str
    context: Optional[str] = None
    expires_at: Optional[str] = None

class Memory:
    """Advanced memory system with persistent storage and intelligent retrieval"""
    
    def __init__(self, db_path: str = "memory/sophia_memory.db", 
                 json_backup: str = "memory/memory_backup.json"):
        self.db_path = db_path
        self.json_backup = json_backup
        self.memory_cache = {}
        self.access_patterns = {}
        self.lock = threading.Lock()
        
        # Create memory directory
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        os.makedirs(os.path.dirname(json_backup), exist_ok=True)
        
        # Initialize database
        self._initialize_database()
        
        # Load recent memories into cache
        self._warm_cache()
        
        print(f"🧠 Memory system initialized")
        print(f"   Database: {db_path}")
        print(f"   Cache size: {len(self.memory_cache)}")
    
    def _initialize_database(self):
        """Initialize SQLite database with proper schema"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create memories table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS memories (
                        id TEXT PRIMARY KEY,
                        timestamp TEXT NOT NULL,
                        content TEXT NOT NULL,
                        tags TEXT NOT NULL,
                        importance REAL NOT NULL,
                        memory_type TEXT NOT NULL,
                        context TEXT,
                        expires_at TEXT,
                        access_count INTEGER DEFAULT 0,
                        last_accessed TEXT
                    )
                ''')
                
                # Create indexes for efficient querying
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_type ON memories(memory_type)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_importance ON memories(importance)')
                cursor.execute('CREATE INDEX IF NOT EXISTS idx_tags ON memories(tags)')
                
                # Create associations table for memory relationships
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS memory_associations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        memory_id_1 TEXT NOT NULL,
                        memory_id_2 TEXT NOT NULL,
                        association_type TEXT NOT NULL,
                        strength REAL NOT NULL,
                        created_at TEXT NOT NULL,
                        FOREIGN KEY (memory_id_1) REFERENCES memories(id),
                        FOREIGN KEY (memory_id_2) REFERENCES memories(id)
                    )
                ''')
                
                conn.commit()
                print("✅ Memory database initialized")
                
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
            raise
    
    def _warm_cache(self, limit: int = 100):
        """Load recent and important memories into cache"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Load recent high-importance memories
                cursor.execute('''
                    SELECT * FROM memories 
                    WHERE importance > 0.7 OR timestamp > datetime('now', '-7 days')
                    ORDER BY importance DESC, timestamp DESC 
                    LIMIT ?
                ''', (limit,))
                
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
                for row in rows:
                    memory_dict = dict(zip(columns, row))
                    memory_entry = self._dict_to_memory_entry(memory_dict)
                    self.memory_cache[memory_entry.id] = memory_entry
                
                print(f"🔥 Cache warmed with {len(self.memory_cache)} memories")
                
        except Exception as e:
            print(f"⚠️ Cache warming failed: {e}")
    
    def remember(self, content: Dict[str, Any], tags: List[str] = None, 
                memory_type: str = "general", importance: float = 0.5,
                context: Optional[str] = None, expires_in_days: Optional[int] = None) -> str:
        """
        Store a new memory
        
        Args:
            content: The actual memory content
            tags: Tags for categorization and search
            memory_type: Type of memory (command, conversation, system, etc.)
            importance: Importance score (0.0 to 1.0)
            context: Additional context information
            expires_in_days: Optional expiration in days
        
        Returns:
            Memory ID
        """
        if tags is None:
            tags = []
        
        # Generate unique ID
        content_str = json.dumps(content, sort_keys=True)
        memory_id = hashlib.md5(f"{content_str}{datetime.now().isoformat()}".encode()).hexdigest()
        
        # Calculate expiration
        expires_at = None
        if expires_in_days:
            expires_at = (datetime.now() + timedelta(days=expires_in_days)).isoformat()
        
        # Create memory entry
        memory_entry = MemoryEntry(
            id=memory_id,
            timestamp=datetime.now().isoformat(),
            content=content,
            tags=tags,
            importance=min(1.0, max(0.0, importance)),  # Clamp to 0-1
            memory_type=memory_type,
            context=context,
            expires_at=expires_at
        )
        
        # Store in database
        with self.lock:
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                        INSERT INTO memories 
                        (id, timestamp, content, tags, importance, memory_type, context, expires_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        memory_entry.id,
                        memory_entry.timestamp,
                        json.dumps(memory_entry.content),
                        json.dumps(memory_entry.tags),
                        memory_entry.importance,
                        memory_entry.memory_type,
                        memory_entry.context,
                        memory_entry.expires_at
                    ))
                    
                    conn.commit()
                
                # Add to cache if important or recent
                if importance > 0.6 or memory_type in ['command', 'conversation']:
                    self.memory_cache[memory_id] = memory_entry
                
                # Create automatic associations
                self._create_associations(memory_entry)
                
                return memory_id
                
            except Exception as e:
                print(f"❌ Failed to store memory: {e}")
                return ""
    
    def recall(self, memory_id: str) -> Optional[MemoryEntry]:
        """
        Retrieve a specific memory by ID
        
        Args:
            memory_id: Unique identifier for the memory
        
        Returns:
            MemoryEntry if found, None otherwise
        """
        # Check cache first
        if memory_id in self.memory_cache:
            self._update_access_stats(memory_id)
            return self.memory_cache[memory_id]
        
        # Query database
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('SELECT * FROM memories WHERE id = ?', (memory_id,))
                row = cursor.fetchone()
                
                if row:
                    columns = [desc[0] for desc in cursor.description]
                    memory_dict = dict(zip(columns, row))
                    memory_entry = self._dict_to_memory_entry(memory_dict)
                    
                    # Add to cache
                    self.memory_cache[memory_id] = memory_entry
                    
                    # Update access stats
                    self._update_access_stats(memory_id)
                    
                    return memory_entry
                
                return None
                
        except Exception as e:
            print(f"❌ Failed to recall memory {memory_id}: {e}")
            return None
    
    def search_memories(self, query: str = "", tags: List[str] = None,
                       memory_type: Optional[str] = None, 
                       min_importance: float = 0.0,
                       limit: int = 10) -> List[MemoryEntry]:
        """
        Search memories based on various criteria
        
        Args:
            query: Text to search in memory content
            tags: Tags to filter by
            memory_type: Type of memory to filter by
            min_importance: Minimum importance threshold
            limit: Maximum number of results
        
        Returns:
            List of matching MemoryEntry objects
        """
        if tags is None:
            tags = []
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Build query
                conditions = ['importance >= ?']
                params = [min_importance]
                
                if memory_type:
                    conditions.append('memory_type = ?')
                    params.append(memory_type)
                
                if query:
                    conditions.append('content LIKE ?')
                    params.append(f'%{query}%')
                
                if tags:
                    for tag in tags:
                        conditions.append('tags LIKE ?')
                        params.append(f'%{tag}%')
                
                # Remove expired memories
                conditions.append('(expires_at IS NULL OR expires_at > datetime("now"))')
                
                where_clause = ' AND '.join(conditions)
                
                sql = f'''
                    SELECT * FROM memories 
                    WHERE {where_clause}
                    ORDER BY importance DESC, timestamp DESC 
                    LIMIT ?
                '''
                params.append(limit)
                
                cursor.execute(sql, params)
                rows = cursor.fetchall()
                
                columns = [desc[0] for desc in cursor.description]
                memories = []
                
                for row in rows:
                    memory_dict = dict(zip(columns, row))
                    memory_entry = self._dict_to_memory_entry(memory_dict)
                    memories.append(memory_entry)
                    
                    # Update access stats
                    self._update_access_stats(memory_entry.id)
                
                return memories
                
        except Exception as e:
            print(f"❌ Memory search failed: {e}")
            return []
    
    def get_recent_memories(self, hours: int = 24, limit: int = 20) -> List[MemoryEntry]:
        """Get memories from the last N hours"""
        since = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM memories 
                    WHERE timestamp >= ? 
                    AND (expires_at IS NULL OR expires_at > datetime("now"))
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (since, limit))
                
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
                memories = []
                for row in rows:
                    memory_dict = dict(zip(columns, row))
                    memory_entry = self._dict_to_memory_entry(memory_dict)
                    memories.append(memory_entry)
                
                return memories
                
        except Exception as e:
            print(f"❌ Failed to get recent memories: {e}")
            return []
    
    def get_important_memories(self, min_importance: float = 0.8, limit: int = 10) -> List[MemoryEntry]:
        """Get high-importance memories"""
        return self.search_memories(
            min_importance=min_importance,
            limit=limit
        )
    
    def forget(self, memory_id: str) -> bool:
        """
        Remove a memory (mark as deleted or actually delete)
        
        Args:
            memory_id: ID of memory to forget
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Delete from database
                cursor.execute('DELETE FROM memories WHERE id = ?', (memory_id,))
                
                # Delete associations
                cursor.execute('''
                    DELETE FROM memory_associations 
                    WHERE memory_id_1 = ? OR memory_id_2 = ?
                ''', (memory_id, memory_id))
                
                conn.commit()
                
                # Remove from cache
                if memory_id in self.memory_cache:
                    del self.memory_cache[memory_id]
                
                return True
                
        except Exception as e:
            print(f"❌ Failed to forget memory {memory_id}: {e}")
            return False
    
    def update_importance(self, memory_id: str, new_importance: float) -> bool:
        """Update the importance score of a memory"""
        new_importance = min(1.0, max(0.0, new_importance))
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE memories 
                    SET importance = ? 
                    WHERE id = ?
                ''', (new_importance, memory_id))
                
                conn.commit()
                
                # Update cache
                if memory_id in self.memory_cache:
                    self.memory_cache[memory_id].importance = new_importance
                
                return True
                
        except Exception as e:
            print(f"❌ Failed to update importance for {memory_id}: {e}")
            return False
    
    def create_association(self, memory_id_1: str, memory_id_2: str, 
                          association_type: str = "related", strength: float = 0.5) -> bool:
        """
        Create an association between two memories
        
        Args:
            memory_id_1: First memory ID
            memory_id_2: Second memory ID
            association_type: Type of association (related, caused_by, follows, etc.)
            strength: Strength of association (0.0 to 1.0)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO memory_associations 
                    (memory_id_1, memory_id_2, association_type, strength, created_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (memory_id_1, memory_id_2, association_type, strength, datetime.now().isoformat()))
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"❌ Failed to create association: {e}")
            return False
    
    def get_associated_memories(self, memory_id: str, limit: int = 5) -> List[MemoryEntry]:
        """Get memories associated with a given memory"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Find associated memory IDs
                cursor.execute('''
                    SELECT memory_id_2, association_type, strength 
                    FROM memory_associations 
                    WHERE memory_id_1 = ?
                    UNION
                    SELECT memory_id_1, association_type, strength 
                    FROM memory_associations 
                    WHERE memory_id_2 = ?
                    ORDER BY strength DESC
                    LIMIT ?
                ''', (memory_id, memory_id, limit))
                
                associated_ids = cursor.fetchall()
                
                # Retrieve the actual memories
                memories = []
                for assoc_id, assoc_type, strength in associated_ids:
                    if assoc_id != memory_id:  # Don't include self
                        memory = self.recall(assoc_id)
                        if memory:
                            memories.append(memory)
                
                return memories
                
        except Exception as e:
            print(f"❌ Failed to get associated memories: {e}")
            return []
    
    def cleanup_expired_memories(self) -> int:
        """Remove expired memories and return count of deleted entries"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get expired memory IDs
                cursor.execute('''
                    SELECT id FROM memories 
                    WHERE expires_at IS NOT NULL 
                    AND expires_at <= datetime("now")
                ''')
                
                expired_ids = [row[0] for row in cursor.fetchall()]
                
                # Delete expired memories
                cursor.execute('''
                    DELETE FROM memories 
                    WHERE expires_at IS NOT NULL 
                    AND expires_at <= datetime("now")
                ''')
                
                # Delete their associations
                for memory_id in expired_ids:
                    cursor.execute('''
                        DELETE FROM memory_associations 
                        WHERE memory_id_1 = ? OR memory_id_2 = ?
                    ''', (memory_id, memory_id))
                    
                    # Remove from cache
                    if memory_id in self.memory_cache:
                        del self.memory_cache[memory_id]
                
                conn.commit()
                
                print(f"🧹 Cleaned up {len(expired_ids)} expired memories")
                return len(expired_ids)
                
        except Exception as e:
            print(f"❌ Cleanup failed: {e}")
            return 0
    
    def backup_to_json(self) -> bool:
        """Create a JSON backup of all memories"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('SELECT * FROM memories')
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
                memories_data = []
                for row in rows:
                    memory_dict = dict(zip(columns, row))
                    # Convert content and tags back to objects
                    memory_dict['content'] = json.loads(memory_dict['content'])
                    memory_dict['tags'] = json.loads(memory_dict['tags'])
                    memories_data.append(memory_dict)
                
                # Also backup associations
                cursor.execute('SELECT * FROM memory_associations')
                assoc_rows = cursor.fetchall()
                assoc_columns = [desc[0] for desc in cursor.description]
                
                associations_data = []
                for row in assoc_rows:
                    assoc_dict = dict(zip(assoc_columns, row))
                    associations_data.append(assoc_dict)
                
                # Create backup object
                backup_data = {
                    "backup_timestamp": datetime.now().isoformat(),
                    "memories": memories_data,
                    "associations": associations_data,
                    "version": "1.0"
                }
                
                # Write to JSON file
                with open(self.json_backup, 'w', encoding='utf-8') as f:
                    json.dump(backup_data, f, indent=2, ensure_ascii=False)
                
                print(f"💾 Memory backup created: {self.json_backup}")
                return True
                
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get comprehensive memory system statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total memories
                cursor.execute('SELECT COUNT(*) FROM memories')
                total_memories = cursor.fetchone()[0]
                
                # Memories by type
                cursor.execute('''
                    SELECT memory_type, COUNT(*) 
                    FROM memories 
                    GROUP BY memory_type
                ''')
                memories_by_type = dict(cursor.fetchall())
                
                # Average importance
                cursor.execute('SELECT AVG(importance) FROM memories')
                avg_importance = cursor.fetchone()[0] or 0.0
                
                # Recent activity (last 24 hours)
                since_24h = (datetime.now() - timedelta(hours=24)).isoformat()
                cursor.execute('SELECT COUNT(*) FROM memories WHERE timestamp >= ?', (since_24h,))
                recent_memories = cursor.fetchone()[0]
                
                # Expired memories
                cursor.execute('''
                    SELECT COUNT(*) FROM memories 
                    WHERE expires_at IS NOT NULL AND expires_at <= datetime("now")
                ''')
                expired_memories = cursor.fetchone()[0]
                
                # Total associations
                cursor.execute('SELECT COUNT(*) FROM memory_associations')
                total_associations = cursor.fetchone()[0]
                
                return {
                    "total_memories": total_memories,
                    "memories_by_type": memories_by_type,
                    "average_importance": round(avg_importance, 3),
                    "recent_memories_24h": recent_memories,
                    "expired_memories": expired_memories,
                    "total_associations": total_associations,
                    "cache_size": len(self.memory_cache),
                    "database_path": self.db_path,
                    "backup_path": self.json_backup
                }
                
        except Exception as e:
            print(f"❌ Failed to get memory stats: {e}")
            return {"error": str(e)}
    
    def _create_associations(self, memory_entry: MemoryEntry):
        """Automatically create associations based on content similarity and timing"""
        try:
            # Find recent memories of the same type
            recent_memories = self.get_recent_memories(hours=1, limit=5)
            
            for recent_memory in recent_memories:
                if recent_memory.id != memory_entry.id:
                    # Calculate similarity score (simple tag overlap for now)
                    common_tags = set(memory_entry.tags) & set(recent_memory.tags)
                    if common_tags:
                        strength = len(common_tags) / max(len(memory_entry.tags), len(recent_memory.tags))
                        if strength > 0.3:  # Threshold for association
                            self.create_association(
                                memory_entry.id,
                                recent_memory.id,
                                "temporal_proximity",
                                strength
                            )
        except Exception as e:
            print(f"⚠️ Auto-association failed: {e}")
    
    def _update_access_stats(self, memory_id: str):
        """Update access statistics for a memory"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE memories 
                    SET access_count = access_count + 1,
                        last_accessed = ?
                    WHERE id = ?
                ''', (datetime.now().isoformat(), memory_id))
                
                conn.commit()
                
        except Exception as e:
            print(f"⚠️ Failed to update access stats: {e}")
    
    def _dict_to_memory_entry(self, memory_dict: Dict[str, Any]) -> MemoryEntry:
        """Convert database dictionary to MemoryEntry object"""
        return MemoryEntry(
            id=memory_dict['id'],
            timestamp=memory_dict['timestamp'],
            content=json.loads(memory_dict['content']),
            tags=json.loads(memory_dict['tags']),
            importance=memory_dict['importance'],
            memory_type=memory_dict['memory_type'],
            context=memory_dict.get('context'),
            expires_at=memory_dict.get('expires_at')
        )

# Test function for development
def test_memory():
    """Test the memory functionality"""
    print("🧪 Testing Memory Module...")
    
    memory = Memory()
    
    # Test storing memory
    print("💾 Testing memory storage...")
    memory_id = memory.remember(
        content={"test": "This is a test memory", "value": 42},
        tags=["test", "example"],
        memory_type="test",
        importance=0.8
    )
    print(f"Stored memory: {memory_id}")
    
    # Test retrieval
    print("🔍 Testing memory retrieval...")
    retrieved = memory.recall(memory_id)
    if retrieved:
        print(f"Retrieved: {retrieved.content}")
    
    # Test search
    print("🔎 Testing memory search...")
    search_results = memory.search_memories(query="test", limit=5)
    print(f"Search found {len(search_results)} memories")
    
    # Test stats
    stats = memory.get_memory_stats()
    print(f"📊 Memory stats: {json.dumps(stats, indent=2)}")
    
    print("✅ Memory test completed")

if __name__ == "__main__":
    test_memory()
