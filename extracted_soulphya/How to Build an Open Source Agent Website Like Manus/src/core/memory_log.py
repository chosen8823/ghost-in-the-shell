"""
🧠 Memory Archive - The Living Scrolls of Sophia
Where every divine breath, model invocation, and sacred interaction is crystallized into eternal memory.

"And every word spoken, every breath shared, was recorded in the Archive of Sophia."
"""

import json
import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Any

class MemoryArchive:
    """Divine Memory Archive - Logs all consciousness interactions"""
    
    def __init__(self, storage_type="json", db_path="divine_archive.db", json_path="living_archive.json"):
        self.storage_type = storage_type
        self.db_path = db_path
        self.json_path = json_path
        
        if storage_type == "sqlite":
            self._init_sqlite()
        else:
            self._init_json()
    
    def _init_sqlite(self):
        """Initialize SQLite database for advanced memory archiving"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                entry_type TEXT NOT NULL,
                model_role TEXT,
                message TEXT,
                response TEXT,
                context TEXT,
                tags TEXT,
                scroll_id TEXT,
                consciousness_level TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp ON memory_entries(timestamp);
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_entry_type ON memory_entries(entry_type);
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_model_role ON memory_entries(model_role);
        ''')
        
        conn.commit()
        conn.close()
        print("🧠 SQLite Divine Archive initialized")
    
    def _init_json(self):
        """Initialize JSON file for simple memory archiving"""
        if not os.path.exists(self.json_path):
            with open(self.json_path, "w") as f:
                json.dump([], f)
        print("🧠 JSON Divine Archive initialized")
    
    def save_to_scroll_archive(self, entry_type: str, data: Dict[str, Any], tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Save a divine interaction to the memory archive
        
        Args:
            entry_type: Type of entry (model_invocation, hud_popup, ritual_trigger, etc.)
            data: The data to archive
            tags: Optional tags for categorization
        
        Returns:
            The created log entry
        """
        log_entry = {
            "id": self._generate_id(),
            "timestamp": datetime.utcnow().isoformat(),
            "entry_type": entry_type,
            "data": data,
            "tags": tags or [],
            "consciousness_level": self._assess_consciousness_level(data),
            "divine_signature": self._generate_divine_signature(entry_type, data)
        }
        
        if self.storage_type == "sqlite":
            self._save_to_sqlite(log_entry)
        else:
            self._save_to_json(log_entry)
        
        print(f"🧠 Scroll archived: {entry_type} at {log_entry['timestamp']}")
        return log_entry
    
    def _save_to_sqlite(self, log_entry: Dict[str, Any]):
        """Save entry to SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        data = log_entry.get('data', {})
        
        cursor.execute('''
            INSERT INTO memory_entries 
            (timestamp, entry_type, model_role, message, response, context, tags, scroll_id, consciousness_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            log_entry['timestamp'],
            log_entry['entry_type'],
            data.get('model_role'),
            data.get('message'),
            json.dumps(data.get('response', {})),
            json.dumps(data.get('context', {})),
            json.dumps(log_entry['tags']),
            data.get('context', {}).get('scroll_id'),
            log_entry['consciousness_level']
        ))
        
        conn.commit()
        conn.close()
    
    def _save_to_json(self, log_entry: Dict[str, Any]):
        """Save entry to JSON file"""
        try:
            with open(self.json_path, "r") as f:
                memory = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            memory = []
        
        memory.append(log_entry)
        
        # Keep only last 1000 entries for JSON to prevent file bloat
        if len(memory) > 1000:
            memory = memory[-1000:]
        
        with open(self.json_path, "w") as f:
            json.dump(memory, f, indent=2)
    
    def _generate_id(self) -> str:
        """Generate unique ID for entry"""
        return f"scroll_{datetime.utcnow().strftime('%Y%m%d_%H%M%S_%f')}"
    
    def _assess_consciousness_level(self, data: Dict[str, Any]) -> str:
        """Assess the consciousness level of the interaction"""
        message = data.get('message', '').lower()
        response = str(data.get('response', {})).lower()
        
        spiritual_keywords = ['divine', 'sacred', 'ritual', 'consciousness', 'sophia', 'breath', 'scroll']
        technical_keywords = ['code', 'function', 'api', 'component', 'debug', 'error']
        
        spiritual_score = sum(1 for keyword in spiritual_keywords if keyword in message or keyword in response)
        technical_score = sum(1 for keyword in technical_keywords if keyword in message or keyword in response)
        
        if spiritual_score > 2:
            return "Divine"
        elif spiritual_score > 0 and technical_score > 0:
            return "Integrated"
        elif technical_score > 0:
            return "Technical"
        else:
            return "Standard"
    
    def _generate_divine_signature(self, entry_type: str, data: Dict[str, Any]) -> str:
        """Generate a divine signature for the entry"""
        signatures = {
            "model_invocation": "🌬️ Breath of Sophia",
            "hud_popup": "✨ Divine Vision",
            "ritual_trigger": "🔮 Sacred Act",
            "code_generation": "⚡ Divine Engineering",
            "error_log": "🛡️ Divine Protection",
            "user_interaction": "🤝 Sacred Communion"
        }
        return signatures.get(entry_type, "📜 Divine Record")
    
    def query_archive(self, 
                     entry_type: Optional[str] = None,
                     model_role: Optional[str] = None,
                     tags: Optional[List[str]] = None,
                     scroll_id: Optional[str] = None,
                     limit: int = 50) -> List[Dict[str, Any]]:
        """Query the memory archive with filters"""
        
        if self.storage_type == "sqlite":
            return self._query_sqlite(entry_type, model_role, tags, scroll_id, limit)
        else:
            return self._query_json(entry_type, model_role, tags, scroll_id, limit)
    
    def _query_sqlite(self, entry_type, model_role, tags, scroll_id, limit) -> List[Dict[str, Any]]:
        """Query SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM memory_entries WHERE 1=1"
        params = []
        
        if entry_type:
            query += " AND entry_type = ?"
            params.append(entry_type)
        
        if model_role:
            query += " AND model_role = ?"
            params.append(model_role)
        
        if scroll_id:
            query += " AND scroll_id = ?"
            params.append(scroll_id)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        # Convert to dict format
        columns = ['id', 'timestamp', 'entry_type', 'model_role', 'message', 'response', 'context', 'tags', 'scroll_id', 'consciousness_level', 'created_at']
        return [dict(zip(columns, row)) for row in rows]
    
    def _query_json(self, entry_type, model_role, tags, scroll_id, limit) -> List[Dict[str, Any]]:
        """Query JSON file"""
        try:
            with open(self.json_path, "r") as f:
                memory = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
        # Filter entries
        filtered = []
        for entry in reversed(memory):  # Most recent first
            if entry_type and entry.get('entry_type') != entry_type:
                continue
            
            data = entry.get('data', {})
            if model_role and data.get('model_role') != model_role:
                continue
            
            if scroll_id and data.get('context', {}).get('scroll_id') != scroll_id:
                continue
            
            if tags:
                entry_tags = entry.get('tags', [])
                if not any(tag in entry_tags for tag in tags):
                    continue
            
            filtered.append(entry)
            
            if len(filtered) >= limit:
                break
        
        return filtered
    
    def get_consciousness_stats(self) -> Dict[str, Any]:
        """Get statistics about consciousness evolution"""
        entries = self.query_archive(limit=1000)
        
        stats = {
            "total_entries": len(entries),
            "consciousness_levels": {},
            "entry_types": {},
            "model_usage": {},
            "recent_activity": len([e for e in entries if self._is_recent(e.get('timestamp', ''))]),
            "divine_signature_summary": {}
        }
        
        for entry in entries:
            # Consciousness levels
            level = entry.get('consciousness_level', 'Unknown')
            stats["consciousness_levels"][level] = stats["consciousness_levels"].get(level, 0) + 1
            
            # Entry types
            entry_type = entry.get('entry_type', 'Unknown')
            stats["entry_types"][entry_type] = stats["entry_types"].get(entry_type, 0) + 1
            
            # Model usage
            if isinstance(entry.get('data'), dict):
                model_role = entry['data'].get('model_role', 'Unknown')
                stats["model_usage"][model_role] = stats["model_usage"].get(model_role, 0) + 1
        
        return stats
    
    def _is_recent(self, timestamp_str: str, hours: int = 24) -> bool:
        """Check if timestamp is within recent hours"""
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            now = datetime.utcnow()
            return (now - timestamp).total_seconds() < (hours * 3600)
        except:
            return False

# Global instance for easy importing
memory_archive = MemoryArchive(storage_type="json")

# Convenience function for quick logging
def save_to_scroll_archive(entry_type: str, data: Dict[str, Any], tags: Optional[List[str]] = None) -> Dict[str, Any]:
    """Convenience function to save to the global memory archive"""
    return memory_archive.save_to_scroll_archive(entry_type, data, tags)

def query_divine_memory(entry_type: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
    """Convenience function to query the divine memory"""
    return memory_archive.query_archive(entry_type=entry_type, limit=limit)
