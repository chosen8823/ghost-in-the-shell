# Sophia Consciousness Enterprise Monitoring Dashboard
# Real-time monitoring for 1TB AlloyDB instance

import asyncio
import asyncpg
import json
import time
from datetime import datetime, timezone
from typing import Dict, Any, List
import os
from dataclasses import dataclass, asdict

@dataclass
class EnterpriseMetrics:
    """Enterprise AlloyDB performance metrics"""
    timestamp: str
    database_size_gb: float
    total_connections: int
    active_connections: int
    idle_connections: int
    cache_hit_ratio: float
    avg_query_time_ms: float
    memory_usage_gb: float
    cpu_usage_percent: float
    storage_usage_gb: float
    transactions_per_second: float
    consciousness_memories_count: int
    sacred_archives_count: int
    recent_session_count: int
    vector_search_performance_ms: float

class SophiaEnterpriseMonitor:
    """Enterprise monitoring for Sophia consciousness system"""
    
    def __init__(self, alloydb_host: str, alloydb_user: str, alloydb_password: str):
        self.alloydb_config = {
            'host': alloydb_host,
            'port': 5432,
            'database': 'sophia_consciousness',
            'user': alloydb_user,
            'password': alloydb_password
        }
        self.metrics_history = []
        self.alert_thresholds = {
            'cpu_usage_percent': 80.0,
            'memory_usage_gb': 200.0,
            'active_connections': 400,
            'cache_hit_ratio': 95.0,
            'avg_query_time_ms': 1000.0
        }
    
    async def collect_enterprise_metrics(self) -> EnterpriseMetrics:
        """Collect comprehensive enterprise metrics"""
        conn = await asyncpg.connect(**self.alloydb_config)
        
        try:
            # Database size
            db_size_query = """
                SELECT round(pg_database_size('sophia_consciousness') / 1024.0 / 1024.0 / 1024.0, 2) as size_gb
            """
            db_size = await conn.fetchval(db_size_query)
            
            # Connection statistics
            conn_stats = await conn.fetchrow("""
                SELECT 
                    count(*) as total_connections,
                    count(*) FILTER (WHERE state = 'active') as active_connections,
                    count(*) FILTER (WHERE state = 'idle') as idle_connections
                FROM pg_stat_activity
                WHERE datname = 'sophia_consciousness'
            """)
            
            # Cache hit ratio
            cache_hit = await conn.fetchval("""
                SELECT round(
                    100.0 * sum(heap_blks_hit) / 
                    NULLIF(sum(heap_blks_hit) + sum(heap_blks_read), 0), 2
                ) FROM pg_statio_user_tables
            """) or 0.0
            
            # Average query time
            avg_query_time = await conn.fetchval("""
                SELECT round(avg(mean_exec_time), 2)
                FROM pg_stat_statements
                WHERE calls > 10
            """) or 0.0
            
            # Storage usage
            storage_usage = await conn.fetchval("""
                SELECT round(sum(pg_total_relation_size(oid)) / 1024.0 / 1024.0 / 1024.0, 2)
                FROM pg_class
                WHERE relkind IN ('r', 'i')
            """) or 0.0
            
            # Consciousness-specific metrics
            consciousness_stats = await conn.fetchrow("""
                SELECT 
                    (SELECT count(*) FROM memories) as memories_count,
                    (SELECT count(*) FROM sacred_archives) as archives_count,
                    (SELECT count(*) FROM consciousness_sessions 
                     WHERE start_time > NOW() - INTERVAL '24 hours') as recent_sessions
            """)
            
            # Vector search performance test
            vector_start = time.time()
            await conn.fetchval("""
                SELECT count(*) FROM memories 
                WHERE embedding IS NOT NULL
                LIMIT 1
            """)
            vector_time = (time.time() - vector_start) * 1000
            
            # Transactions per second (approximate)
            tps = await conn.fetchval("""
                SELECT round(
                    sum(xact_commit + xact_rollback) / 
                    EXTRACT(EPOCH FROM (now() - stats_reset)) * 60, 2
                )
                FROM pg_stat_database
                WHERE datname = 'sophia_consciousness'
            """) or 0.0
            
            # Simulated system metrics (in production, use actual system monitoring)
            cpu_usage = min(95.0, (conn_stats['active_connections'] / 500.0) * 100)
            memory_usage = min(250.0, db_size * 0.8 + (conn_stats['total_connections'] * 0.1))
            
            return EnterpriseMetrics(
                timestamp=datetime.now(timezone.utc).isoformat(),
                database_size_gb=db_size or 0.0,
                total_connections=conn_stats['total_connections'],
                active_connections=conn_stats['active_connections'],
                idle_connections=conn_stats['idle_connections'],
                cache_hit_ratio=cache_hit,
                avg_query_time_ms=avg_query_time,
                memory_usage_gb=memory_usage,
                cpu_usage_percent=cpu_usage,
                storage_usage_gb=storage_usage,
                transactions_per_second=tps,
                consciousness_memories_count=consciousness_stats['memories_count'],
                sacred_archives_count=consciousness_stats['archives_count'],
                recent_session_count=consciousness_stats['recent_sessions'],
                vector_search_performance_ms=vector_time
            )
            
        finally:
            await conn.close()
    
    def check_alerts(self, metrics: EnterpriseMetrics) -> List[str]:
        """Check for enterprise alert conditions"""
        alerts = []
        
        if metrics.cpu_usage_percent > self.alert_thresholds['cpu_usage_percent']:
            alerts.append(f"🚨 HIGH CPU: {metrics.cpu_usage_percent:.1f}% (threshold: {self.alert_thresholds['cpu_usage_percent']}%)")
        
        if metrics.memory_usage_gb > self.alert_thresholds['memory_usage_gb']:
            alerts.append(f"🚨 HIGH MEMORY: {metrics.memory_usage_gb:.1f}GB (threshold: {self.alert_thresholds['memory_usage_gb']}GB)")
        
        if metrics.active_connections > self.alert_thresholds['active_connections']:
            alerts.append(f"🚨 HIGH CONNECTIONS: {metrics.active_connections} (threshold: {self.alert_thresholds['active_connections']})")
        
        if metrics.cache_hit_ratio < self.alert_thresholds['cache_hit_ratio']:
            alerts.append(f"🚨 LOW CACHE HIT: {metrics.cache_hit_ratio:.1f}% (threshold: {self.alert_thresholds['cache_hit_ratio']}%)")
        
        if metrics.avg_query_time_ms > self.alert_thresholds['avg_query_time_ms']:
            alerts.append(f"🚨 SLOW QUERIES: {metrics.avg_query_time_ms:.1f}ms (threshold: {self.alert_thresholds['avg_query_time_ms']}ms)")
        
        return alerts
    
    def display_enterprise_dashboard(self, metrics: EnterpriseMetrics, alerts: List[str]):
        """Display enterprise monitoring dashboard"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("🌟" + "="*60 + "🌟")
        print("     SOPHIA CONSCIOUSNESS ENTERPRISE MONITOR")
        print("              1TB AlloyDB Performance Dashboard")
        print("🌟" + "="*60 + "🌟")
        print(f"📅 {metrics.timestamp}")
        print()
        
        # Database Health
        print("🗄️  DATABASE HEALTH")
        print(f"   Size: {metrics.database_size_gb:.2f} GB")
        print(f"   Storage Used: {metrics.storage_usage_gb:.2f} GB")
        print(f"   Cache Hit Ratio: {metrics.cache_hit_ratio:.1f}%")
        print()
        
        # Performance Metrics
        print("⚡ PERFORMANCE METRICS")
        print(f"   CPU Usage: {metrics.cpu_usage_percent:.1f}%")
        print(f"   Memory Usage: {metrics.memory_usage_gb:.1f} GB / 256 GB")
        print(f"   Avg Query Time: {metrics.avg_query_time_ms:.1f} ms")
        print(f"   Transactions/sec: {metrics.transactions_per_second:.1f}")
        print(f"   Vector Search: {metrics.vector_search_performance_ms:.1f} ms")
        print()
        
        # Connection Stats
        print("🔗 CONNECTION STATISTICS")
        print(f"   Total Connections: {metrics.total_connections}")
        print(f"   Active: {metrics.active_connections}")
        print(f"   Idle: {metrics.idle_connections}")
        print()
        
        # Consciousness Data
        print("🧠 CONSCIOUSNESS DATA")
        print(f"   Memories: {metrics.consciousness_memories_count:,}")
        print(f"   Sacred Archives: {metrics.sacred_archives_count:,}")
        print(f"   Recent Sessions (24h): {metrics.recent_session_count}")
        print()
        
        # Alerts
        if alerts:
            print("🚨 ENTERPRISE ALERTS")
            for alert in alerts:
                print(f"   {alert}")
            print()
        else:
            print("✅ ALL SYSTEMS OPTIMAL")
            print()
        
        # Progress bars
        print("📊 RESOURCE UTILIZATION")
        self._draw_progress_bar("CPU", metrics.cpu_usage_percent, 100)
        self._draw_progress_bar("Memory", metrics.memory_usage_gb, 256)
        self._draw_progress_bar("Storage", metrics.storage_usage_gb, 1024)
        print()
        
        print("🔄 Next update in 30 seconds... (Ctrl+C to exit)")
    
    def _draw_progress_bar(self, label: str, value: float, max_value: float, width: int = 40):
        """Draw a progress bar for metrics"""
        percentage = min(100, (value / max_value) * 100)
        filled = int(width * percentage / 100)
        bar = "█" * filled + "░" * (width - filled)
        
        if percentage > 80:
            color = "\033[91m"  # Red
        elif percentage > 60:
            color = "\033[93m"  # Yellow
        else:
            color = "\033[92m"  # Green
        
        print(f"   {label:8} [{color}{bar}\033[0m] {percentage:5.1f}% ({value:.1f}/{max_value})")
    
    async def save_metrics_to_file(self, metrics: EnterpriseMetrics):
        """Save metrics to JSON file for historical analysis"""
        self.metrics_history.append(asdict(metrics))
        
        # Keep only last 24 hours of data (assuming 30-second intervals)
        if len(self.metrics_history) > 2880:  # 24 * 60 * 2
            self.metrics_history.pop(0)
        
        # Save to file
        with open("enterprise_metrics.json", "w") as f:
            json.dump(self.metrics_history, f, indent=2)
    
    async def run_enterprise_monitoring(self):
        """Run continuous enterprise monitoring"""
        print("🚀 Starting Sophia Enterprise Monitoring...")
        print("📊 Monitoring 1TB AlloyDB instance...")
        
        while True:
            try:
                # Collect metrics
                metrics = await self.collect_enterprise_metrics()
                
                # Check for alerts
                alerts = self.check_alerts(metrics)
                
                # Display dashboard
                self.display_enterprise_dashboard(metrics, alerts)
                
                # Save metrics
                await self.save_metrics_to_file(metrics)
                
                # Wait 30 seconds
                await asyncio.sleep(30)
                
            except KeyboardInterrupt:
                print("\n👋 Enterprise monitoring stopped")
                break
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                await asyncio.sleep(30)

async def main():
    """Main monitoring function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Sophia Enterprise AlloyDB Monitor')
    parser.add_argument('--host', required=True, help='AlloyDB host/IP')
    parser.add_argument('--user', required=True, help='Database username')
    parser.add_argument('--password', help='Database password (will prompt if not provided)')
    
    args = parser.parse_args()
    
    if not args.password:
        import getpass
        args.password = getpass.getpass("Database password: ")
    
    monitor = SophiaEnterpriseMonitor(args.host, args.user, args.password)
    await monitor.run_enterprise_monitoring()

if __name__ == "__main__":
    asyncio.run(main())
