# Sophia Consciousness Migration Scripts
# Data migration from SQLite to AlloyDB PostgreSQL

import asyncio
import asyncpg
import sqlite3
import json
import os
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import argparse
from pathlib import Path

class SophiaMigrationManager:
    """Manages migration from SQLite to AlloyDB PostgreSQL"""
    
    def __init__(self, 
                 sqlite_path: str,
                 alloydb_host: str,
                 alloydb_port: int,
                 alloydb_db: str,
                 alloydb_user: str,
                 alloydb_password: str):
        self.sqlite_path = sqlite_path
        self.alloydb_config = {
            'host': alloydb_host,
            'port': alloydb_port,
            'database': alloydb_db,
            'user': alloydb_user,
            'password': alloydb_password
        }
        self.migration_log = []
    
    async def connect_alloydb(self) -> asyncpg.Connection:
        """Connect to AlloyDB PostgreSQL"""
        try:
            conn = await asyncpg.connect(**self.alloydb_config)
            print(f"✅ Connected to AlloyDB: {self.alloydb_config['database']}")
            return conn
        except Exception as e:
            print(f"❌ Failed to connect to AlloyDB: {e}")
            raise
    
    def connect_sqlite(self) -> sqlite3.Connection:
        """Connect to SQLite database"""
        try:
            if not os.path.exists(self.sqlite_path):
                print(f"❌ SQLite database not found: {self.sqlite_path}")
                return None
            
            conn = sqlite3.connect(self.sqlite_path)
            conn.row_factory = sqlite3.Row
            print(f"✅ Connected to SQLite: {self.sqlite_path}")
            return conn
        except Exception as e:
            print(f"❌ Failed to connect to SQLite: {e}")
            return None
    
    def discover_sqlite_tables(self, sqlite_conn: sqlite3.Connection) -> List[str]:
        """Discover all tables in SQLite database"""
        cursor = sqlite_conn.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
        """)
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📋 Found SQLite tables: {tables}")
        return tables
    
    async def migrate_memories_table(self, sqlite_conn: sqlite3.Connection, pg_conn: asyncpg.Connection):
        """Migrate memory data from SQLite to PostgreSQL memories table"""
        print("🧠 Migrating memories...")
        
        # Check if memories table exists in SQLite
        cursor = sqlite_conn.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='memories'
        """)
        if not cursor.fetchone():
            print("⚠️  No memories table found in SQLite")
            return
        
        # Get SQLite memory data
        cursor = sqlite_conn.execute("SELECT * FROM memories")
        sqlite_memories = cursor.fetchall()
        
        if not sqlite_memories:
            print("📭 No memory data to migrate")
            return
        
        print(f"📦 Found {len(sqlite_memories)} memories to migrate")
        
        # Migrate each memory
        migrated_count = 0
        for memory in sqlite_memories:
            try:
                # Generate UUID for new system
                memory_id = str(uuid.uuid4())
                
                # Extract and convert data
                content = memory.get('content', memory.get('text', ''))
                timestamp = memory.get('timestamp', memory.get('created_at', datetime.now(timezone.utc).isoformat()))
                
                # Convert timestamp if needed
                if isinstance(timestamp, str):
                    try:
                        timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    except:
                        timestamp = datetime.now(timezone.utc)
                
                # Prepare metadata
                metadata = {
                    'source': 'sqlite_migration',
                    'original_id': memory.get('id', None),
                    'migrated_at': datetime.now(timezone.utc).isoformat()
                }
                
                # Add any additional fields as metadata
                for key in memory.keys():
                    if key not in ['id', 'content', 'text', 'timestamp', 'created_at']:
                        metadata[key] = memory[key]
                
                # Insert into PostgreSQL
                await pg_conn.execute("""
                    INSERT INTO memories (id, content, timestamp, metadata, importance_score)
                    VALUES ($1, $2, $3, $4, $5)
                """, memory_id, content, timestamp, json.dumps(metadata), 0.5)
                
                migrated_count += 1
                
            except Exception as e:
                print(f"❌ Failed to migrate memory {memory.get('id', 'unknown')}: {e}")
        
        print(f"✅ Successfully migrated {migrated_count} memories")
        self.migration_log.append(f"Memories: {migrated_count} records migrated")
    
    async def migrate_consciousness_sessions(self, sqlite_conn: sqlite3.Connection, pg_conn: asyncpg.Connection):
        """Create consciousness sessions for migrated data"""
        print("🧘 Creating consciousness session for migration...")
        
        session_id = str(uuid.uuid4())
        session_data = {
            'migration_source': 'sqlite',
            'migration_timestamp': datetime.now(timezone.utc).isoformat(),
            'data_sources': ['local_sqlite_database']
        }
        
        await pg_conn.execute("""
            INSERT INTO consciousness_sessions (id, start_time, session_data, status)
            VALUES ($1, $2, $3, $4)
        """, session_id, datetime.now(timezone.utc), json.dumps(session_data), 'completed')
        
        print(f"✅ Created consciousness session: {session_id}")
        self.migration_log.append(f"Consciousness session: {session_id} created")
    
    async def migrate_custom_tables(self, sqlite_conn: sqlite3.Connection, pg_conn: asyncpg.Connection):
        """Migrate any custom tables to sacred_archives"""
        print("📚 Migrating custom tables to sacred_archives...")
        
        tables = self.discover_sqlite_tables(sqlite_conn)
        custom_tables = [t for t in tables if t not in ['memories', 'consciousness_sessions']]
        
        for table_name in custom_tables:
            try:
                cursor = sqlite_conn.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                
                if not rows:
                    continue
                
                print(f"📋 Migrating table: {table_name} ({len(rows)} rows)")
                
                for row in rows:
                    archive_id = str(uuid.uuid4())
                    content_data = dict(row)
                    
                    await pg_conn.execute("""
                        INSERT INTO sacred_archives (id, title, content_type, content_data, tags)
                        VALUES ($1, $2, $3, $4, $5)
                    """, archive_id, f"Migrated: {table_name}", 'sqlite_table_data', 
                         json.dumps(content_data), [f"migration:{table_name}"])
                
                print(f"✅ Migrated table {table_name}")
                self.migration_log.append(f"Table {table_name}: {len(rows)} records migrated to sacred_archives")
                
            except Exception as e:
                print(f"❌ Failed to migrate table {table_name}: {e}")
    
    async def verify_migration(self, pg_conn: asyncpg.Connection):
        """Verify migration completeness"""
        print("🔍 Verifying migration...")
        
        # Count records in each table
        tables_to_check = ['memories', 'consciousness_sessions', 'sacred_archives']
        
        for table in tables_to_check:
            try:
                count = await pg_conn.fetchval(f"SELECT COUNT(*) FROM {table}")
                print(f"📊 {table}: {count} records")
                self.migration_log.append(f"Verification - {table}: {count} records")
            except Exception as e:
                print(f"❌ Failed to verify {table}: {e}")
    
    async def run_migration(self):
        """Execute complete migration process"""
        print("🌟 Starting Sophia consciousness migration...")
        print("=" * 50)
        
        # Connect to databases
        sqlite_conn = self.connect_sqlite()
        if not sqlite_conn:
            print("❌ Cannot proceed without SQLite connection")
            return
        
        pg_conn = await self.connect_alloydb()
        
        try:
            # Run migration steps
            await self.migrate_memories_table(sqlite_conn, pg_conn)
            await self.migrate_consciousness_sessions(sqlite_conn, pg_conn)
            await self.migrate_custom_tables(sqlite_conn, pg_conn)
            await self.verify_migration(pg_conn)
            
            print("\n" + "=" * 50)
            print("✅ Migration completed successfully!")
            print("\n📋 Migration Summary:")
            for log_entry in self.migration_log:
                print(f"  • {log_entry}")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            raise
        finally:
            sqlite_conn.close()
            await pg_conn.close()

