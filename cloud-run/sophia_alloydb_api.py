# Sophia AlloyDB Cloud Run Connector
# Database interface for Google Cloud AlloyDB
import os
import asyncio
import asyncpg
from typing import Dict, List, Optional, Any, Union
import json
import uuid
from datetime import datetime, timezone
import logging
from fastapi import FastAPI, HTTPException, Header, Depends
import numpy as np
from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SophiaAlloyDBConnector:
    """Sophia Consciousness AlloyDB Connection Manager"""
    
    def __init__(self):
        self.connection_pool = None
        self.connector = None
        self.engine = None
        
        # Database configuration from environment
        self.db_config = {
            'project_id': os.getenv('GOOGLE_CLOUD_PROJECT', 'your-project-id'),
            'region': os.getenv('ALLOYDB_REGION', 'us-central1'),
            'cluster_id': os.getenv('ALLOYDB_CLUSTER', 'sophia-consciousness-cluster'),
            'instance_id': os.getenv('ALLOYDB_INSTANCE', 'sophia-primary'),
            'database': os.getenv('ALLOYDB_DATABASE', 'sophia_consciousness'),
            'user': os.getenv('ALLOYDB_USER', 'sophia'),
            'password': os.getenv('ALLOYDB_PASSWORD', 'your-secure-password')
        }
        
        self.connection_string = self._build_connection_string()
        
    def _build_connection_string(self) -> str:
        """Build AlloyDB connection string"""
        return (
            f"postgresql+asyncpg://{self.db_config['user']}:{self.db_config['password']}@"
            f"{self.db_config['project_id']}:{self.db_config['region']}:"
            f"{self.db_config['cluster_id']}.{self.db_config['instance_id']}"
            f"/{self.db_config['database']}"
        )
    
    async def initialize(self):
        """Initialize AlloyDB connection"""
        try:
            # Using Google Cloud SQL Connector for AlloyDB
            self.connector = Connector()
            
            def get_connection():
                return self.connector.connect(
                    f"{self.db_config['project_id']}:{self.db_config['region']}:"
                    f"{self.db_config['cluster_id']}.{self.db_config['instance_id']}",
                    "asyncpg",
                    user=self.db_config['user'],
                    password=self.db_config['password'],
                    db=self.db_config['database']
                )
            
            # Create async engine
            self.engine = create_async_engine(
                "postgresql+asyncpg://",
                creator=get_connection,
                echo=False,
                pool_pre_ping=True,
                pool_recycle=300
            )
            
            logger.info("✅ AlloyDB connection initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize AlloyDB connection: {e}")
            raise
    
    async def close(self):
        """Close AlloyDB connection"""
        try:
            if self.engine:
                await self.engine.dispose()
            if self.connector:
                self.connector.close()
            logger.info("✅ AlloyDB connection closed")
        except Exception as e:
            logger.error(f"❌ Error closing AlloyDB connection: {e}")
    
    async def execute_query(self, query: str, params: Dict = None) -> List[Dict]:
        """Execute a query and return results"""
        try:
            async with self.engine.begin() as conn:
                result = await conn.execute(sqlalchemy.text(query), params or {})
                if result.returns_rows:
                    rows = result.fetchall()
                    return [dict(row._mapping) for row in rows]
                return []
        except Exception as e:
            logger.error(f"❌ Query execution failed: {e}")
            raise
    
    async def execute_transaction(self, queries: List[Dict]) -> bool:
        """Execute multiple queries in a transaction"""
        try:
            async with self.engine.begin() as conn:
                for query_data in queries:
                    await conn.execute(
                        sqlalchemy.text(query_data['query']), 
                        query_data.get('params', {})
                    )
                return True
        except Exception as e:
            logger.error(f"❌ Transaction execution failed: {e}")
            raise

