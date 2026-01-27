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
│   ├── app/                 # Application factory and configuration
│   │   ├── factory.py       # FastAPI app creation
│   │   ├── lifespan.py      # Startup/shutdown lifecycle
│   │   ├── scheduler.py     # Background task scheduling
│   │   └── middleware.py    # Rate limiting middleware
│   ├── api/v1/              # API routes
│   │   ├── flips.py         # Flipping endpoints
│   │   ├── gear/            # Gear endpoints (modular)
│   │   └── slayer.py        # Slayer endpoints
│   ├── services/            # Business logic
│   │   ├── wiki/            # OSRS Wiki API client
│   │   ├── gear/            # Gear calculation services
│   │   ├── flipping.py      # Flipping service
│   │   └── slayer.py        # Slayer service
│   ├── models/              # SQLModel database models
│   ├── db/                  # Database configuration
│   ├── data/                # Static data (wiki progression)
│   ├── main.py              # Application entry point
│   └── config.py            # Settings and configuration
└── frontend/
    └── src/
        ├── features/        # Feature modules
        │   ├── flipping/    # Flipping tool
        │   ├── gear/        # Gear calculator
        │   └── slayer/      # Slayer task tracker
        ├── lib/             # Shared utilities and API client
        ├── App.tsx          # Main app component
        └── main.tsx         # Application entry point
```

## Setup

### 1. Environment Configuration

Copy the example environment file and configure:

```bash
cp .env.example .env
```

Edit `.env` and update:
- `USER_AGENT` - Replace with your GitHub repository URL
- `CORS_ORIGINS` - Add production domains if deploying
- `DATABASE_URL` - Change to PostgreSQL URL for production

### 2. Backend Setup

Install dependencies:

```bash
poetry install
```

### 3. Frontend Setup

Install dependencies:

```bash
cd frontend
npm install
```

## Running the Application

### Development Mode

**Backend** (runs on port 8000):
```bash
poetry run uvicorn backend.main:app --reload
```

**Frontend** (runs on port 5173):
```bash
cd frontend
npm run dev
```

### Production Mode

**Backend**:
```bash
poetry run uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

**Frontend**:
```bash
cd frontend
npm run build
npm run preview
```

## Testing

### Backend Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=backend --cov-report=html

# Run specific test file
poetry run pytest backend/tests/test_flipping.py
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm run test

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage
```

## Documentation

- **API Documentation**: http://localhost:8000/docs (when running locally)
- **Architecture**: See [refactor.md](refactor.md) for project architecture details
- **Status**: See [STATUS.md](STATUS.md) for current implementation status

## API Endpoints

### Flipping
- `POST /api/v1/flips` - Find profitable flip opportunities
- `GET /api/v1/flips` - Get flip recommendations with filters

### Gear
- `POST /api/v1/gear` - Create a new gear set
- `GET /api/v1/gear` - Get all gear sets
- `GET /api/v1/gear/{id}` - Get gear set by ID
- `GET /api/v1/gear/suggestions` - Get gear suggestions for slot
- `GET /api/v1/gear/preset` - Get preset loadouts by tier
- `GET /api/v1/gear/progression/{style}` - Get wiki progression data
- `POST /api/v1/gear/best-loadout` - Calculate best affordable loadout
- `POST /api/v1/gear/upgrade-path` - Get upgrade recommendations
- `POST /api/v1/gear/dps` - Calculate DPS for loadout
- `DELETE /api/v1/gear/{id}` - Delete a gear set

### Slayer
- `GET /api/v1/slayer/masters` - Get all slayer masters
- `GET /api/v1/slayer/tasks` - Get slayer tasks by master
- `GET /api/v1/slayer/advice` - Get task-specific advice

## Features

### Flipping Calculator
- Real-time GE price tracking via OSRS Wiki API
- Accurate tax calculation (2% with 5M cap)
- ROI and margin analysis
- Volume-based filtering
- Budget-based recommendations

### Gear Calculator
- Wiki-based progression tracking
- DPS calculations for loadouts
- Upgrade path recommendations
- Budget optimization
- Stat requirement validation
- Quest/achievement requirement checking

### Slayer Tracker
- Task assignments by master
- Combat advice and strategies
- Monster weaknesses and locations
- XP and profit tracking

## Development

- Backend follows Python type hints and async/await patterns
- Frontend uses TypeScript strict mode and functional components
- All API endpoints are versioned under `/api/v1/`
- Business logic is contained in backend services
- Database models use SQLModel (Pydantic + SQLAlchemy)
- Frontend state management via TanStack Query

## Code Quality

- **Test Coverage**: 83% (213 tests passing)
- **Type Safety**: Full TypeScript + Python type hints
- **Architecture**: Clean separation of concerns (services/API/models)
- **Performance**: Optimized SQL queries and async operations

## License

MIT License - see LICENSE file for details