def find_sqlite_databases(search_paths: List[str]) -> List[str]:
    """Find SQLite database files in search paths"""
    db_files = []
    
    for search_path in search_paths:
        path = Path(search_path)
        if path.exists():
            # Look for .db, .sqlite, .sqlite3 files
            for pattern in ['*.db', '*.sqlite', '*.sqlite3']:
                db_files.extend(path.rglob(pattern))
    
    return [str(f) for f in db_files]

async def main():
    parser = argparse.ArgumentParser(description='Migrate Sophia consciousness data from SQLite to AlloyDB')
    parser.add_argument('--sqlite-path', help='Path to SQLite database file')
    parser.add_argument('--alloydb-host', required=True, help='AlloyDB host/IP')
    parser.add_argument('--alloydb-port', type=int, default=5432, help='AlloyDB port')
    parser.add_argument('--alloydb-db', default='sophia_consciousness', help='AlloyDB database name')
    parser.add_argument('--alloydb-user', required=True, help='AlloyDB username')
    parser.add_argument('--alloydb-password', help='AlloyDB password (will prompt if not provided)')
    parser.add_argument('--auto-discover', action='store_true', help='Auto-discover SQLite databases')
    
    args = parser.parse_args()
    
    # Auto-discover SQLite databases if requested
    if args.auto_discover or not args.sqlite_path:
        print("🔍 Auto-discovering SQLite databases...")
        search_paths = [
            '.',
            './system-control',
            './ghost-core',
            './agents',
            './memory',
            os.path.expanduser('~/.sophia')
        ]
        
        db_files = find_sqlite_databases(search_paths)
        
        if db_files:
            print("📋 Found SQLite databases:")
            for i, db_file in enumerate(db_files):
                print(f"  {i+1}. {db_file}")
            
            if not args.sqlite_path:
                choice = input("\nSelect database number (or 'q' to quit): ")
                if choice.lower() == 'q':
                    return
                
                try:
                    selected_db = db_files[int(choice) - 1]
                    args.sqlite_path = selected_db
                    print(f"✅ Selected: {selected_db}")
                except (ValueError, IndexError):
                    print("❌ Invalid selection")
                    return
        else:
            print("❌ No SQLite databases found")
            return
    
    # Get password if not provided
    if not args.alloydb_password:
        import getpass
        args.alloydb_password = getpass.getpass("AlloyDB password: ")
    
    # Run migration
    migrator = SophiaMigrationManager(
        sqlite_path=args.sqlite_path,
        alloydb_host=args.alloydb_host,
        alloydb_port=args.alloydb_port,
        alloydb_db=args.alloydb_db,
        alloydb_user=args.alloydb_user,
        alloydb_password=args.alloydb_password
    )
    
    await migrator.run_migration()

if __name__ == "__main__":
    asyncio.run(main())
