# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-28

### Added

#### Flipping Calculator
- Real-time Grand Exchange price tracking via OSRS Wiki API
- Flip opportunity scanner with budget, ROI, and volume filters
- Accurate tax calculation (2% with 5M cap)
- Trade logging and profit tracking
- Watchlist functionality with price alerts
- Alert notifications for price thresholds
- Trade statistics and profit analysis

#### Gear Calculator
- Loadout builder with gear set management
- DPS (Damage Per Second) calculations for loadouts
- DPS Lab for side-by-side loadout comparisons
- Best-in-Slot (BiS) calculator with budget constraints
- Boss-specific BiS recommendations (Vorkath, Zulrah, TOA, GWD)
- Upgrade path recommendations with DPS/GP ratios
- Wiki-based progression tracking (melee, ranged, magic)
- Preset loadouts by tier
- Gear suggestions by slot
- Constraint-aware loadouts (ironman mode, content tags, tick manipulation)
- Global upgrade path across all combat styles

#### Slayer Tracker
- Slayer master task listings (Duradel, Konar, Nieve, etc.)
- Task-specific advice (DO/SKIP/BLOCK recommendations)
- Detailed location information with requirements
- Monster database with search and filtering
- Combat advice and strategy recommendations
- XP and profit tracking
- Alternative monster suggestions

#### API Endpoints

**Flipping:**
- `GET /api/v1/flips/opportunities` - Get flip opportunities with filters
- `GET /api/v1/flipping/scanner` - GE Tracker-style flip scanner

**Trades:**
- `POST /api/v1/trades` - Log buy/sell transactions
- `GET /api/v1/trades` - Get trade history with filters
- `GET /api/v1/trades/stats` - Get aggregate trade statistics

**Watchlist:**
- `POST /api/v1/watchlist` - Add item to watchlist
- `GET /api/v1/watchlist` - Get user's watchlist
- `DELETE /api/v1/watchlist/{id}` - Remove watchlist item
- `GET /api/v1/watchlist/alerts` - Get triggered alerts

**Gear:**
- `POST /api/v1/gear` - Create gear set
- `GET /api/v1/gear` - Get all gear sets
- `GET /api/v1/gear/{id}` - Get gear set by ID
- `DELETE /api/v1/gear/{id}` - Delete gear set
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

**Slayer:**
- `GET /api/v1/slayer/masters` - Get all slayer masters
- `GET /api/v1/slayer/tasks/{master}` - Get tasks by master
- `GET /api/v1/slayer/advice/{task_id}` - Get task-specific advice
- `GET /api/v1/slayer/location/{task_id}` - Get detailed location information

#### Infrastructure
- FastAPI backend with async/await support
- React frontend with TypeScript strict mode
- SQLModel ORM with SQLite (PostgreSQL-ready)
- Comprehensive test suite (639 tests, 96.7% coverage)
- E2E tests (101 tests)
- Integration tests (28 tests)
- CI/CD pipeline with GitHub Actions
- Rate limiting (100 req/min default, 10 req/min strict)
- CORS configuration
- Background job scheduling for price updates and watchlist alerts
- Database migrations
- OpenAPI/Swagger documentation

#### Frontend Features
- Modern UI with Mantine components
- OSRS-themed color scheme
- Responsive design
- Keyboard shortcuts
- Loading states and error handling
- Searchable dropdowns
- Filter bars with focus support
- Navigation dropdowns with hierarchical structure

### Technical Details

- **Backend**: Python 3.13, FastAPI, SQLModel, SQLite
- **Frontend**: React 18, TypeScript, Vite, Mantine UI, TanStack Query
- **Test Coverage**: 96.7% overall (7,935/8,203 lines covered)
- **Code Quality**: Ruff, Black, MyPy passing
- **API Versioning**: `/api/v1/`
- **Error Handling**: Standardized `ErrorResponse` schema
- **Type Safety**: Full type hints (Python) and strict TypeScript

### Documentation

- Comprehensive README with setup instructions
- API documentation via OpenAPI/Swagger
- Architecture documentation
- Development guidelines

[0.1.0]: https://github.com/IBMaxin/osrs-tool-hub/releases/tag/v0.1.0
