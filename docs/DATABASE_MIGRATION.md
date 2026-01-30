# Database Migration Guide

Complete guide for migrating from SQLite to PostgreSQL and managing database schema changes with Alembic.

## Table of Contents

1. [Why Migrate to PostgreSQL?](#why-migrate-to-postgresql)
2. [Prerequisites](#prerequisites)
3. [Setting Up Alembic](#setting-up-alembic)
4. [Migration Strategy](#migration-strategy)
5. [Step-by-Step Migration](#step-by-step-migration)
6. [Rollback Procedures](#rollback-procedures)
7. [Production Deployment](#production-deployment)

---

## Why Migrate to PostgreSQL?

### SQLite Limitations for Production

- **Concurrency:** Limited write concurrency (single writer lock)
- **Scalability:** Not suitable for high-traffic applications
- **Features:** Lacks advanced features (full-text search, JSON operators, etc.)
- **Connections:** No connection pooling support

### PostgreSQL Benefits

- **Concurrency:** MVCC for excellent read/write performance
- **Reliability:** ACID-compliant with robust backup/recovery
- **Features:** Rich data types, full-text search, JSON support
- **Extensions:** PostGIS, pg_trgm, and many others
- **Monitoring:** Built-in statistics and query analysis

---

## Prerequisites

### Software Requirements

```bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Or via Docker
docker run --name osrs-postgres \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=osrs_tool_hub \
  -p 5432:5432 \
  -d postgres:16
```

### Python Dependencies

Add to `pyproject.toml`:

```toml
[tool.poetry.dependencies]
psycopg2-binary = "^2.9.9"
alembic = "^1.13.1"

[tool.poetry.group.dev.dependencies]
pgcli = "^4.0.1"  # Optional: Better PostgreSQL CLI
```

Install:

```bash
poetry install
```

---

## Setting Up Alembic

### 1. Initialize Alembic

```bash
# From project root
poetry run alembic init alembic
```

This creates:
```
alembic/
├── env.py           # Migration environment configuration
├── script.py.mako   # Migration script template
├── README
└── versions/        # Migration version files
alembic.ini          # Alembic configuration
```

### 2. Configure Alembic

Edit `alembic.ini`:

```ini
# Comment out the default sqlalchemy.url
# sqlalchemy.url = driver://user:pass@localhost/dbname

# We'll set this dynamically from config.py
```

Edit `alembic/env.py`:

```python
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from backend.config import get_settings
from backend.db.base import Base  # Import all models
from backend.models import *  # Import all models to register with Base

config = context.config
settings = get_settings()

# Set the database URL from settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode (async)."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### 3. Create Initial Migration

```bash
# Generate migration from current models
poetry run alembic revision --autogenerate -m "Initial schema"

# Review the generated migration in alembic/versions/
# Edit if necessary

# Apply the migration
poetry run alembic upgrade head
```

---

## Migration Strategy

### Zero-Downtime Migration (Recommended for Production)

1. **Dual-Write Phase**
   - Write to both SQLite and PostgreSQL
   - Read from SQLite (current production)
   - Duration: 1-2 weeks

2. **Validation Phase**
   - Compare data between databases
   - Run parallel testing
   - Duration: 1 week

3. **Switch Phase**
   - Enable read from PostgreSQL
   - Monitor for issues
   - Keep SQLite as backup
   - Duration: 1 week

4. **Cleanup Phase**
   - Remove dual-write logic
   - Decommission SQLite

### Simple Migration (Development/Small Apps)

1. Export data from SQLite
2. Create PostgreSQL schema
3. Import data to PostgreSQL
4. Update configuration
5. Test and deploy

---

## Step-by-Step Migration

### Step 1: Set Up PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE osrs_tool_hub;
CREATE USER osrs_user WITH ENCRYPTED PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE osrs_tool_hub TO osrs_user;
\c osrs_tool_hub
GRANT ALL ON SCHEMA public TO osrs_user;
\q
```

### Step 2: Export SQLite Data

Create `scripts/export_sqlite.py`:

```python
import sqlite3
import json
from pathlib import Path

def export_table(conn, table_name):
    """Export table to JSON."""
    cursor = conn.execute(f"SELECT * FROM {table_name}")
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    
    data = [dict(zip(columns, row)) for row in rows]
    
    output_file = Path(f"data_export/{table_name}.json")
    output_file.parent.mkdir(exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    
    print(f"Exported {len(data)} rows from {table_name}")

def main():
    conn = sqlite3.connect("osrs_tool_hub.db")
    
    # Get all table names
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    )
    tables = [row[0] for row in cursor.fetchall()]
    
    for table in tables:
        export_table(conn, table)
    
    conn.close()
    print("\nExport complete!")

if __name__ == "__main__":
    main()
```

Run export:

```bash
poetry run python scripts/export_sqlite.py
```

### Step 3: Update Configuration

Update `backend/config.py`:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Change default from SQLite to PostgreSQL
    DATABASE_URL: str = (
        "postgresql+asyncpg://osrs_user:secure_password@localhost:5432/osrs_tool_hub"
    )
    
    # For development, you can still use SQLite
    # DATABASE_URL: str = "sqlite+aiosqlite:///./osrs_tool_hub.db"
    
    class Config:
        env_file = ".env"
```

Update `.env`:

```bash
# PostgreSQL (Production)
DATABASE_URL=postgresql+asyncpg://osrs_user:secure_password@localhost:5432/osrs_tool_hub

# SQLite (Development)
# DATABASE_URL=sqlite+aiosqlite:///./osrs_tool_hub.db
```

### Step 4: Create PostgreSQL Schema

```bash
# Apply all migrations
poetry run alembic upgrade head

# Verify tables were created
psql -U osrs_user -d osrs_tool_hub -c "\dt"
```

### Step 5: Import Data

Create `scripts/import_postgres.py`:

```python
import asyncio
import json
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from backend.config import get_settings
from backend.models import *

async def import_table(session: AsyncSession, model_class, data_file: Path):
    """Import data from JSON to PostgreSQL."""
    with open(data_file) as f:
        records = json.load(f)
    
    for record in records:
        instance = model_class(**record)
        session.add(instance)
    
    await session.commit()
    print(f"Imported {len(records)} records to {model_class.__tablename__}")

async def main():
    settings = get_settings()
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        # Import in correct order (respecting foreign keys)
        await import_table(session, Item, Path("data_export/items.json"))
        await import_table(session, Trade, Path("data_export/trades.json"))
        await import_table(session, Watchlist, Path("data_export/watchlist.json"))
        # Add more tables as needed
    
    await engine.dispose()
    print("\nImport complete!")

if __name__ == "__main__":
    asyncio.run(main())
```

Run import:

```bash
poetry run python scripts/import_postgres.py
```

### Step 6: Verify Migration

```bash
# Check row counts
psql -U osrs_user -d osrs_tool_hub << EOF
SELECT 'items' as table_name, COUNT(*) FROM items
UNION ALL
SELECT 'trades', COUNT(*) FROM trades
UNION ALL
SELECT 'watchlist', COUNT(*) FROM watchlist;
EOF

# Compare with SQLite counts
sqlite3 osrs_tool_hub.db << EOF
SELECT 'items', COUNT(*) FROM items
UNION ALL
SELECT 'trades', COUNT(*) FROM trades
UNION ALL
SELECT 'watchlist', COUNT(*) FROM watchlist;
EOF
```

### Step 7: Test Application

```bash
# Start with PostgreSQL
poetry run uvicorn backend.main:app --reload

# Run test suite
poetry run pytest backend/tests/

# Check API endpoints
curl http://localhost:8000/api/v1/health
```

---

## Managing Schema Changes

### Creating New Migrations

```bash
# After modifying models
poetry run alembic revision --autogenerate -m "Add new column to trades"

# Review and edit the generated migration
vim alembic/versions/xxxx_add_new_column_to_trades.py

# Apply migration
poetry run alembic upgrade head
```

### Migration Best Practices

1. **Always review autogenerated migrations**
2. **Test on development database first**
3. **Add data migrations if needed**
4. **Include both upgrade() and downgrade()**
5. **Document complex migrations**

---

## Rollback Procedures

### Rolling Back Migrations

```bash
# Rollback one migration
poetry run alembic downgrade -1

# Rollback to specific revision
poetry run alembic downgrade <revision_id>

# Rollback all migrations
poetry run alembic downgrade base
```

### Emergency Database Rollback

If issues occur in production:

1. **Keep SQLite backup during migration period**
2. **Update .env to point back to SQLite**
3. **Restart application**
4. **Investigate issues**

```bash
# Switch back to SQLite
DATABASE_URL=sqlite+aiosqlite:///./osrs_tool_hub.db

# Restart
sudo systemctl restart osrs-tool-hub
```

---

## Production Deployment

### Pre-Deployment Checklist

- [ ] PostgreSQL installed and configured
- [ ] Database backups automated
- [ ] Connection pooling configured
- [ ] Migrations tested on staging
- [ ] Monitoring alerts set up
- [ ] Rollback plan documented
- [ ] Team notified of maintenance window

### Deployment Steps

```bash
# 1. Backup SQLite database
cp osrs_tool_hub.db osrs_tool_hub.db.backup

# 2. Export data
poetry run python scripts/export_sqlite.py

# 3. Create PostgreSQL schema
poetry run alembic upgrade head

# 4. Import data
poetry run python scripts/import_postgres.py

# 5. Update environment
vi .env  # Update DATABASE_URL

# 6. Restart application
sudo systemctl restart osrs-tool-hub

# 7. Verify
curl http://localhost:8000/api/v1/health
poetry run pytest backend/tests/e2e/
```

### Post-Deployment Monitoring

```bash
# Monitor PostgreSQL performance
psql -U osrs_user -d osrs_tool_hub -c "
  SELECT query, calls, total_time, mean_time 
  FROM pg_stat_statements 
  ORDER BY total_time DESC 
  LIMIT 10;
"

# Check slow queries
psql -U osrs_user -d osrs_tool_hub -c "
  SELECT pid, now() - pg_stat_activity.query_start AS duration, query 
  FROM pg_stat_activity 
  WHERE state = 'active' AND now() - pg_stat_activity.query_start > interval '5 seconds';
"
```

---

## Performance Optimization

### Connection Pooling

Update `backend/db/session.py`:

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=20,          # Connection pool size
    max_overflow=10,       # Additional connections when pool is full
    pool_pre_ping=True,    # Verify connections before using
    pool_recycle=3600,     # Recycle connections after 1 hour
    echo=False,            # Set to True for SQL logging
)
```

### Indexes

Add indexes for common queries:

```bash
poetry run alembic revision -m "Add performance indexes"
```

In the migration file:

```python
def upgrade():
    op.create_index('ix_trades_item_id', 'trades', ['item_id'])
    op.create_index('ix_trades_timestamp', 'trades', ['timestamp'])
    op.create_index('ix_items_name', 'items', ['name'])

def downgrade():
    op.drop_index('ix_trades_item_id')
    op.drop_index('ix_trades_timestamp')
    op.drop_index('ix_items_name')
```

---

## Troubleshooting

### Common Issues

**Issue:** "password authentication failed"
```bash
# Check pg_hba.conf authentication method
sudo vi /etc/postgresql/16/main/pg_hba.conf
# Change 'peer' to 'md5' for local connections
sudo systemctl restart postgresql
```

**Issue:** "connection refused"
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check listening address
sudo netstat -plunt | grep 5432
```

**Issue:** "too many connections"
```bash
# Increase max_connections in postgresql.conf
sudo vi /etc/postgresql/16/main/postgresql.conf
# max_connections = 200
sudo systemctl restart postgresql
```

---

## Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Async Documentation](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [PostgreSQL Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)