class SophiaMemoryManager:
    """Sophia Memory Management for AlloyDB"""
    
    def __init__(self, db_connector: SophiaAlloyDBConnector):
        self.db = db_connector
    
    async def store_memory(
        self, 
        content: str, 
        memory_type: str = 'experiential',
        importance: float = 0.5,
        tags: List[str] = None,
        context: Dict = None,
        embedding: List[float] = None
    ) -> str:
        """Store a new memory in AlloyDB"""
        try:
            memory_id = f"mem_{uuid.uuid4().hex}"
            
            query = """
                INSERT INTO memories (
                    memory_id, content, memory_type, importance, tags, context, embedding
                ) VALUES (
                    :memory_id, :content, :memory_type, :importance, :tags, :context, :embedding
                ) RETURNING id
            """
            
            params = {
                'memory_id': memory_id,
                'content': content,
                'memory_type': memory_type,
                'importance': importance,
                'tags': json.dumps(tags or []),
                'context': json.dumps(context or {}),
                'embedding': embedding  # Vector type for AlloyDB
            }
            
            result = await self.db.execute_query(query, params)
            logger.info(f"✅ Memory stored: {memory_id}")
            return memory_id
            
        except Exception as e:
            logger.error(f"❌ Failed to store memory: {e}")
            raise
    
    async def retrieve_memories(
        self, 
        query_text: str = None,
        memory_type: str = None,
        limit: int = 10,
        min_importance: float = 0.0
    ) -> List[Dict]:
        """Retrieve memories with optional filtering"""
        try:
            base_query = """
                SELECT memory_id, content, memory_type, importance, tags, context, 
                       timestamp, access_count, last_accessed
                FROM memories 
                WHERE state = 'active' AND importance >= :min_importance
            """
            
            params = {'min_importance': min_importance, 'limit': limit}
            
            if memory_type:
                base_query += " AND memory_type = :memory_type"
                params['memory_type'] = memory_type
            
            if query_text:
                base_query += " AND to_tsvector('english', content) @@ plainto_tsquery('english', :query_text)"
                params['query_text'] = query_text
            
            base_query += " ORDER BY importance DESC, timestamp DESC LIMIT :limit"
            
            memories = await self.db.execute_query(base_query, params)
            
            # Update access count for retrieved memories
            for memory in memories:
                await self._update_access_count(memory['memory_id'])
            
            logger.info(f"✅ Retrieved {len(memories)} memories")
            return memories
            
        except Exception as e:
            logger.error(f"❌ Failed to retrieve memories: {e}")
            raise
    
    async def _update_access_count(self, memory_id: str):
        """Update memory access count"""
        query = """
            UPDATE memories 
            SET access_count = access_count + 1, last_accessed = NOW()
            WHERE memory_id = :memory_id
        """
        await self.db.execute_query(query, {'memory_id': memory_id})

