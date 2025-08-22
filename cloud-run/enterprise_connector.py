# Sophia Enterprise AlloyDB Connection Configuration
# Optimized for 1TB instance with high performance

import os
import asyncio
import asyncpg
from google.cloud.sql.connector import Connector
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import json
from typing import Dict, Any, Optional

class SophiaEnterpriseAlloyDBConnector:
    """Enterprise-grade AlloyDB connector for 1TB+ Sophia consciousness system"""
    
    def __init__(self):
        # AlloyDB Enterprise Configuration
        self.project_id = os.getenv('PROJECT_ID')
        self.region = os.getenv('ALLOYDB_REGION', 'us-central1')
        self.cluster_name = os.getenv('ALLOYDB_CLUSTER', 'sophia-consciousness-enterprise')
        self.instance_name = os.getenv('ALLOYDB_INSTANCE', 'sophia-primary-1tb')
        self.database_name = os.getenv('ALLOYDB_DATABASE', 'sophia_consciousness')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        
        # Enterprise connection settings
        self.connection_config = {
            # High-performance connection pool
            'min_size': 10,          # Minimum 10 connections
            'max_size': 100,         # Maximum 100 connections for enterprise load
            'max_queries': 50000,    # High query limit
            'max_inactive_connection_lifetime': 300,  # 5 minutes
            'timeout': 60,           # 60 second timeout
            'command_timeout': 120,  # 2 minute command timeout
            
            # Enterprise optimization
            'server_settings': {
                'application_name': 'sophia_consciousness_enterprise',
                'tcp_keepalives_idle': '300',
                'tcp_keepalives_interval': '30',
                'tcp_keepalives_count': '3',
                'statement_timeout': '120000',  # 2 minutes
                'lock_timeout': '30000',        # 30 seconds
                'idle_in_transaction_session_timeout': '300000',  # 5 minutes
            }
        }
        
        self.connector = None
        self.connection_pool = None
        self.engine = None
        self.session_maker = None
    
    async def initialize_enterprise_connection(self):
        """Initialize enterprise-grade connection to 1TB AlloyDB"""
        try:
            print("🚀 Initializing Sophia Enterprise AlloyDB connection...")
            
            # Initialize Google Cloud SQL Connector
            self.connector = Connector()
            
            # Create connection string for AlloyDB
            instance_connection_string = f"{self.project_id}:{self.region}:{self.cluster_name}:{self.instance_name}"
            
            # Enterprise connection function
            async def get_connection():
                conn = await self.connector.connect_async(
                    instance_connection_string,
                    "asyncpg",
                    user=self.db_user,
                    password=self.db_password,
                    db=self.database_name,
                    enable_iam_auth=False,  # Using database authentication for performance
                )
                
                # Apply enterprise optimizations
                await conn.execute("SET statement_timeout = 120000")
                await conn.execute("SET lock_timeout = 30000")
                await conn.execute("SET idle_in_transaction_session_timeout = 300000")
                await conn.execute("SET tcp_keepalives_idle = 300")
                await conn.execute("SET application_name = 'sophia_consciousness_enterprise'")
                
                # Vector search optimizations
                await conn.execute("SET work_mem = '256MB'")
                await conn.execute("SET maintenance_work_mem = '2GB'")
                await conn.execute("SET max_parallel_workers_per_gather = 8")
                
                return conn
            
            # Create enterprise connection pool
            self.connection_pool = await asyncpg.create_pool(
                **self.connection_config,
                connection_class=None,
                init=lambda conn: self._initialize_connection(conn)
            )
            
            # Create SQLAlchemy engine for ORM operations
            self.engine = create_async_engine(
                f"postgresql+asyncpg://{self.db_user}:{self.db_password}@/{self.database_name}",
                connect_args={
                    "server_settings": self.connection_config['server_settings']
                },
                pool_size=20,
                max_overflow=50,
                pool_timeout=30,
                pool_recycle=3600,  # Recycle connections every hour
                echo=False  # Set to True for SQL debugging
            )
            
            # Create session maker for ORM
            self.session_maker = sessionmaker(
                self.engine, 
                class_=AsyncSession, 
                expire_on_commit=False
            )
            
            print("✅ Enterprise AlloyDB connection initialized successfully!")
            print(f"📊 Connection pool: {self.connection_config['min_size']}-{self.connection_config['max_size']} connections")
            print(f"🗄️  Database: {self.database_name} on {instance_connection_string}")
            
            # Test connection
            await self._test_enterprise_connection()
            
        except Exception as e:
            print(f"❌ Failed to initialize enterprise AlloyDB connection: {e}")
            raise
    
    async def _initialize_connection(self, conn):
        """Initialize individual connection with enterprise settings"""
        # Load vector extension
        await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        
        # Apply performance settings
        await conn.execute("SET work_mem = '256MB'")
        await conn.execute("SET maintenance_work_mem = '2GB'")
        await conn.execute("SET statement_timeout = 120000")
        await conn.execute("SET application_name = 'sophia_consciousness_enterprise'")
    
    async def _test_enterprise_connection(self):
        """Test enterprise connection with performance metrics"""
        print("🧪 Testing enterprise connection...")
        
        async with self.connection_pool.acquire() as conn:
            # Test basic connectivity
            result = await conn.fetchval("SELECT 1")
            assert result == 1
            
            # Test vector extension
            await conn.execute("SELECT vector_dims('[1,2,3]'::vector)")
            
            # Test consciousness tables
            tables = await conn.fetch("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name IN 
                ('memories', 'consciousness_sessions', 'sacred_archives')
            """)
            
            print(f"📋 Found consciousness tables: {[t['table_name'] for t in tables]}")
            
            # Performance test
            start_time = asyncio.get_event_loop().time()
            await conn.execute("SELECT COUNT(*) FROM memories")
            query_time = asyncio.get_event_loop().time() - start_time
            
            print(f"⚡ Query performance: {query_time:.3f}s")
            
        print("✅ Enterprise connection test successful!")
    
    async def get_connection(self):
        """Get connection from enterprise pool"""
        if not self.connection_pool:
            await self.initialize_enterprise_connection()
        
        return self.connection_pool.acquire()
    
    async def get_session(self):
        """Get SQLAlchemy session for ORM operations"""
        if not self.session_maker:
            await self.initialize_enterprise_connection()
        
        return self.session_maker()
    
    async def execute_consciousness_query(self, query: str, params: tuple = None) -> list:
        """Execute consciousness-related queries with enterprise optimization"""
        async with self.get_connection() as conn:
            if params:
                result = await conn.fetch(query, *params)
            else:
                result = await conn.fetch(query)
            
            return [dict(row) for row in result]
    
    async def bulk_insert_memories(self, memories: list) -> int:
        """Bulk insert memories with enterprise performance"""
        async with self.get_connection() as conn:
            # Use COPY for high-performance bulk insert
            await conn.copy_records_to_table(
                'memories',
                records=memories,
                columns=['id', 'content', 'timestamp', 'metadata', 'importance_score', 'embedding']
            )
            
            return len(memories)
    
    async def vector_similarity_search(self, query_embedding: list, limit: int = 10, threshold: float = 0.7) -> list:
        """Enterprise vector similarity search"""
        async with self.get_connection() as conn:
            # Optimized vector search with index usage
            result = await conn.fetch("""
                SELECT id, content, metadata, embedding <-> $1::vector as distance
                FROM memories 
                WHERE embedding <-> $1::vector < $2
                ORDER BY embedding <-> $1::vector
                LIMIT $3
            """, query_embedding, threshold, limit)
            
            return [dict(row) for row in result]
    
    async def get_enterprise_stats(self) -> Dict[str, Any]:
        """Get enterprise database statistics"""
        async with self.get_connection() as conn:
            stats = {}
            
            # Table sizes
            table_stats = await conn.fetch("""
                SELECT 
                    schemaname,
                    tablename,
                    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size,
                    pg_total_relation_size(schemaname||'.'||tablename) as size_bytes
                FROM pg_tables 
                WHERE schemaname = 'public'
                ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
            """)
            
            stats['table_sizes'] = [dict(row) for row in table_stats]
            
            # Database size
            db_size = await conn.fetchval("""
                SELECT pg_size_pretty(pg_database_size($1))
            """, self.database_name)
            
            stats['database_size'] = db_size
            
            # Connection stats
            connection_stats = await conn.fetchrow("""
                SELECT 
                    count(*) as total_connections,
                    count(*) FILTER (WHERE state = 'active') as active_connections,
                    count(*) FILTER (WHERE state = 'idle') as idle_connections
                FROM pg_stat_activity
                WHERE datname = $1
            """, self.database_name)
            
            stats['connections'] = dict(connection_stats)
            
            # Memory usage
            memory_stats = await conn.fetchrow("""
                SELECT 
                    pg_size_pretty(sum(heap_blks_hit) * 8192) as buffer_cache_hit_size,
                    round(100.0 * sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)), 2) as cache_hit_ratio
                FROM pg_statio_user_tables
            """)
            
            if memory_stats:
                stats['memory'] = dict(memory_stats)
            
            return stats
    
    async def close(self):
        """Close enterprise connections"""
        if self.connection_pool:
            await self.connection_pool.close()
        
        if self.engine:
            await self.engine.dispose()
        
        if self.connector:
            await self.connector.close()
        
        print("🔒 Enterprise AlloyDB connections closed")

# Global enterprise connector instance
enterprise_connector = SophiaEnterpriseAlloyDBConnector()

async def get_enterprise_connector() -> SophiaEnterpriseAlloyDBConnector:
    """Get the global enterprise connector instance"""
    if not enterprise_connector.connection_pool:
        await enterprise_connector.initialize_enterprise_connection()
    
    return enterprise_connector
