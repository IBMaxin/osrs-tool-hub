# Database Seeding Guide

## Overview

This directory contains scripts to populate the database with initial OSRS data.

## Slayer Data

### What Gets Seeded

- **50+ Monsters** with accurate stats from OSRS Wiki
- **40+ Tasks for Duradel** (high-level slayer master)
- **43+ Tasks for Nieve/Steve** (mid-high level slayer master)
- **18+ Tasks for Konar** (location-specific master)

### How to Reseed

#### Option 1: Run the seed script directly

```bash
# From project root
poetry run python -m backend.seeds.slayer.seed
```

#### Option 2: Using Python directly (if poetry isn't working)

```bash
# From project root
python -m backend.seeds.slayer.seed
```

#### Option 3: Reset database and reseed

```bash
# Delete the database file
rm backend/slayer.db

# Run the seed script (it will create tables automatically)
poetry run python -m backend.seeds.slayer.seed
```

### Verification

After seeding, verify the data:

```bash
# Check that database was created
ls backend/slayer.db

# Start the backend
poetry run uvicorn backend.main:app --reload

# Test endpoints
curl http://localhost:8000/api/v1/slayer/masters
curl http://localhost:8000/api/v1/slayer/tasks/Duradel
curl http://localhost:8000/api/v1/slayer/tasks/Nieve
```

You should now see:
- **Duradel**: ~40 tasks
- **Nieve**: ~43 tasks
- All missing monsters included (Fire giants, Black demons, etc.)

### Troubleshooting

**Problem**: `ModuleNotFoundError`
```bash
# Make sure you're in the project root and using poetry
cd /path/to/osrs-tool-hub
poetry install
poetry run python -m backend.seeds.slayer.seed
```

**Problem**: Duplicate tasks warning
```
✓ This is normal - the script skips existing tasks
✓ Delete slayer.db to start fresh
```

**Problem**: Missing monsters in frontend
```bash
# Check backend logs for errors
# Verify monsters were seeded:
sqlite3 backend/slayer.db "SELECT COUNT(*) FROM monster;"
# Should show 50+
```

## Data Sources

- **Monster stats**: OSRS Wiki individual monster pages
- **Task weights**: OSRS Wiki slayer master pages
- **Task quantities**: Official OSRS data

## Updates

Last updated: January 27, 2026
- Added comprehensive Duradel tasks (40+)
- Added comprehensive Nieve/Steve tasks (43+)
- Added all missing monster definitions (50+)
