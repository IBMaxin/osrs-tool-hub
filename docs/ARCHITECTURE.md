# Architecture Documentation

This document provides an overview of the OSRS Tool Hub architecture, design decisions, and system components.

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Backend Architecture](#backend-architecture)
4. [Frontend Architecture](#frontend-architecture)
5. [Data Flow](#data-flow)
6. [Database Schema](#database-schema)
7. [API Design](#api-design)
8. [Design Decisions](#design-decisions)

## System Overview

OSRS Tool Hub is a full-stack web application for Old School RuneScape players, providing tools for:
- **Flipping**: Finding profitable Grand Exchange trading opportunities
- **Gear**: Optimizing equipment loadouts and calculating DPS
- **Slayer**: Managing slayer tasks and getting combat advice

### Technology Stack

**Backend**:
- Python 3.13
- FastAPI (async web framework)
- SQLModel (ORM combining Pydantic + SQLAlchemy)
- SQLite (development) / PostgreSQL (production)
- APScheduler (background job scheduling)
- httpx (async HTTP client)

**Frontend**:
- React 18
- TypeScript (strict mode)
- Vite (build tool)
- Mantine UI (component library)
- TanStack Query (data fetching)
- Axios (HTTP client)

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Flipping   │  │     Gear     │  │    Slayer    │      │
│  │   Feature    │  │   Feature    │  │   Feature    │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                  │               │
│         └─────────────────┼──────────────────┘               │
│                           │                                  │
│                  ┌────────▼─────────┐                        │
│                  │  Typed API Client │                        │
│                  │  (lib/api/)      │                        │
│                  └────────┬─────────┘                        │
└────────────────────────────┼──────────────────────────────────┘
                             │ HTTP/REST
┌────────────────────────────▼──────────────────────────────────┐
│                    Backend (FastAPI)                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              API Routes (api/v1/)                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │   │
│  │  │  Flips   │  │   Gear   │  │  Slayer  │          │   │
│  │  │  Trades  │  │   DPS    │  │  Tasks   │          │   │
│  │  │Watchlist │  │   BiS    │  │  Advice  │          │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘          │   │
│  └───────┼─────────────┼──────────────┼─────────────────┘   │
│          │             │              │                       │
│  ┌───────▼─────────────▼──────────────▼──────────────┐      │
│  │            Services Layer (services/)              │      │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐        │      │
│  │  │ Flipping │  │   Gear   │  │  Slayer  │        │      │
│  │  │  Trade   │  │    DPS   │  │   Data   │        │      │
│  │  │Watchlist │  │  Loadout │  │  Service  │        │      │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘        │      │
│  └───────┼─────────────┼──────────────┼───────────────┘      │
│          │             │              │                       │
│  ┌───────▼─────────────▼──────────────▼──────────────┐      │
│  │         Database Layer (SQLModel)                   │      │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐        │      │
│  │  │  Items   │  │  Gear    │  │  Slayer  │        │      │
│  │  │  Prices  │  │  Sets    │  │  Tasks   │        │      │
│  │  │  Trades  │  │  Models  │  │  Monsters│        │      │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘        │      │
│  └───────┼─────────────┼──────────────┼───────────────┘      │
│          │             │              │                       │
│          └─────────────┼──────────────┘                       │
│                        │                                       │
│                  ┌─────▼─────┐                                │
│                  │  Database  │                                │
│                  │ (SQLite/   │                                │
│                  │ PostgreSQL) │                                │
│                  └─────────────┘                                │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐    │
│  │         Background Jobs (APScheduler)                 │    │
│  │  • Price updates (every 5 minutes)                    │    │
│  │  • Watchlist alerts (every 5 minutes)                  │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌──────────────────────────────────────────────────────┐    │
│  │         External APIs                                │    │
│  │  • OSRS Wiki Price API                               │    │
│  └──────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Backend Architecture

### Application Structure

```
backend/
├── app/                    # Application lifecycle
│   ├── factory.py         # FastAPI app creation
│   ├── lifespan.py        # Startup/shutdown tasks
│   ├── scheduler.py       # Background job scheduling
│   ├── middleware.py      # Rate limiting middleware
│   └── logging_config.py  # Logging configuration
├── api/v1/                # API routes (thin layer)
│   ├── flips.py           # Flipping endpoints
│   ├── trades.py          # Trade logging endpoints
│   ├── watchlist.py       # Watchlist endpoints
│   ├── gear/              # Gear endpoints (modular)
│   │   ├── routes/        # Route modules
│   │   ├── schemas.py     # Request/response models
│   │   └── validators.py # Validation helpers
│   └── slayer.py          # Slayer endpoints
├── services/              # Business logic
│   ├── flipping.py       # Flipping calculations
│   ├── trade.py          # Trade tracking
│   ├── watchlist.py      # Watchlist management
│   ├── gear/             # Gear services (modular)
│   │   ├── service.py    # Main gear service
│   │   ├── dps.py        # DPS calculations
│   │   ├── loadouts.py   # Loadout optimization
│   │   ├── boss.py       # Boss BiS calculations
│   │   └── ...
│   ├── slayer.py         # Slayer task logic
│   └── wiki/             # Wiki API client
│       ├── client.py     # HTTP client
│       └── sync.py       # Data synchronization
├── models/                # Database models
│   ├── items.py          # Item, PriceSnapshot
│   ├── gear.py           # GearSet
│   ├── flipping.py       # Trade, WatchlistItem
│   └── slayer.py         # Monster, SlayerTask
├── db/                    # Database layer
│   ├── session.py        # Session management
│   └── migrations.py     # Schema migrations
├── data/                  # Static data
│   └── bosses/           # Boss data JSON files
└── config.py              # Configuration settings
```

### Key Design Principles

1. **Thin Routes**: Routes only handle HTTP concerns (validation, serialization)
2. **Fat Services**: Business logic lives in services
3. **Separation of Concerns**: Clear boundaries between layers
4. **Type Safety**: Full type hints throughout
5. **Async/Await**: Leverage FastAPI's async capabilities

### Request Flow

```
HTTP Request
    ↓
API Route (api/v1/)
    ↓ (validation)
Service Layer (services/)
    ↓ (business logic)
Database Layer (models/ + db/)
    ↓
Database (SQLite/PostgreSQL)
    ↓
Response (serialized)
    ↓
HTTP Response
```

### Background Jobs

**Price Updates** (every 5 minutes):
- Fetches latest prices from OSRS Wiki API
- Updates `PriceSnapshot` records
- Maintains price history

**Watchlist Alerts** (every 5 minutes):
- Evaluates watchlist conditions
- Creates alerts when thresholds are met
- Respects 1-hour cooldown per item

## Frontend Architecture

### Application Structure

```
frontend/src/
├── features/              # Feature modules
│   ├── flipping/         # Flipping feature
│   │   ├── components/   # Feature components
│   │   ├── hooks/        # Feature hooks
│   │   └── types.ts      # Feature types
│   ├── gear/             # Gear feature
│   └── slayer/           # Slayer feature
├── lib/                   # Shared code
│   ├── api/              # Typed API client
│   │   ├── client.ts     # Axios instance
│   │   ├── types.ts      # API types
│   │   └── ...           # API modules
│   ├── components/       # Shared components
│   ├── hooks/            # Shared hooks
│   └── utils/            # Utilities
├── theme/                 # Theme configuration
│   └── osrs-theme.ts     # OSRS color scheme
└── App.tsx               # Root component
```

### Key Design Principles

1. **Feature-First**: Code organized by feature, not by type
2. **Typed API Client**: All API calls through typed client
3. **Component Composition**: Small, reusable components
4. **Custom Hooks**: Business logic in hooks, not components
5. **TypeScript Strict**: No `any`, full type safety

### Data Flow

```
Component
    ↓ (useQuery/useMutation)
Custom Hook (feature/hooks/)
    ↓ (API call)
Typed API Client (lib/api/)
    ↓ (HTTP request)
Backend API
    ↓ (response)
React Query Cache
    ↓ (re-render)
Component
```

### State Management

- **Server State**: TanStack Query (caching, synchronization)
- **Client State**: React useState/useReducer
- **Form State**: Controlled components (Mantine forms)
- **URL State**: React Router (navigation state)

## Data Flow

### Flipping Flow

```
User sets filters
    ↓
Frontend: FiltersBar component
    ↓
useFlips hook queries API
    ↓
Backend: /api/v1/flips/opportunities
    ↓
FlippingService.find_best_flips()
    ↓
Database query with filters
    ↓
Return FlipOpportunity[]
    ↓
Frontend: ResultsTable displays results
```

### Gear DPS Flow

```
User builds loadout
    ↓
Frontend: LoadoutBuilder component
    ↓
useDPSLab hook calls API
    ↓
Backend: /api/v1/dps/compare
    ↓
DPSService.compare_dps()
    ↓
Calculate DPS for each loadout
    ↓
Return DPSComparisonResponse
    ↓
Frontend: DPSComparisonTable displays results
```

### Slayer Advice Flow

```
User selects task
    ↓
Frontend: TaskCard component
    ↓
useSlayerAdvice hook queries API
    ↓
Backend: /api/v1/slayer/advice/{task_id}
    ↓
SlayerService.suggest_action()
    ↓
Evaluate task based on stats
    ↓
Return advice (DO/SKIP/BLOCK)
    ↓
Frontend: AdviceModal displays recommendation
```

## Database Schema

### Core Tables

**Items**:
- `id` (PK)
- `name`, `members`, `tradeable`
- Combat stats (attack, strength, defence, etc.)
- Requirements (quests, achievements, levels)

**PriceSnapshots**:
- `id` (PK)
- `item_id` (FK → Items)
- `buy_price`, `sell_price`, `volume`
- `timestamp`

**Trades**:
- `id` (PK)
- `user_id`, `item_id` (FK → Items)
- `buy_price`, `sell_price`, `quantity`
- `profit`, `status`
- `created_at`, `updated_at`

**WatchlistItems**:
- `id` (PK)
- `user_id`, `item_id` (FK → Items)
- `alert_type`, `threshold`
- `is_active`
- `created_at`, `last_triggered_at`

**WatchlistAlerts**:
- `id` (PK)
- `watchlist_item_id` (FK → WatchlistItems)
- `triggered_at`, `current_value`, `threshold_value`
- `message`

**GearSets**:
- `id` (PK)
- `user_id`, `name`
- `loadout` (JSON)
- `created_at`, `updated_at`

**Monsters**:
- `id` (PK)
- `name`, `combat_level`, `slayer_level`
- `slayer_xp`, `hitpoints`
- Defence stats

**SlayerTasks**:
- `id` (PK)
- `monster_id` (FK → Monsters)
- `master` (enum), `weight`
- `min_quantity`, `max_quantity`

### Relationships

- Items → PriceSnapshots (one-to-many)
- Items → Trades (one-to-many)
- Items → WatchlistItems (one-to-many)
- Monsters → SlayerTasks (one-to-many)
- WatchlistItems → WatchlistAlerts (one-to-many)

## API Design

### Versioning

All endpoints are versioned under `/api/v1/`:
- `/api/v1/flips/opportunities`
- `/api/v1/gear/dps`
- `/api/v1/slayer/advice/{task_id}`

### Error Handling

All errors follow the `ErrorResponse` schema:

```json
{
  "error": {
    "code": "HTTP_400",
    "message": "Validation error",
    "details": {
      "field": "budget",
      "reason": "Must be greater than 0"
    }
  }
}
```

### Rate Limiting

- **Default**: 100 requests/minute per IP
- **Strict**: 10 requests/minute for expensive endpoints
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`

### Authentication

Currently, the API uses client-side user IDs (UUIDs stored in localStorage). Future versions may include JWT authentication.

## Design Decisions

### Why FastAPI?

- **Performance**: Async/await support, high performance
- **Type Safety**: Built on Pydantic for validation
- **Documentation**: Automatic OpenAPI/Swagger docs
- **Modern**: Python 3.13+ features, type hints

### Why SQLModel?

- **Type Safety**: Combines Pydantic + SQLAlchemy
- **Validation**: Request/response validation built-in
- **Flexibility**: Can use SQLAlchemy features when needed
- **Simplicity**: Single model definition for API and DB

### Why React + TypeScript?

- **Type Safety**: Catch errors at compile time
- **Component Reusability**: Modular, composable components
- **Ecosystem**: Rich library ecosystem (Mantine, TanStack Query)
- **Developer Experience**: Great tooling and debugging

### Why Feature-First Structure?

- **Scalability**: Easy to add new features
- **Maintainability**: Related code grouped together
- **Team Collaboration**: Clear ownership boundaries
- **Code Organization**: Intuitive file structure

### Why TanStack Query?

- **Caching**: Automatic request caching and deduplication
- **Synchronization**: Background refetching
- **Optimistic Updates**: Better UX for mutations
- **Error Handling**: Built-in retry and error states

### Database Choice

- **SQLite**: Development and small deployments
- **PostgreSQL**: Production (better concurrency, features)

### Background Jobs

- **APScheduler**: Python-native, easy integration
- **5-minute intervals**: Balance between freshness and API limits
- **Separate jobs**: Price updates and watchlist alerts

## Future Considerations

### Scalability

- **Horizontal Scaling**: Load balancer + multiple backend instances
- **Database Scaling**: Read replicas, connection pooling
- **Caching**: Redis for frequently accessed data
- **CDN**: Static asset delivery

### Features

- **User Accounts**: JWT authentication, user profiles
- **Data Persistence**: Save loadouts, trade history per user
- **Real-time Updates**: WebSocket support for price updates
- **Advanced Analytics**: Historical price charts, trend analysis

### Performance

- **Query Optimization**: Database indexes, query analysis
- **Frontend Optimization**: Code splitting, lazy loading
- **API Optimization**: Response compression, pagination
- **Caching Strategy**: Multi-layer caching (browser, CDN, server)

---

*Last Updated: 2026-01-28*
