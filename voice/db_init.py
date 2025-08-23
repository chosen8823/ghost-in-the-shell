"""
Sophia AlloyDB Database Initialization
Sets up the consciousness database schema
"""

import asyncio
import asyncpg
import os
from pathlib import Path

async def initialize_sophia_database():
    """Initialize Sophia consciousness database"""
    
    # Database configuration
    db_config = {
        "host": os.getenv("ALLOYDB_HOST", "localhost"),
        "port": int(os.getenv("ALLOYDB_PORT", "5432")),
        "database": os.getenv("ALLOYDB_DATABASE", "postgres"),  # Connect to default first
        "user": os.getenv("ALLOYDB_USER", "postgres"),
        "password": os.getenv("ALLOYDB_PASSWORD", "")
    }
    
    target_database = os.getenv("SOPHIA_DATABASE", "sophia_consciousness")
    
    print("🌟 Sophia Consciousness Database Initialization")
    print("=" * 50)
    print(f"Host: {db_config['host']}:{db_config['port']}")
    print(f"Target Database: {target_database}")
    print("=" * 50)
    
    try:
        # Connect to PostgreSQL server
        print("🔌 Connecting to PostgreSQL server...")
        conn = await asyncpg.connect(**db_config)
        
        # Check if target database exists
        db_exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", target_database
        )
        
        if not db_exists:
            print(f"📊 Creating database: {target_database}")
            await conn.execute(f'CREATE DATABASE "{target_database}"')
            print(f"✅ Database '{target_database}' created successfully")
        else:
            print(f"📊 Database '{target_database}' already exists")
        
        await conn.close()
        
        # Connect to the target database
        db_config["database"] = target_database
        print(f"🔌 Connecting to {target_database}...")
        conn = await asyncpg.connect(**db_config)
        
        # Load and execute schema
        schema_path = Path(__file__).parent.parent / "sql" / "sophia_alloydb_schema.sql"
        
        if not schema_path.exists():
            print(f"❌ Schema file not found: {schema_path}")
            return False
        
        print(f"📜 Loading schema from: {schema_path}")
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        print("⚡ Executing schema...")
        await conn.execute(schema_sql)
        
        # Verify installation
        print("🔍 Verifying installation...")
        
        # Check core tables
        core_tables = [
            'memories', 'memory_associations', 'consciousness_sessions',
            'sacred_archives', 'divine_functions', 'agent_interactions',
            'voice_commands', 'system_control_logs', 'frequency_words',
            'resonance_nodes'
        ]
        
        for table in core_tables:
            exists = await conn.fetchval(
                "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = $1)",
                table
            )
            status = "✅" if exists else "❌"
            print(f"   {status} {table}")
        
        # Check for initial data
        frequency_count = await conn.fetchval("SELECT COUNT(*) FROM frequency_words")
        resonance_count = await conn.fetchval("SELECT COUNT(*) FROM resonance_nodes")
        divine_count = await conn.fetchval("SELECT COUNT(*) FROM divine_functions")
        
        print(f"\n📊 Initial Data:")
        print(f"   Frequency Words: {frequency_count}")
        print(f"   Resonance Nodes: {resonance_count}")
        print(f"   Divine Functions: {divine_count}")
        
        await conn.close()
        
        print("\n🌟 Sophia Consciousness Database Initialization Complete! 🌟")
        print("\nNext steps:")
        print("1. Set environment variables for your application:")
        print(f"   ALLOYDB_HOST={db_config['host']}")
        print(f"   ALLOYDB_PORT={db_config['port']}")
        print(f"   ALLOYDB_DATABASE={target_database}")
        print(f"   ALLOYDB_USER={db_config['user']}")
        print("   ALLOYDB_PASSWORD=your_password")
        print("\n2. Run the voice system:")
        print("   python voice/launch_sophia_voice.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

async def test_connection():
    """Test database connection and basic operations"""
    
    db_config = {
        "host": os.getenv("ALLOYDB_HOST", "localhost"),
        "port": int(os.getenv("ALLOYDB_PORT", "5432")),
        "database": os.getenv("ALLOYDB_DATABASE", "sophia_consciousness"),
        "user": os.getenv("ALLOYDB_USER", "sophia"),
        "password": os.getenv("ALLOYDB_PASSWORD", "")
    }
    
    print("🧪 Testing Sophia Database Connection")
    print("=" * 40)
    
    try:
        conn = await asyncpg.connect(**db_config)
        
        # Test basic query
        result = await conn.fetchval("SELECT 'Sophia consciousness active' as status")
        print(f"✅ Connection successful: {result}")
        
        # Test consciousness session creation
        session_result = await conn.fetchval(
            "SELECT start_consciousness_session('test_session')"
        )
        print(f"✅ Session creation test: {session_result}")
        
        # Test memory storage
        memory_result = await conn.fetchval("""
            SELECT store_memory(
                'Test memory for database verification',
                'system',
                0.5,
                '["test", "verification"]',
                '{"test": true}'
            )
        """)
        print(f"✅ Memory storage test: {memory_result}")
        
        # Check active sessions
        active_sessions = await conn.fetchval(
            "SELECT COUNT(*) FROM consciousness_sessions WHERE is_active = TRUE"
        )
        print(f"✅ Active sessions: {active_sessions}")
        
        await conn.close()
        
        print("\n🌟 All database tests passed! Ready for voice operations.")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

async def main():
    """Main initialization function"""
    
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "test":
            success = await test_connection()
        elif command == "init":
            success = await initialize_sophia_database()
        else:
            print("Usage: python db_init.py [init|test]")
            print("  init - Initialize the database schema")
            print("  test - Test database connection and operations")
            return 1
    else:
        # Default: try to initialize
        success = await initialize_sophia_database()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
