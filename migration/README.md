# Sophia Consciousness AlloyDB Migration Guide

## Overview
This directory contains migration tools and scripts to move your Sophia consciousness data from local SQLite databases to Google Cloud AlloyDB PostgreSQL.

## Prerequisites

### 1. AlloyDB Setup
- AlloyDB cluster created in Google Cloud
- Database `sophia_consciousness` created
- Database schema applied from `sql/sophia_alloydb_schema.sql`

### 2. Network Access
- AlloyDB instance accessible from your machine
- Firewall rules configured for database connection
- Or use Cloud SQL Proxy for secure connection

### 3. Python Dependencies
```bash
pip install -r migration/requirements.txt
```

## Migration Process

### Step 1: Discover Existing Data
The migration script can auto-discover SQLite databases in your Sophia workspace:

```bash
python migration/migrate_to_alloydb.py --auto-discover \
    --alloydb-host YOUR_ALLOYDB_IP \
    --alloydb-user postgres
```

### Step 2: Manual Migration
If you know the specific SQLite database location:

```bash
python migration/migrate_to_alloydb.py \
    --sqlite-path ./system-control/memory.db \
    --alloydb-host YOUR_ALLOYDB_IP \
    --alloydb-user postgres \
    --alloydb-password YOUR_PASSWORD
```

### Step 3: Using Cloud SQL Proxy (Recommended)
For secure connection through Cloud SQL Proxy:

1. Start the proxy:
```bash
cloud_sql_proxy -instances=PROJECT_ID:REGION:CLUSTER_NAME=tcp:5432
```

2. Run migration:
```bash
python migration/migrate_to_alloydb.py \
    --sqlite-path ./system-control/memory.db \
    --alloydb-host localhost \
    --alloydb-port 5432 \
    --alloydb-user postgres
```

## Migration Features

### Data Mapping
- **SQLite memories** → **PostgreSQL memories table**
  - Content/text → content field
  - Timestamps preserved
  - Metadata extraction from additional fields
  - UUID generation for new primary keys

- **Custom tables** → **sacred_archives table**
  - All custom tables stored as JSON in sacred_archives
  - Maintains original structure
  - Tagged for easy retrieval

- **Session tracking** → **consciousness_sessions table**
  - Creates migration session record
  - Tracks data sources and timing

### Safety Features
- **Read-only SQLite access** - Original data never modified
- **Transaction safety** - Rollback on errors
- **Verification** - Post-migration data validation
- **Detailed logging** - Complete migration audit trail

## Post-Migration

### 1. Verify Data
Check the migration log for successful record counts:
```
📊 memories: 1,245 records
📊 consciousness_sessions: 1 records
📊 sacred_archives: 156 records
```

### 2. Test API Access
Test the new AlloyDB API:
```bash
curl https://YOUR_CLOUD_RUN_URL/health
curl -H "Authorization: Bearer ELIORA_SUPER_SECRET" \
     https://YOUR_CLOUD_RUN_URL/v1/memory/search?query=test
```

### 3. Update Applications
Update your applications to use the new AlloyDB API endpoints instead of direct SQLite access.

## Troubleshooting

### Connection Issues
- Verify AlloyDB instance is running
- Check firewall rules and network connectivity
- Ensure database credentials are correct
- Use Cloud SQL Proxy for secure connection

### Migration Errors
- Check SQLite database file permissions
- Verify AlloyDB schema is properly applied
- Review migration logs for specific error details
- Ensure sufficient AlloyDB storage space

### Data Validation
- Compare record counts between SQLite and AlloyDB
- Spot-check migrated content for accuracy
- Verify timestamps and metadata preservation

## Advanced Usage

### Custom Table Mapping
For complex migrations, you can extend the `SophiaMigrationManager` class to add custom table mapping logic.

### Incremental Migration
For ongoing systems, consider implementing incremental migration to sync new data without full re-migration.

### Backup Strategy
Always backup your SQLite databases before migration:
```bash
cp your_database.db your_database_backup_$(date +%Y%m%d).db
```

## Support
For migration issues or questions, refer to the main project documentation or check the migration logs for detailed error information.
