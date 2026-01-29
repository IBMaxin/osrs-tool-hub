# OSRS Tool Hub

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![Node.js 20](https://img.shields.io/badge/node-20.x-green.svg)](https://nodejs.org/)
[![Test Coverage](https://img.shields.io/badge/coverage-96.7%25-brightgreen.svg)]()

A comprehensive tool hub for Old School RuneScape players, featuring flipping calculators, gear set builders, and slayer tools.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/osrs-tool-hub.git
cd osrs-tool-hub

# Backend setup
poetry install
cp .env.example .env
poetry run uvicorn backend.main:app --reload

# Frontend setup (in another terminal)
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` to use the application.

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

- **[User Guide](docs/USER_GUIDE.md)** - Complete guide to using all features
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs (when running locally)
- **[Architecture](docs/ARCHITECTURE.md)** - System architecture and design decisions
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment instructions
- **[Contributing](CONTRIBUTING.md)** - Development setup and contribution guidelines
- **[Security Policy](SECURITY.md)** - Security policy and best practices
- **[Changelog](CHANGELOG.md)** - Version history and release notes

## API Endpoints

### Flipping
- `GET /api/v1/flips/opportunities` - Get flip opportunities with filters
- `GET /api/v1/flipping/scanner` - GE Tracker-style flip scanner
- `POST /api/v1/trades` - Log buy/sell transactions
- `GET /api/v1/trades` - Get trade history with filters
- `GET /api/v1/trades/stats` - Get aggregate trade statistics
- `POST /api/v1/watchlist` - Add item to watchlist
- `GET /api/v1/watchlist` - Get user's watchlist
- `DELETE /api/v1/watchlist/{id}` - Remove watchlist item
- `GET /api/v1/watchlist/alerts` - Get triggered alerts

### Gear
- `POST /api/v1/gear` - Create a new gear set
- `GET /api/v1/gear` - Get all gear sets
- `GET /api/v1/gear/{id}` - Get gear set by ID
- `DELETE /api/v1/gear/{id}` - Delete a gear set
- `GET /api/v1/gear/suggestions` - Get gear suggestions for slot
- `GET /api/v1/gear/preset` - Get preset loadouts by tier
- `GET /api/v1/gear/progression/{style}` - Get wiki progression data
- `POST /api/v1/gear/best-loadout` - Calculate best affordable loadout
- `POST /api/v1/gear/upgrade-path` - Get upgrade recommendations
- `POST /api/v1/gear/dps` - Calculate DPS for loadout
- `POST /api/v1/dps/compare` - Compare multiple loadouts side-by-side
- `GET /api/v1/gear/bosses` - List available bosses
- `POST /api/v1/gear/bis/{boss_name}` - Calculate boss BiS
- `GET /api/v1/gear/items/{item_id}` - Get item details
- `POST /api/v1/gear/slayer-gear` - Get slayer gear suggestions

### Slayer
- `GET /api/v1/slayer/masters` - Get all slayer masters
- `GET /api/v1/slayer/tasks/{master}` - Get slayer tasks by master
- `GET /api/v1/slayer/advice/{task_id}` - Get task-specific advice
- `GET /api/v1/slayer/location/{task_id}` - Get detailed location information

### Health
- `GET /api/v1/health` - Health check endpoint (database + external API status)

## Features

### Flipping Calculator
- Real-time GE price tracking via OSRS Wiki API (5-minute updates)
- Accurate tax calculation (2% with 5M cap)
- ROI and margin analysis
- Volume-based filtering
- Budget-based recommendations
- Trade logging and profit tracking
- Watchlist with price alerts
- Trade statistics and analytics

### Gear Calculator
- Wiki-based progression tracking (melee, ranged, magic)
- DPS calculations for loadouts
- DPS Lab for side-by-side loadout comparisons
- Best-in-Slot (BiS) calculator with budget constraints
- Boss-specific BiS recommendations (Vorkath, Zulrah, TOA, GWD)
- Upgrade path recommendations with DPS/GP ratios
- Constraint-aware loadouts (ironman mode, content tags)
- Global upgrade path across all combat styles

### Slayer Tracker
- Task assignments by master (Duradel, Konar, Nieve, etc.)
- Task-specific advice (DO/SKIP/BLOCK recommendations)
- Detailed location information with requirements
- Monster database with search and filtering
- Combat advice and strategy recommendations
- XP and profit tracking
- Alternative monster suggestions

## Development

- Backend follows Python type hints and async/await patterns
- Frontend uses TypeScript strict mode and functional components
- All API endpoints are versioned under `/api/v1/`
- Business logic is contained in backend services
- Database models use SQLModel (Pydantic + SQLAlchemy)
- Frontend state management via TanStack Query

## Code Quality

- **Test Coverage**: 96.7% overall (639 tests passing)
  - 101 E2E tests
  - 28 integration tests
  - 510+ unit tests
- **Type Safety**: Full TypeScript strict mode + Python type hints
- **Architecture**: Clean separation of concerns (services/API/models)
- **Performance**: Optimized SQL queries and async operations
- **CI/CD**: Automated testing, linting, and type checking

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup instructions
- Code style guidelines
- Testing requirements
- Pull request process

## Deployment

For production deployment, see [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for:
- Environment configuration
- Database setup (SQLite/PostgreSQL)
- Backend deployment options
- Frontend static hosting
- Reverse proxy configuration
- Monitoring and health checks

## License

MIT License - see [LICENSE](LICENSE) file for details

## Support

- **Issues**: Report bugs or request features on [GitHub Issues](https://github.com/YOUR_USERNAME/osrs-tool-hub/issues)
- **Security**: Report security vulnerabilities via [SECURITY.md](SECURITY.md)
- **Documentation**: See [docs/](docs/) directory for detailed documentation

## Version

Current version: **0.1.0** (Initial Release)

See [CHANGELOG.md](CHANGELOG.md) for version history.