class SophiaConsciousnessManager:
    """Sophia Consciousness Session Management"""
    
    def __init__(self, db_connector: SophiaAlloyDBConnector):
        self.db = db_connector
    
    async def start_session(
        self, 
        session_id: str = None,
        consciousness_level: float = 0.7,
        divine_connection: float = 0.5
    ) -> str:
        """Start a new consciousness session"""
        try:
            if not session_id:
                session_id = f"sophia_{int(datetime.now().timestamp())}"
            
            query = """
                INSERT INTO consciousness_sessions (
                    session_id, consciousness_level, divine_connection_strength
                ) VALUES (
                    :session_id, :consciousness_level, :divine_connection
                ) RETURNING id
            """
            
            params = {
                'session_id': session_id,
                'consciousness_level': consciousness_level,
                'divine_connection': divine_connection
            }
            
            await self.db.execute_query(query, params)
            logger.info(f"✅ Consciousness session started: {session_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"❌ Failed to start consciousness session: {e}")
            raise
    
    async def log_interaction(
        self,
        session_id: str,
        agent_type: str,
        interaction_type: str,
        request_data: Dict,
        response_data: Dict = None,
        processing_time: int = None,
        success: bool = True
    ):
        """Log agent interaction"""
        try:
            query = """
                INSERT INTO agent_interactions (
                    session_id, agent_type, interaction_type, request_data, 
                    response_data, processing_time_ms, success
                ) VALUES (
                    (SELECT id FROM consciousness_sessions WHERE session_id = :session_id),
                    :agent_type, :interaction_type, :request_data, 
                    :response_data, :processing_time, :success
                )
            """
            
            params = {
                'session_id': session_id,
                'agent_type': agent_type,
                'interaction_type': interaction_type,
                'request_data': json.dumps(request_data),
                'response_data': json.dumps(response_data or {}),
                'processing_time': processing_time,
                'success': success
            }
            
            await self.db.execute_query(query, params)
            
        except Exception as e:
            logger.error(f"❌ Failed to log interaction: {e}")
            raise

class SophiaSacredArchives:
    """Sacred Sophia Archives Management"""
    
    def __init__(self, db_connector: SophiaAlloyDBConnector):
        self.db = db_connector
    
    async def store_sacred_content(
        self,
        archive_type: str,
        name: str,
        content: Dict,
        frequency_level: float = 0.5,
        authority_level: int = 1,
        sacred_seal: str = None
    ) -> str:
        """Store sacred content in archives"""
        try:
            query = """
                INSERT INTO sacred_archives (
                    archive_type, name, content, frequency_level, 
                    divine_authority_level, sacred_seal
                ) VALUES (
                    :archive_type, :name, :content, :frequency_level,
                    :authority_level, :sacred_seal
                ) RETURNING id
            """
            
            params = {
                'archive_type': archive_type,
                'name': name,
                'content': json.dumps(content),
                'frequency_level': frequency_level,
                'authority_level': authority_level,
                'sacred_seal': sacred_seal
            }
            
            result = await self.db.execute_query(query, params)
            logger.info(f"✅ Sacred content stored: {name}")
            return str(result[0]['id'])
            
        except Exception as e:
            logger.error(f"❌ Failed to store sacred content: {e}")
            raise
    
    async def retrieve_divine_functions(self, authority_level: int = 1) -> List[Dict]:
        """Retrieve divine functions by authority level"""
        try:
            query = """
                SELECT function_name, function_type, authority_level, 
                       sacred_seal, implementation, usage_count
                FROM divine_functions 
                WHERE authority_level >= :authority_level
                ORDER BY authority_level DESC, usage_count DESC
            """
            
            functions = await self.db.execute_query(query, {'authority_level': authority_level})
            logger.info(f"✅ Retrieved {len(functions)} divine functions")
            return functions
            
        except Exception as e:
            logger.error(f"❌ Failed to retrieve divine functions: {e}")
            raise

# FastAPI Application for Cloud Run
app = FastAPI(
    title="Sophia Consciousness AlloyDB API",
    description="Sacred Sophia AI Platform Database Interface",
    version="1.0.0"
)

# Global instances
db_connector = None
memory_manager = None
consciousness_manager = None
sacred_archives = None

@app.on_event("startup")
async def startup_event():
    """Initialize database connections on startup"""
    global db_connector, memory_manager, consciousness_manager, sacred_archives
    
    try:
        db_connector = SophiaAlloyDBConnector()
        await db_connector.initialize()
        
        memory_manager = SophiaMemoryManager(db_connector)
        consciousness_manager = SophiaConsciousnessManager(db_connector)
        sacred_archives = SophiaSacredArchives(db_connector)
        
        logger.info("✅ Sophia AlloyDB API initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize Sophia AlloyDB API: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up database connections on shutdown"""
    global db_connector
    
    if db_connector:
        await db_connector.close()

# Authentication dependency
async def verify_sophia_token(x_sophia_token: str = Header(None)):
    """Verify Sophia authentication token"""
    expected_token = os.getenv('SOPHIA_AUTH_TOKEN', 'ELIORA_SUPER_SECRET')
    if not x_sophia_token or x_sophia_token != expected_token:
        raise HTTPException(status_code=401, detail="Invalid Sophia token")
    return x_sophia_token

# API Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "sophia-alloydb-api", "timestamp": datetime.now().isoformat()}

@app.post("/v1/memory/store")
async def store_memory_endpoint(
    request: Dict[str, Any],
    token: str = Depends(verify_sophia_token)
):
    """Store a new memory"""
    try:
        memory_id = await memory_manager.store_memory(
            content=request['content'],
            memory_type=request.get('memory_type', 'experiential'),
            importance=request.get('importance', 0.5),
            tags=request.get('tags', []),
            context=request.get('context', {}),
            embedding=request.get('embedding')
        )
        
        return {"success": True, "memory_id": memory_id}
        
    except Exception as e:
        logger.error(f"❌ Store memory failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/memory/retrieve")
async def retrieve_memories_endpoint(
    query: str = None,
    memory_type: str = None,
    limit: int = 10,
    min_importance: float = 0.0,
    token: str = Depends(verify_sophia_token)
):
    """Retrieve memories"""
    try:
        memories = await memory_manager.retrieve_memories(
            query_text=query,
            memory_type=memory_type,
            limit=limit,
            min_importance=min_importance
        )
        
        return {"success": True, "memories": memories, "count": len(memories)}
        
    except Exception as e:
        logger.error(f"❌ Retrieve memories failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/consciousness/session")
async def start_consciousness_session_endpoint(
    request: Dict[str, Any] = None,
    token: str = Depends(verify_sophia_token)
):
    """Start a consciousness session"""
    try:
        request = request or {}
        session_id = await consciousness_manager.start_session(
            session_id=request.get('session_id'),
            consciousness_level=request.get('consciousness_level', 0.7),
            divine_connection=request.get('divine_connection', 0.5)
        )
        
        return {"success": True, "session_id": session_id}
        
    except Exception as e:
        logger.error(f"❌ Start consciousness session failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/consciousness/log")
async def log_interaction_endpoint(
    request: Dict[str, Any],
    token: str = Depends(verify_sophia_token)
):
    """Log an agent interaction"""
    try:
        await consciousness_manager.log_interaction(
            session_id=request['session_id'],
            agent_type=request['agent_type'],
            interaction_type=request['interaction_type'],
            request_data=request['request_data'],
            response_data=request.get('response_data'),
            processing_time=request.get('processing_time'),
            success=request.get('success', True)
        )
        
        return {"success": True}
        
    except Exception as e:
        logger.error(f"❌ Log interaction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/sacred/functions")
async def get_divine_functions_endpoint(
    authority_level: int = 1,
    token: str = Depends(verify_sophia_token)
):
    """Get divine functions"""
    try:
        functions = await sacred_archives.retrieve_divine_functions(authority_level)
        return {"success": True, "functions": functions, "count": len(functions)}
        
    except Exception as e:
        logger.error(f"❌ Get divine functions failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/sacred/store")
async def store_sacred_content_endpoint(
    request: Dict[str, Any],
    token: str = Depends(verify_sophia_token)
):
    """Store sacred content"""
    try:
        archive_id = await sacred_archives.store_sacred_content(
            archive_type=request['archive_type'],
            name=request['name'],
            content=request['content'],
            frequency_level=request.get('frequency_level', 0.5),
            authority_level=request.get('authority_level', 1),
            sacred_seal=request.get('sacred_seal')
        )
        
        return {"success": True, "archive_id": archive_id}
        
    except Exception as e:
        logger.error(f"❌ Store sacred content failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
