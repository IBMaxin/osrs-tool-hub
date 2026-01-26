# OSRS Tool Hub

A comprehensive tool hub for Old School RuneScape players, featuring flipping calculators, gear set builders, and slayer tools.

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLModel** - SQL database ORM
- **SQLite** - Database (can be swapped for PostgreSQL)
- **httpx** - Async HTTP client
- **apscheduler** - Task scheduling
- **Poetry** - Dependency management

### Frontend
- **React** - UI library
- **Vite** - Build tool
- **TypeScript** - Type safety
- **Mantine UI** - Component library
- **TanStack Query** - Data fetching

## Project Structure

```
osrs-tool-hub/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # Database configuration
│   ├── config.py            # App settings
│   ├── models.py            # SQLModel models
│   ├── services/            # Business logic
│   │   ├── wiki_client.py   # OSRS Wiki API client
│   │   ├── wiki_data.py     # Wiki data service
│   │   ├── flipping.py      # Flipping service
│   │   ├── gear.py          # Gear service
│   │   ├── gear_presets.py  # Gear presets service
│   │   ├── item_stats.py    # Item stats service
│   │   └── slayer.py        # Slayer service
│   └── api/v1/              # API routes
│       ├── flips.py         # Flipping endpoints
│       ├── gear.py          # Gear endpoints
│       └── slayer.py        # Slayer endpoints
└── frontend/
    └── src/
        ├── features/        # Feature modules
        │   ├── flipping/
        │   ├── gear/
        │   └── slayer/
        ├── App.tsx          # Main app component
        └── main.tsx         # Application entry point
```

## Setup

1. Install backend dependencies:
   ```bash
   poetry install
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

## Run

- **Backend**: `poetry run uvicorn backend.main:app --reload` (runs on port 8000)
- **Frontend**: `npm run dev` (runs on port 5173)

## Docs

API documentation available at: http://localhost:8000/docs (when running locally)

See [refactor.md](refactor.md) for planned architectural improvements.

## API Endpoints

### Flipping
- `POST /api/v1/flips` - Create a new flip calculation
- `GET /api/v1/flips` - Get all flips
- `GET /api/v1/flips/{id}` - Get flip by ID
- `DELETE /api/v1/flips/{id}` - Delete a flip

### Gear
- `POST /api/v1/gear` - Create a new gear set
- `GET /api/v1/gear` - Get all gear sets
- `GET /api/v1/gear/{id}` - Get gear set by ID
- `DELETE /api/v1/gear/{id}` - Delete a gear set

### Slayer
- `GET /api/v1/slayer/masters` - Get all slayer masters
- `GET /api/v1/slayer/tasks` - Get slayer tasks

## Development

- Backend code follows Python type hints and async/await patterns
- Frontend uses TypeScript strict mode and functional components
- All API endpoints are under `/api/v1/`
- Business logic is contained in backend services
