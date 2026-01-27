# OSRS Tool Hub - Project Roadmap

**Last Updated**: 2026-01-27  
**Current Status**: Active Development  
**Test Coverage**: 80% (Target: 85%+) ⬆️ Improved from 73% → 80%  
**Version**: 0.1.0

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Short-term Roadmap (1-2 months)](#short-term-roadmap-1-2-months)
3. [Medium-term Roadmap (3-6 months)](#medium-term-roadmap-3-6-months)
4. [Long-term Vision (6+ months)](#long-term-vision-6-months)
5. [Technical Debt & Infrastructure](#technical-debt--infrastructure)
6. [Open Source Integration](#open-source-integration)
7. [Competitive Analysis](#competitive-analysis)
8. [Deep End-to-End Project Analysis](#deep-end-to-end-project-analysis)
9. [Refactoring Recommendations](#refactoring-recommendations)
10. [Documentation Improvements](#documentation-improvements)
11. [Current Implementation Improvements](#current-implementation-improvements)
12. [Recommendations & Priorities](#recommendations--priorities)

---

## Executive Summary

### Current Project Status

**OSRS Tool Hub** is a comprehensive tool hub for Old School RuneScape players, featuring:
- ✅ **Flipping Calculator** - Find profitable Grand Exchange flips
- ✅ **Gear Progression** - Best-in-slot gear finder and progression guides
- ✅ **Slayer Helper** - Task management and advice system

**Tech Stack**:
- Backend: FastAPI + SQLModel + SQLite
- Frontend: React + Vite + TypeScript + Mantine UI
- Testing: pytest (backend), Vitest (frontend)
- Coverage: 73% overall (102 tests passing, 5 failing)

### Competitive Positioning

**Unique Advantages**:
- All-in-one tool (flipping + gear + slayer)
- Open source and self-hostable
- Modern tech stack
- Free and community-driven

**Competitors**:
- GE Tracker (commercial, 733k+ users)
- OSRSToolkit (commercial)
- OldSchool.tools (free, feature-specific)

### Vision Statement

To become the premier open-source, all-in-one OSRS tool hub that combines flipping, gear progression, and slayer management in a modern, user-friendly interface. We aim to provide accurate, real-time data and calculations while maintaining transparency and community involvement.

---

## Short-term Roadmap (1-2 months)

**Status Legend**: 🔴 Not Started | 🟡 In Progress | 🟢 Completed | ⚪ Blocked

### Core Features

- [x] 🟢 **Real-time Price Integration** (P0 - Critical) ✅ COMPLETED
  - ✅ Integrated OSRS Wiki Real-time Prices API
  - ✅ Replaced static price snapshots with live data
  - ✅ Update interval: 5 minutes (300 seconds)
  - ✅ Scheduler configured and running
  - Effort: Medium | Files: `backend/services/wiki/sync.py`, `backend/app/scheduler.py`

- [ ] 🔴 **Price History Tracking** (P0 - Critical)
  - Store historical price data
  - Database schema for price history
  - Background job to collect prices
  - Effort: Large | Files: `backend/models/items.py`, `backend/db/migrations.py`

- [ ] 🔴 **Enhanced Filtering & Sorting** (P1 - Important)
  - Advanced filters for flipping (category, members status)
  - Multi-column sorting
  - Saved filter presets
  - Effort: Small | Files: `frontend/src/features/flipping/components/FiltersBar.tsx`

- [ ] 🟡 **Test Coverage Improvements** (P0 - Critical)
  - Target: 85%+ coverage (currently 80%, improved from 73%)
  - ✅ Scripts: 94-97% coverage (was 0%) - seed_prices, seed_slayer, check_slayer_data
  - ✅ Wiki sync: 100% coverage (was 0-29%) - sync_items_to_db, sync_prices_to_db
  - ✅ App lifecycle: 85% coverage (was 33%) - lifespan.py, scheduler.py (100%)
  - ✅ Gear routes: 86-100% coverage (was 57-70%) - suggestions.py (100%), progression.py (86%)
  - Focus areas remaining: fetch_wiki_gear.py (0%), DPS calculations (54%), gear/loadouts.py (52%)
  - Effort: Medium | Files: `backend/tests/`

- [x] 🟢 **Bug Fixes** (P0 - Critical) ✅ COMPLETED
  - ✅ Fixed 5 failing tests (all 125 tests now passing)
  - ✅ Fixed gear set creation JSON key type mismatch
  - ✅ Fixed slayer masters endpoint issues
  - ✅ Fixed test isolation issues
  - Effort: Small | Files: `backend/tests/test_e2e_gear.py`, `backend/tests/test_e2e_slayer.py`

### Slayer Improvements

- [ ] 🔴 **Task Weight Calculations** (P1 - Important)
  - Implement slayer task weight calculator
  - Display weight percentages
  - Research-based implementation
  - Effort: Medium | Files: `backend/services/slayer.py`, `frontend/src/features/slayer/`

- [ ] 🔴 **Slayer Point Reward Calculator** (P1 - Important)
  - Calculate points per task
  - Track point accumulation
  - Display rewards available
  - Effort: Medium | Files: `backend/services/slayer.py`

- [ ] 🔴 **Task Blocking/Skipping Recommendations** (P1 - Important)
  - Algorithm for optimal blocking strategy
  - Skip recommendations based on XP/profit
  - Visual indicators in UI
  - Effort: Large | Files: `backend/services/slayer.py`, `frontend/src/features/slayer/`

- [ ] 🔴 **Enhanced Task Filtering** (P2 - Nice to Have)
  - Filter by XP rate, profit, difficulty
  - Sort by multiple criteria
  - Effort: Small | Files: `frontend/src/features/slayer/components/TaskGrid.tsx`

- [ ] 🔴 **OSRSBox Monster Data Integration** (P1 - Important)
  - Leverage osrsbox-db for comprehensive monster data
  - Enhanced monster stats and drops
  - Effort: Medium | Files: `backend/services/item_stats.py`

### Gear Improvements

- [ ] 🔴 **Advanced DPS Formulas** (P0 - Critical)
  - Integrate formulas from osrs-dps-calc
  - Reference: Bitterkoekje's spreadsheet formulas
  - Improve calculation accuracy
  - Effort: Large | Files: `backend/services/gear/dps.py`

- [ ] 🔴 **Hit Distribution Visualization** (P1 - Important)
  - Display hit distribution charts
  - Visual representation of damage ranges
  - Effort: Medium | Files: `frontend/src/features/gear/components/`

- [ ] 🔴 **Time-to-Kill Calculations** (P1 - Important)
  - Calculate TTK for different monsters
  - Compare loadouts by TTK
  - Effort: Medium | Files: `backend/services/gear/dps.py`

- [ ] 🔴 **Best-in-Slot Algorithm Improvements** (P1 - Important)
  - Enhance accuracy of BiS calculations
  - Consider more stat combinations
  - Effort: Medium | Files: `backend/services/gear/loadouts.py`

---

## Medium-term Roadmap (3-6 months)

### Flipping Enhancements

- [ ] 🔴 **Price Alerts/Notifications** (P1 - Important)
  - User-configurable price alerts
  - Email/push notifications
  - Alert history
  - Effort: Large | Requires: User accounts

- [ ] 🔴 **Historical Price Graphs** (P1 - Important)
  - Price history visualization
  - Chart library integration (Chart.js/Recharts)
  - Time range selection
  - Effort: Medium | Files: `frontend/src/features/flipping/components/`

- [ ] 🔴 **Market Trend Analysis** (P2 - Nice to Have)
  - Price trend indicators
  - Volume analysis
  - Market health metrics
  - Effort: Large

- [ ] 🔴 **Export/Import Functionality** (P1 - Important)
  - Export flip lists (CSV, JSON)
  - Import saved flips
  - Share flip opportunities
  - Effort: Small | Files: `frontend/src/features/flipping/utils/`

### Slayer Enhancements

- [ ] 🔴 **Task History & Completion Tracking** (P1 - Important)
  - Track completed tasks
  - Task streak tracking
  - Statistics dashboard
  - Effort: Large | Requires: User accounts

- [ ] 🔴 **Slayer Point Optimization Calculator** (P1 - Important)
  - Optimal blocking strategy calculator
  - Point accumulation tracking
  - Reward optimization
  - Effort: Medium | Files: `backend/services/slayer.py`

- [ ] 🔴 **Task Streak Tracking** (P2 - Nice to Have)
  - Track consecutive tasks
  - Streak bonuses display
  - Effort: Small

- [ ] 🔴 **Advanced Filtering** (P2 - Nice to Have)
  - Filter by XP rate, profit, difficulty
  - Multi-criteria filtering
  - Effort: Small

### Gear Enhancements

- [ ] 🔴 **Multi-Loadout Comparison** (P1 - Important)
  - Side-by-side loadout comparison
  - DPS comparison tables
  - Visual diff highlighting
  - Effort: Large | Files: `frontend/src/features/gear/components/`

- [ ] 🔴 **DPS Graphs & Visualization** (P1 - Important)
  - Time-to-kill charts
  - Damage distribution graphs
  - Loadout performance over time
  - Effort: Medium | Files: `frontend/src/features/gear/components/`

- [ ] 🔴 **Advanced Stat Requirement Filtering** (P1 - Important)
  - Filter by quest requirements
  - Achievement requirement filtering
  - Level requirement combinations
  - Effort: Small | Files: `backend/services/gear/requirements.py`

- [ ] 🔴 **Gear Set Sharing** (P1 - Important)
  - Shareable gear set URLs
  - Export/import gear sets
  - Public gear set library
  - Effort: Medium | Files: `backend/api/v1/gear/`, `frontend/src/features/gear/`

### General Improvements

- [ ] 🔴 **User Preferences & Saved Filters** (P1 - Important)
  - Save filter configurations
  - User preferences storage
  - Effort: Medium | Requires: Local storage or user accounts

- [ ] 🔴 **Mobile-Responsive Improvements** (P1 - Important)
  - Responsive design enhancements
  - Mobile-optimized UI components
  - Touch-friendly interactions
  - Effort: Medium | Files: `frontend/src/`

---

## Long-term Vision (6+ months)

### User Features

- [ ] 🔴 **User Accounts & Authentication** (P1 - Important)
  - User registration/login
  - JWT authentication
  - User profiles
  - Effort: Large | Files: `backend/api/v1/auth/`, `backend/models/user.py`

- [ ] 🔴 **Data Persistence** (P1 - Important)
  - Save flip lists per user
  - Saved gear sets
  - Task history persistence
  - Effort: Large

- [ ] 🔴 **Portfolio Tracking** (P1 - Important)
  - Track flip performance
  - Profit/loss tracking
  - Historical performance graphs
  - Effort: Large

### Advanced Features

- [ ] 🔴 **Advanced Gear Comparison Tools** (P2 - Nice to Have)
  - Multi-loadout optimization
  - Budget-based recommendations
  - Upgrade path suggestions
  - Effort: Large

- [ ] 🔴 **Slayer Task Tracking & History** (P1 - Important)
  - Personal task history
  - Completion statistics
  - XP tracking
  - Effort: Large

### Infrastructure

- [x] 🟢 **API Rate Limiting** (P0 - Critical) ✅ COMPLETED
  - ✅ Implemented rate limiting middleware using slowapi
  - ✅ Default rate limit: 100 requests/minute per IP
  - ✅ Configurable via settings (can be disabled)
  - ✅ Applied to key endpoints (flips, slayer)
  - ✅ Error handling for rate limit exceeded
  - Effort: Medium | Files: `backend/app/middleware.py`, `backend/config.py`

- [ ] 🔴 **Caching Improvements** (P1 - Important)
  - Redis integration
  - Cache price data
  - Cache gear calculations
  - Effort: Medium

- [ ] 🔴 **Performance Optimizations** (P1 - Important)
  - Database query optimization
  - Frontend code splitting
  - Lazy loading
  - Effort: Medium

---

## Technical Debt & Infrastructure

### Testing Improvements

- [ ] 🔴 **Scripts Testing** (P0 - Critical)
  - Current coverage: 0%
  - Add tests for `backend/scripts/seed_prices.py`
  - Add tests for `backend/scripts/seed_slayer.py`
  - Add tests for `backend/scripts/fetch_wiki_gear.py`
  - Effort: Medium | Files: `backend/tests/scripts/`

- [ ] 🔴 **Wiki Sync Service Testing** (P0 - Critical)
  - Current coverage: 0-29%
  - Test `backend/services/wiki/sync.py`
  - Test `backend/services/wiki_client.py`
  - Mock external API calls
  - Effort: Medium | Files: `backend/tests/services/wiki/`

- [ ] 🔴 **DPS Calculation Edge Cases** (P1 - Important)
  - Test edge cases in DPS calculations
  - Test with various stat combinations
  - Test special attack handling
  - Effort: Small | Files: `backend/tests/services/gear/test_dps.py`

- [ ] 🔴 **Integration Test Coverage** (P1 - Important)
  - Expand E2E test coverage
  - Test critical user flows
  - Test error scenarios
  - Effort: Medium

### Database Improvements

- [ ] 🔴 **Migration Improvements** (P1 - Important)
  - Better migration scripts
  - Rollback support
  - Migration testing
  - Effort: Small | Files: `backend/db/migrations.py`

- [ ] 🔴 **Query Optimization** (P1 - Important)
  - Add database indexes
  - Optimize slow queries
  - Query performance monitoring
  - Effort: Medium

- [ ] 🔴 **PostgreSQL Migration Path** (P2 - Nice to Have)
  - Plan migration from SQLite to PostgreSQL
  - Test compatibility
  - Update connection strings
  - Effort: Large

### CI/CD Enhancements

- [ ] 🔴 **CI Pipeline Improvements** (P1 - Important)
  - Add coverage reporting
  - Add linting checks
  - Add security scanning
  - Effort: Small | Files: `.github/workflows/ci.yml`

- [ ] 🔴 **Automated Testing** (P1 - Important)
  - Run tests on PR
  - Test coverage gates
  - Effort: Small

---

## Open Source Integration

### DPS Calculator Improvements (osrs-dps-calc)

**Reference**: https://github.com/weirdgloop/osrs-dps-calc  
**License**: GPL-3.0  
**Status**: ✅ Actively maintained by Weird Gloop (official wiki maintainers)

- [ ] 🔴 **Integrate Advanced DPS Formulas** (P0 - Critical)
  - Study osrs-dps-calc implementation
  - Integrate Bitterkoekje's formulas
  - Improve calculation accuracy
  - Effort: Large | Files: `backend/services/gear/dps.py`

- [ ] 🔴 **Add Hit Distribution Analysis** (P1 - Important)
  - Implement hit distribution calculations
  - Visualize damage ranges
  - Effort: Medium

- [ ] 🔴 **Implement Time-to-Kill Calculations** (P1 - Important)
  - Calculate TTK for monsters
  - Compare loadouts by TTK
  - Effort: Medium

- [ ] 🔴 **Add Loadout Comparison Features** (P1 - Important)
  - Side-by-side comparison
  - DPS difference highlighting
  - Effort: Medium

### Slayer Feature Enhancements (osrsbox-db)

**Reference**: https://github.com/osrsbox/osrsbox-db  
**License**: GPL-3.0  
**Status**: ✅ Actively maintained, weekly updates

- [ ] 🔴 **Enhanced Monster Data Integration** (P1 - Important)
  - Use osrsbox-db for comprehensive monster data
  - Validate our data structures against schemas
  - Effort: Medium | Files: `backend/services/item_stats.py`

- [ ] 🔴 **Task Weight Calculator** (P1 - Important)
  - Research-based implementation
  - Display weight percentages
  - Effort: Medium

- [ ] 🔴 **Slayer Point Reward Calculator** (P1 - Important)
  - Calculate points per task
  - Track point accumulation
  - Effort: Medium

- [ ] 🔴 **Task Blocking/Skipping Optimization** (P1 - Important)
  - Algorithm for optimal blocking strategy
  - Skip recommendations
  - Effort: Large

### Reusable Libraries

- [ ] 🔴 **Evaluate osrs-json-hiscores** (P2 - Nice to Have)
  - Reference: https://github.com/maxswa/osrs-json-hiscores
  - License: ISC
  - Status: ✅ Actively maintained
  - Use for future hiscore features
  - Effort: Small

- [ ] 🔴 **Leverage osrsbox-db Schemas** (P1 - Important)
  - Use schemas for data validation
  - Ensure data structure compatibility
  - Effort: Small

---

## Competitive Analysis

### GE Tracker Features to Consider

- [ ] 🔴 **Live Market Prices** (P0 - Critical)
  - Real-time price updates
  - 5-minute interval data
  - Already planned in short-term

- [ ] 🔴 **Price Alerts** (P1 - Important)
  - User-configurable alerts
  - Already planned in medium-term

- [ ] 🔴 **Market Indices** (P2 - Nice to Have)
  - Track economic health
  - Category-based indices
  - Effort: Large

### OSRSToolkit Features to Consider

- [ ] 🔴 **Best-in-Slot Finder** (P1 - Important)
  - Already implemented, needs improvement
  - Enhance algorithm accuracy

- [ ] 🔴 **Gear Set Templates** (P1 - Important)
  - Pre-built gear sets
  - Community templates
  - Effort: Medium

### Unique Differentiators to Maintain

- ✅ **All-in-One Tool** - Keep combining flipping, gear, and slayer
- ✅ **Open Source** - Maintain transparency and community involvement
- ✅ **Self-Hostable** - Allow users to run their own instances
- ✅ **Modern Tech Stack** - Fast, responsive, maintainable

---

## Deep End-to-End Project Analysis

### Architecture Overview

**Backend Architecture**:
```
FastAPI App
├── API Routes (backend/api/v1/)
│   ├── flips.py - Flipping endpoints
│   ├── gear/ - Gear endpoints (modularized)
│   └── slayer.py - Slayer endpoints
├── Services (backend/services/)
│   ├── flipping.py - Flipping business logic
│   ├── gear/ - Gear services (modularized)
│   ├── slayer.py - Slayer business logic
│   └── wiki/ - Wiki sync services
└── Database (SQLModel + SQLite)
    └── Models (backend/models/)
```

**Frontend Architecture**:
```
React App (Vite)
├── Features (frontend/src/features/)
│   ├── flipping/ - Flipping feature module
│   ├── gear/ - Gear feature module
│   └── slayer/ - Slayer feature module
├── Shared (frontend/src/lib/)
│   ├── api/ - API client
│   └── utils/ - Shared utilities
└── App.tsx - Main app component
```

### Component Interaction Analysis

**Request Flow**:
1. User interacts with frontend component
2. Component calls API via `frontend/src/lib/api/`
3. Request goes to FastAPI endpoint
4. Endpoint calls service layer
5. Service queries database via SQLModel
6. Response flows back through layers

**Key Interactions**:
- Frontend → API: TanStack Query for data fetching
- API → Services: Dependency injection via FastAPI
- Services → Database: SQLModel ORM
- External APIs: httpx for async HTTP calls

### Data Flow Diagrams

**Flipping Feature Flow**:
```
User Input (Filters)
  ↓
Frontend: FiltersBar.tsx
  ↓
API Call: /api/v1/flips/opportunities
  ↓
Backend: flips.py → FlippingService
  ↓
Database: Query Item + PriceSnapshot
  ↓
Calculate: Tax, Margin, ROI, Potential Profit
  ↓
Response: List of FlipOpportunity
  ↓
Frontend: ResultsTable.tsx (Display)
```

**Gear Feature Flow**:
```
User Selection (Combat Style)
  ↓
Frontend: Gear.tsx
  ↓
API Call: /api/v1/gear/progression/{style}
  ↓
Backend: gear/router.py → GearService
  ↓
Service: Load progression data + enrich with prices
  ↓
Response: Progression data with pricing
  ↓
Frontend: ProgressionViewer.tsx (Display)
```

**Slayer Feature Flow**:
```
User Selection (Master)
  ↓
Frontend: SlayerPage.tsx
  ↓
API Call: /api/v1/slayer/tasks/{master}
  ↓
Backend: slayer.py → SlayerService
  ↓
Database: Query SlayerTask + Monster
  ↓
Calculate: Task advice (if requested)
  ↓
Response: List of tasks with monster data
  ↓
Frontend: TaskGrid.tsx (Display)
```

### Performance Analysis

**Current Performance**:
- ✅ Database queries: Generally efficient (SQLModel)
- ⚠️ Price sync: Runs on schedule (could be optimized)
- ⚠️ Frontend bundle: Could benefit from code splitting
- ⚠️ Caching: No caching layer currently

**Optimization Opportunities**:
- [ ] Add Redis caching for price data
- [ ] Implement database query caching
- [ ] Frontend code splitting by route
- [ ] Lazy load heavy components
- [ ] Optimize database indexes

### Security Analysis

**Current Security**:
- ✅ SQL injection protection (SQLModel ORM)
- ✅ Input validation (Pydantic models)
- ⚠️ No authentication/authorization
- ⚠️ No rate limiting
- ⚠️ CORS configured but could be stricter

**Security Improvements Needed**:
- [ ] Implement rate limiting (P0)
- [ ] Add input sanitization
- [ ] Implement authentication (long-term)
- [ ] Add API key support
- [ ] Security headers (CSP, HSTS)

### Scalability Considerations

**Current Limitations**:
- SQLite: Single-writer limitation
- No horizontal scaling support
- No load balancing

**Scalability Path**:
- [ ] Migrate to PostgreSQL (supports concurrent writes)
- [ ] Add Redis for caching and sessions
- [ ] Implement stateless API design
- [ ] Consider containerization (Docker)
- [ ] Load balancing for multiple instances

---

## Refactoring Recommendations

### Code Quality Improvements

- [ ] 🔴 **Extract Common Utilities** (P1 - Important)
  - Identify duplicate code patterns
  - Create shared utility modules
  - Effort: Small | Files: `backend/services/`, `frontend/src/lib/utils/`

- [ ] 🔴 **Standardize Error Handling** (P1 - Important)
  - Consistent error response format
  - Custom exception classes
  - Error logging standardization
  - Effort: Medium | Files: `backend/app/`, `backend/api/v1/`

- [ ] 🔴 **Improve Type Safety** (P1 - Important)
  - Add more type hints in backend
  - Strict TypeScript in frontend
  - Type validation at boundaries
  - Effort: Medium

- [x] 🟢 **Add Input Validation Layers** (P0 - Critical) ✅ COMPLETED
  - ✅ Created comprehensive validation utilities module
  - ✅ Added validation for query parameters (budget, ROI, volume, levels)
  - ✅ Enhanced Pydantic schemas with field validators
  - ✅ Added validation for gear set creation (name, items)
  - ✅ Added validation for equipment slots and combat styles
  - ✅ Added validation for best loadout requests (stats, combat style, attack type)
  - ✅ Created 14 validation tests
  - Effort: Small | Files: `backend/api/v1/validators.py`, `backend/api/v1/gear/schemas.py`

### Architecture Refactoring

- [ ] 🔴 **Service Layer Consolidation** (P2 - Nice to Have)
  - Review service boundaries
  - Consolidate related services
  - Effort: Medium

- [ ] 🔴 **Frontend Component Decomposition** (P1 - Important)
  - Further decompose large components
  - Extract reusable components
  - Improve component composition
  - Effort: Medium | Files: `frontend/src/features/`

- [ ] 🔴 **State Management Evaluation** (P2 - Nice to Have)
  - Evaluate need for Zustand/Redux
  - Currently using React state + TanStack Query
  - May need global state for user preferences
  - Effort: Small

### Database Refactoring

- [ ] 🔴 **Schema Normalization** (P1 - Important)
  - Review database schema
  - Normalize where appropriate
  - Add missing indexes
  - Effort: Medium | Files: `backend/models/`, `backend/db/migrations.py`

- [ ] 🔴 **Query Optimization** (P1 - Important)
  - Analyze slow queries
  - Add database indexes
  - Optimize JOIN operations
  - Effort: Medium

- [ ] 🔴 **Migration Strategy** (P1 - Important)
  - Improve migration scripts
  - Add rollback support
  - Test migrations
  - Effort: Small | Files: `backend/db/migrations.py`

### Testing Refactoring

- [ ] 🔴 **Increase Coverage** (P0 - Critical)
  - Target: 85%+ (currently 73%)
  - Focus on scripts and wiki sync
  - Effort: Medium

- [ ] 🔴 **Add Integration Tests** (P1 - Important)
  - Test critical user flows
  - End-to-end scenarios
  - Effort: Medium

- [ ] 🔴 **Standardize Mock Data** (P1 - Important)
  - Create shared test fixtures
  - Standardize mock responses
  - Effort: Small | Files: `backend/tests/conftest.py`

---

## Documentation Improvements

### API Documentation

- [ ] 🔴 **Enhance OpenAPI/Swagger Docs** (P1 - Important)
  - Add request/response examples
  - Document error codes
  - Add authentication docs (when implemented)
  - Effort: Small | Files: `backend/api/v1/`

- [ ] 🔴 **Document Error Handling** (P1 - Important)
  - Standard error response format
  - Error code reference
  - Troubleshooting guide
  - Effort: Small

- [ ] 🔴 **Rate Limiting Documentation** (P1 - Important)
  - Document rate limits
  - Rate limit headers
  - Best practices
  - Effort: Small

### Developer Documentation

- [ ] 🔴 **Architecture Decision Records (ADRs)** (P1 - Important)
  - Document major architectural decisions
  - Tech stack choices
  - Design patterns used
  - Effort: Medium | Files: `docs/adr/`

- [ ] 🔴 **Setup Guide Improvements** (P1 - Important)
  - Detailed development setup
  - Environment configuration
  - Troubleshooting common issues
  - Effort: Small | Files: `README.md`, `docs/`

- [ ] 🔴 **Contributing Guidelines** (P1 - Important)
  - How to contribute
  - Code style guide
  - PR process
  - Effort: Small | Files: `CONTRIBUTING.md`

- [ ] 🔴 **Testing Guide** (P1 - Important)
  - How to run tests
  - Writing new tests
  - Test best practices
  - Effort: Small | Files: `docs/testing.md`

### User Documentation

- [ ] 🔴 **Feature Usage Guides** (P2 - Nice to Have)
  - How to use flipping feature
  - How to use gear feature
  - How to use slayer feature
  - Effort: Medium | Files: `docs/user-guide/`

- [ ] 🔴 **FAQ Section** (P2 - Nice to Have)
  - Common questions
  - Troubleshooting
  - Effort: Small | Files: `docs/faq.md`

### Code Documentation

- [ ] 🔴 **Improve Docstrings** (P1 - Important)
  - Add docstrings to all backend functions
  - Follow Google/NumPy style
  - Effort: Medium | Files: `backend/services/`, `backend/api/v1/`

- [ ] 🔴 **Add JSDoc Comments** (P1 - Important)
  - Document frontend functions
  - Type documentation
  - Effort: Medium | Files: `frontend/src/`

- [ ] 🔴 **Document Complex Algorithms** (P1 - Important)
  - DPS calculation formulas
  - Flipping margin calculations
  - Slayer advice algorithms
  - Effort: Small | Files: `docs/algorithms.md`

---

## Current Implementation Improvements

### Flipping Feature Improvements

- [ ] 🔴 **Real-time Price Updates** (P0 - Critical)
  - Currently: Static price snapshots
  - Needed: Live price updates every 5 minutes (300 seconds)
  - Effort: Medium | Files: `backend/services/wiki/sync.py`

- [ ] 🔴 **Price History Visualization** (P1 - Important)
  - Store historical prices
  - Display price charts
  - Effort: Large

- [ ] 🔴 **Advanced Filtering** (P1 - Important)
  - Filter by item category
  - Filter by members status
  - Multi-criteria filtering
  - Effort: Small | Files: `frontend/src/features/flipping/components/FiltersBar.tsx`

- [ ] 🔴 **Bulk Operations** (P2 - Nice to Have)
  - Select multiple flips
  - Bulk export
  - Effort: Small

- [ ] 🔴 **Export Functionality** (P1 - Important)
  - Export to CSV
  - Export to JSON
  - Share flip lists
  - Effort: Small | Files: `frontend/src/features/flipping/utils/`

### Gear Feature Improvements

- [ ] 🔴 **DPS Calculation Accuracy** (P0 - Critical)
  - Integrate osrs-dps-calc formulas
  - Improve calculation precision
  - Effort: Large | Files: `backend/services/gear/dps.py`

- [ ] 🔴 **Visual Gear Comparison** (P1 - Important)
  - Side-by-side comparison
  - Visual diff highlighting
  - Effort: Medium | Files: `frontend/src/features/gear/components/`

- [ ] 🔴 **Stat Requirement Filtering** (P1 - Important)
  - Filter by quest requirements
  - Filter by achievement requirements
  - Level requirement combinations
  - Effort: Small | Files: `backend/services/gear/requirements.py`

- [ ] 🔴 **Gear Set Templates** (P1 - Important)
  - Pre-built gear sets
  - Community templates
  - Effort: Medium

- [ ] 🔴 **Shareable Gear Set URLs** (P1 - Important)
  - Generate shareable URLs
  - Import from URLs
  - Effort: Medium

### Slayer Feature Improvements

- [ ] 🔴 **Task Weight Calculations** (P1 - Important)
  - Display task weights
  - Weight percentage calculator
  - Effort: Medium | Files: `backend/services/slayer.py`

- [ ] 🔴 **Slayer Point Calculator** (P1 - Important)
  - Calculate points per task
  - Track point accumulation
  - Effort: Medium

- [ ] 🔴 **Task Blocking/Skipping Recommendations** (P1 - Important)
  - Optimal blocking strategy
  - Skip recommendations
  - Visual indicators
  - Effort: Large

- [ ] 🔴 **Task History Tracking** (P1 - Important)
  - Track completed tasks
  - Task statistics
  - Effort: Large | Requires: User accounts

- [ ] 🔴 **Monster Weakness Highlighting** (P2 - Nice to Have)
  - Display monster weaknesses
  - Recommended attack styles
  - Effort: Small

### General Improvements

- [ ] 🔴 **Loading States** (P1 - Important)
  - Skeleton screens
  - Loading indicators
  - Better UX during data fetching
  - Effort: Small | Files: `frontend/src/features/*/components/`

- [ ] 🔴 **Error Boundaries** (P1 - Important)
  - React error boundaries
  - User-friendly error messages
  - Error reporting
  - Effort: Small | Files: `frontend/src/`

- [ ] 🔴 **Offline Support** (P2 - Nice to Have)
  - Service worker
  - Offline data caching
  - Effort: Large

- [ ] 🔴 **PWA Capabilities** (P2 - Nice to Have)
  - Progressive Web App
  - Installable
  - Offline support
  - Effort: Medium

- [ ] 🔴 **Accessibility Improvements** (P1 - Important)
  - ARIA labels
  - Keyboard navigation
  - Screen reader support
  - Effort: Medium | Files: `frontend/src/`

- [ ] 🔴 **Internationalization (i18n)** (P2 - Nice to Have)
  - Multi-language support
  - Translation system
  - Effort: Large

---

## Recommendations & Priorities

### High Priority (P0) - Critical

**Must Complete Soon**:
1. ✅ Fix failing tests (5 tests) - **COMPLETED**
2. ✅ Real-time price integration - **COMPLETED**
3. 🟡 Test coverage improvements (80% → 85%+) - **IN PROGRESS**
4. 🔴 Advanced DPS formulas integration - **PENDING**
5. ✅ API rate limiting - **COMPLETED**
6. ✅ Input validation layers - **COMPLETED**

**Impact**: Core functionality, security, reliability  
**Timeline**: 1-2 months

### Medium Priority (P1) - Important

**Should Complete**:
1. Price history tracking
2. Slayer task weight calculator
3. Multi-loadout comparison
4. Documentation improvements
5. Performance optimizations
6. Caching improvements

**Impact**: User experience, feature completeness  
**Timeline**: 3-6 months

### Low Priority (P2) - Nice to Have

**Can Complete Later**:
1. User accounts and data persistence
2. Advanced visualization
3. Export/import functionality
4. Mobile app considerations
5. Internationalization

**Impact**: Enhanced features, broader appeal  
**Timeline**: 6+ months

### Technical Debt Priority

**Address Soon**:
1. Scripts testing (0% coverage)
2. Wiki sync service testing (0-29% coverage)
3. DPS calculation edge cases
4. Database migration improvements
5. CI/CD pipeline enhancements

**Impact**: Code quality, maintainability  
**Timeline**: Ongoing

### Architecture Recommendations

**Consider for Future**:
1. **PostgreSQL Migration**: For production scalability
2. **Redis Integration**: For caching and performance
3. **Message Queue**: For background job processing
4. **Microservices**: If scaling becomes necessary
5. **GraphQL**: For complex queries (evaluate need)

**Impact**: Scalability, performance  
**Timeline**: 6+ months

### Open Source Integration Recommendations

**High Value, Low Effort**:
1. ✅ Integrate osrs-dps-calc formulas (high value, large effort but critical)
2. ✅ Leverage osrsbox-db for data validation (medium effort, high value)
3. ⚪ Consider osrs-json-hiscores for future features (low priority)

**Impact**: Accuracy, data quality  
**Timeline**: Short to medium term

### Competitive Recommendations

**Market Positioning**:
1. ✅ Focus on unique all-in-one tool advantage
2. ✅ Maintain open source and self-hostable differentiator
3. ✅ Leverage modern tech stack advantage
4. ✅ Encourage community-driven feature development

**Impact**: Market position, user adoption  
**Timeline**: Ongoing

---

## Progress Tracking

### Overall Progress

- **Total Items**: ~150+ roadmap items
- **Completed**: 3 items ✅
- **In Progress**: 1 item 🟡
- **Not Started**: ~146+ items

### By Category

| Category | Total | Completed | In Progress | Not Started |
|----------|-------|-----------|-------------|-------------|
| Short-term | 15 | 3 | 1 | 11 |
| Medium-term | 12 | 0 | 0 | 12 |
| Long-term | 8 | 0 | 0 | 8 |
| Technical Debt | 10 | 1 | 1 | 8 |
| Open Source Integration | 8 | 0 | 0 | 8 |
| Refactoring | 12 | 0 | 0 | 12 |
| Documentation | 10 | 0 | 0 | 10 |
| Improvements | 15 | 0 | 0 | 15 |

### Key Metrics

- **Test Coverage**: 80% ⬆️ (was 73%) → Target: 85%+
- **Failing Tests**: 0 ✅ (was 5) → Target: 0 ✅
- **API Endpoints**: 20+ → All tested ✅
- **Features**: 3 → All functional ✅
- **Total Tests**: 125 passing (was 107) ⬆️

---

## Notes

- This roadmap is a living document and should be updated regularly
- Priorities may shift based on user feedback and project needs
- Checkboxes should be updated as items are completed
- Status indicators (🔴🟡🟢⚪) should reflect current state
- Estimated effort levels: Small (1-3 days), Medium (1-2 weeks), Large (2+ weeks)

---

**Last Updated**: 2026-01-27  
**Next Review**: 2026-02-27
