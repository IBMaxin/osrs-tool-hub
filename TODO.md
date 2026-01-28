# OSRS Tool Hub - Consolidated TODO

**Last Updated**: 2026-01-28  
**Status**: Active Development  
**Test Coverage**: 91%+ (350 tests passing) ✅

---

## ✅ Completed Items (Archive)

### Backend Infrastructure
- [x] Real-time price integration via OSRS Wiki API (5-minute updates)
- [x] API rate limiting (100 req/min per IP, configurable)
- [x] Input validation layers (comprehensive validation utilities)
- [x] Database indexes for slayer tasks (70% faster queries)
- [x] Backend modularization (100% complete)
  - [x] Models split into package structure
  - [x] App lifecycle modules separated
  - [x] Database layer split by responsibility
  - [x] Gear API split with routes subdirectory
  - [x] Gear services split into focused modules
  - [x] Static progression data moved to JSON
  - [x] Seeds reorganized into modules
  - [x] Wiki client split into client/sync

### Frontend Refactoring
- [x] Frontend modularization (100% complete)
  - [x] Shared API client module created
  - [x] Feature-first structure with hooks, components, types, utils
  - [x] Large components decomposed with hooks extraction
  - [x] Formatting helpers consolidated
  - [x] Custom hooks extracted (useFlips, useSlayerMasters, useSlayerTasks, useSlayerAdvice, useGearProgression, useWikiGearProgression)
  - [x] Types.ts files created for each feature

### Slayer Feature
- [x] 4 API endpoints fully functional
- [x] Frontend components (SlayerPage, MasterSelector, TaskGrid, TaskCard, AdviceModal, LocationSection)
- [x] Custom hooks (useSlayerMasters, useSlayerTasks, useSlayerAdvice)
- [x] Type safety fixes (removed all `any` types)
- [x] Added 11 new slayer tasks with complete data:
  - Turoth, Scabarites, Brine rats, Ankou, Black dragons, Bronze dragons, Trolls, Waterfiends, Elves, Mutated zygomites, Fossil Island wyverns
- [x] Nieve task coverage: 21% → ~85% (35/41 tasks with complete data)
- [x] Updated Location and Alternative interfaces
- [x] Removed debug logging from API endpoints
- [x] Fixed duplicate data entries
- [x] Added database indexes

### Flipping Service
- [x] Fixed potential profit calculation bug (now uses MIN(limit, volume))
- [x] Fixed missing sell price validation
- [x] Fixed inconsistent calculation between methods
- [x] Added comprehensive test coverage

### Testing
- [x] Fixed 11 failing tests (test database setup)
- [x] Updated slayer API tests for new parameters
- [x] All 239 tests passing (100% pass rate)
- [x] Fixed ResizeObserver mock for frontend tests
- [x] Fixed integration test JSON key serialization
- [x] Fixed test_suggest_action (Waterfiends use slayer data "DO")
- [x] Added comprehensive test coverage for low-coverage modules (2026-01-28)
  - [x] Added 102 new unit tests across 7 test files
  - [x] Improved coverage for pricing, progression, loadouts, wiki_data, utils, validators, and gear_sets modules
  - [x] All tests follow modular, maintainable structure
  - [x] Tests cover edge cases, error paths, and boundary conditions
  - [x] Total tests: 350 passing (248 + 102 new tests)

### Configuration & Security
- [x] Removed hardcoded credentials from User-Agent
- [x] Made CORS origins configurable via .env
- [x] Created comprehensive .env.example
- [x] Improved .gitignore

### Linting & Formatting (Backend)
- [x] Ruff: all checks passing (unused imports, etc. fixed)
- [x] Black: backend formatted (94 files); `black --check` passes

### Engineering Reliability Pass (2026-01-28)
- [x] **Backend Interface Lockdown**
  - [x] Created consistent error response schema (`ErrorResponse` + `ErrorDetail` models)
  - [x] Added global exception handler for all HTTPExceptions
  - [x] Added `response_model` to all key endpoints (`/api/v1/flips/opportunities`, `/api/v1/slayer/masters`)
  - [x] Updated `FlipOpportunity` model to match service output (added optional fields)
- [x] **Frontend Typed API Strategy**
  - [x] Added `ErrorResponse` and `ErrorDetail` TypeScript types
  - [x] Enhanced API client with `ApiError` class for structured error handling
  - [x] Updated axios interceptor to handle `ErrorResponse` schema
- [x] **Backend Contract Tests**
  - [x] Created `test_flips_contract.py` (4 tests: golden path + validation errors)
  - [x] Created `test_gear_contract.py` (3 tests: golden path + validation + service errors)
  - [x] All contract tests verify response models match actual responses
  - [x] All contract tests verify error responses match `ErrorResponse` schema
- [x] **E2E Smoke Test**
  - [x] Created `test_smoke.py` with critical path and error path tests
  - [x] Tests verify endpoint returns 200 + valid schema
  - [x] Tests verify validation errors return proper status codes
- [x] **Version Pinning & CI**
  - [x] Pinned Python version to `^3.13` in `pyproject.toml`
  - [x] Pinned Node version to `20` via `.nvmrc` and `package.json` engines
  - [x] Updated CI workflow to use Python 3.13
  - [x] Added Poetry dependency caching to CI
  - [x] Added npm dependency caching to CI
- [x] **Test Results**: All 9 new tests passing ✅
- [x] **Linting**: Ruff + Black checks passing ✅

---

## 🔴 High Priority (P0/P1) - Critical/Important

### Slayer Feature Enhancements

#### Task Filtering & Sorting (Frontend)
**Files**: `frontend/src/features/slayer/components/TaskGrid.tsx`, `SlayerPage.tsx`
- [ ] Filter by XP rate
- [ ] Filter by profit rate
- [ ] Filter by combat level range
- [ ] Filter by recommendation (DO/SKIP/BLOCK)
- [ ] Sort by multiple criteria (XP, profit, weight, combat level)
- [ ] Search by monster name
- [ ] Add filter UI component (collapsible filter sidebar)
- [ ] Add sort dropdown (multi-criteria sorting)

#### Task Weight Calculator (Backend + Frontend)
**Files**: `backend/services/slayer.py`, `frontend/src/features/slayer/components/TaskCard.tsx`
- [ ] Calculate weight percentage per task in backend
- [ ] Display probability of getting each task
- [ ] Show total weight for master
- [ ] Visual weight distribution chart (progress bars)
- [ ] Add weight percentage to task response

#### Slayer Point Calculator (Backend + Frontend)
**Files**: `backend/services/slayer.py`, new component
- [ ] Points per task calculation
- [ ] Point accumulation tracking
- [ ] Reward unlock calculator
- [ ] Point efficiency metrics
- [ ] Create new frontend component for point calculator

#### Enhanced Block/Skip Recommendations (Backend)
**Files**: `backend/services/slayer.py`, `TaskCard.tsx`
- [ ] Algorithm for optimal blocking strategy
- [ ] Skip recommendations based on XP/profit efficiency
- [ ] Visual indicators in UI (color coding: DO=green, SKIP=yellow, BLOCK=red)
- [ ] Block list management UI
- [ ] Add color-coded borders to task cards

#### Slayer Data Improvements
**Files**: `backend/services/slayer_data/*.py`
- [ ] Convert 18 tasks from string-based to detailed location format:
  - Black demons, Greater demons, Smoke devils
  - Blue dragons, Steel dragons, Iron dragons
  - Wyrms, Drakes, Hydras
  - Mithril dragons, Adamant dragons, Rune dragons
  - Kraken, Cave kraken, Fire giants
  - Suqah, TzHaar, Spiritual creatures
- [ ] Add XP/profit rates for tasks (currently defaults to 0)
- [ ] Add more alternative monsters
- [ ] Add quest/requirement details

### Gear Feature Improvements

#### Advanced DPS Formulas (P0 - Critical)
**Files**: `backend/services/gear/dps.py`
- [ ] Integrate formulas from osrs-dps-calc (Bitterkoekje's spreadsheet)
- [ ] Improve calculation accuracy
- [ ] Add hit distribution calculations
- [ ] Implement time-to-kill calculations

#### Best-in-Slot Algorithm Improvements
**Files**: `backend/services/gear/loadouts.py`
- [ ] Enhance accuracy of BiS calculations
- [ ] Consider more stat combinations
- [ ] Improve upgrade path recommendations

### Flipping Feature Improvements

#### Price History Tracking (P0 - Critical)
**Files**: `backend/models/items.py`, `backend/db/migrations.py`
- [ ] Store historical price data
- [ ] Database schema for price history
- [ ] Background job to collect prices
- [ ] Price history visualization (charts)

#### Enhanced Filtering & Sorting
**Files**: `frontend/src/features/flipping/components/FiltersBar.tsx`
- [ ] Advanced filters (category, members status)
- [ ] Multi-column sorting
- [ ] Saved filter presets

### General Improvements

#### Performance Optimizations
- [ ] Add Redis caching for price data
- [ ] Implement database query caching
- [ ] Frontend code splitting by route
- [ ] Lazy load heavy components
- [ ] Optimize database indexes

#### Error Handling & UX
**Files**: `frontend/src/features/*/`
- [ ] Improve error handling in hooks (more user-friendly messages)
- [ ] Add error boundaries for all features
- [ ] Better error display in UI
- [ ] Loading states (skeleton screens, loading indicators)
- [ ] Accessibility improvements (ARIA labels, keyboard navigation)

---

## 🟡 Medium Priority (P2) - Enhancements

### Slayer Feature

#### Task Statistics Dashboard (Frontend)
**Files**: New component
- [ ] Average XP rate for master
- [ ] Average profit rate
- [ ] Task distribution chart
- [ ] Most common tasks visualization
- [ ] Create `TaskStatsDashboard.tsx` component

#### Task Comparison Tool (Frontend)
- [ ] Compare 2-3 tasks side-by-side
- [ ] Compare XP rates, profit, requirements
- [ ] Visual comparison cards
- [ ] Create `TaskComparison.tsx` component

#### User Stats Integration (Frontend)
**Files**: `SlayerPage.tsx`, new hook
- [ ] Save user stats (slayer level, combat level)
- [ ] Persist in localStorage
- [ ] Auto-apply to all advice requests
- [ ] Stats input component
- [ ] Create `useUserStats.ts` hook

#### Task History/Tracking (Backend + Frontend)
**Files**: New models, new endpoints, new components
- [ ] Track completed tasks
- [ ] Task streak counter
- [ ] Point accumulation history
- [ ] Statistics over time
- [ ] Create database models for task history
- [ ] Create API endpoints for history
- [ ] Create frontend components for tracking

#### Task Favorites/Bookmarks (Frontend)
**Files**: New component, localStorage
- [ ] Mark favorite tasks
- [ ] Quick access to favorites
- [ ] Personal task notes
- [ ] Create `FavoritesManager.tsx` component

### Gear Feature

#### Multi-Loadout Comparison (Frontend)
**Files**: `frontend/src/features/gear/components/`
- [ ] Side-by-side loadout comparison
- [ ] DPS comparison tables
- [ ] Visual diff highlighting

#### DPS Graphs & Visualization (Frontend)
**Files**: `frontend/src/features/gear/components/`
- [ ] Time-to-kill charts
- [ ] Damage distribution graphs
- [ ] Loadout performance over time

#### Advanced Stat Requirement Filtering
**Files**: `backend/services/gear/requirements.py`
- [ ] Filter by quest requirements
- [ ] Achievement requirement filtering
- [ ] Level requirement combinations

#### Gear Set Sharing
**Files**: `backend/api/v1/gear/`, `frontend/src/features/gear/`
- [ ] Shareable gear set URLs
- [ ] Export/import gear sets
- [ ] Public gear set library

### Flipping Feature

#### Price Alerts/Notifications
- [ ] User-configurable price alerts
- [ ] Email/push notifications (requires user accounts)
- [ ] Alert history

#### Historical Price Graphs
**Files**: `frontend/src/features/flipping/components/`
- [ ] Price history visualization
- [ ] Chart library integration (Chart.js/Recharts)
- [ ] Time range selection

#### Export/Import Functionality
**Files**: `frontend/src/features/flipping/utils/`
- [ ] Export flip lists (CSV, JSON)
- [ ] Import saved flips
- [ ] Share flip opportunities

### General

#### User Preferences & Saved Filters
- [ ] Save filter configurations
- [ ] User preferences storage
- [ ] Local storage or user accounts

#### Mobile-Responsive Improvements
**Files**: `frontend/src/`
- [ ] Responsive design enhancements
- [ ] Mobile-optimized UI components
- [ ] Touch-friendly interactions

---

## 🟢 Low Priority (P3) - Nice to Have

### Slayer Feature
- [ ] Task sharing (share recommendations, export to CSV/JSON)
- [ ] Advanced filtering (location requirements, attack style, items needed)
- [ ] Mobile optimization (responsive design, touch-friendly)

### Gear Feature
- [ ] Advanced gear comparison tools
- [ ] Multi-loadout optimization
- [ ] Budget-based recommendations

### Flipping Feature
- [ ] Market trend analysis (price trends, volume analysis, market health metrics)
- [ ] Bulk operations (select multiple flips, bulk export)

### General
- [ ] Offline support (service worker, offline data caching)
- [ ] PWA capabilities (Progressive Web App, installable)
- [ ] Internationalization (i18n) - Multi-language support

---

## 🔧 Technical Debt & Code Quality

### Testing Improvements

#### Test Coverage (P0 - Critical)
**Target**: 85%+ (currently 91%+ ✅)
- [x] Low-coverage service modules (2026-01-28) ✅
  - [x] `backend/services/gear/pricing.py` - Added 10 tests (was 50%)
  - [x] `backend/services/gear/progression.py` - Added 19 tests (was 52.17%)
  - [x] `backend/services/gear/loadouts.py` - Added 20 tests (was 52.78%)
  - [x] `backend/services/wiki_data.py` - Added 12 tests (was 71.43%)
  - [x] `backend/services/gear/utils.py` - Added 7 tests (new)
  - [x] `backend/api/v1/validators.py` - Added 24 tests (was 79.17%)
  - [x] `backend/api/v1/gear/routes/gear_sets.py` - Added 8 tests (was 74.19%)
- [ ] Scripts/testing gaps
  - [ ] `backend/scripts/seed_prices.py` (has tests; ~94% coverage)
  - [ ] `backend/seeds/slayer/seed.py` (seed_slayer_data; has tests in `tests/scripts/test_seed_slayer.py`)
  - [ ] Wiki gear: no standalone script; progression API fetches from wiki
- [x] Wiki sync service testing ✅
  - [x] `backend/services/wiki_client.py` - Added 10 tests (was 18.29%)
  - [x] `backend/services/wiki/client.py` - Added 6 tests (was 28.57%)
  - [ ] `backend/services/wiki/sync.py` (still needs coverage)
- [x] DPS calculation edge cases ✅
  - [x] `backend/services/gear/dps.py` - Added 17 tests (was 12.96%)
  - [x] Test edge cases in DPS calculations
  - [x] Test with various stat combinations
  - [ ] Test special attack handling (if applicable)
- [x] Item stats service ✅
  - [x] `backend/services/item_stats.py` - Added 8 tests (was 31.15%)
- [ ] Frontend component tests
  - [ ] Filter/sort functionality tests
  - [ ] Weight calculation tests
  - [ ] Error handling tests

#### Integration Test Coverage
- [x] E2E smoke test added (`test_smoke.py`) ✅
- [x] Contract tests for flips and gear endpoints ✅
- [ ] Expand E2E test coverage (more endpoints)
- [ ] Test critical user flows
- [ ] Test error scenarios

### Database Improvements

#### Migration Improvements
**Files**: `backend/db/migrations.py`
- [ ] Better migration scripts
- [ ] Rollback support
- [ ] Migration testing

#### Query Optimization
- [ ] Analyze slow queries
- [ ] Add database indexes where needed
- [ ] Optimize JOIN operations
- [ ] Query performance monitoring

#### PostgreSQL Migration Path (P2)
- [ ] Plan migration from SQLite to PostgreSQL
- [ ] Test compatibility
- [ ] Update connection strings

### Code Quality

#### Frontend Linting (ESLint)
- [ ] **Skipped for now**: no `.eslintrc`; `npm run lint` will fail. Re-add config and address issues to re-enable.

#### Frontend Performance
**File**: `frontend/src/features/slayer/hooks/useSlayerTasks.ts`
- [ ] Fix caching: change `staleTime: 0` to reasonable value (e.g., 5 minutes)
- [ ] Fix caching: change `gcTime: 0` to reasonable value (e.g., 10 minutes)
- [ ] Optimize TaskGrid re-renders (use React.memo if needed)

#### Data Consistency (Backend)
**Files**: `backend/services/slayer_data/*.py`
- [ ] Consolidate duplicate task data (e.g., "Black Demons" vs "Black demons")
- [ ] Standardize location data format (all dicts, no strings)
- [ ] Remove legacy format support after migration

#### Standardize Error Handling
- [x] Consistent error response format ✅ (ErrorResponse schema implemented)
- [ ] Custom exception classes (HTTPException handler covers most cases)
- [ ] Error logging standardization

#### Improve Type Safety
- [ ] Add more type hints in backend
- [ ] Strict TypeScript in frontend
- [ ] Type validation at boundaries

### CI/CD Enhancements
- [ ] Add coverage reporting to CI pipeline
- [x] Linting (backend): Ruff + Black pass locally; CI runs both
- [x] Version pinning: Python 3.13 and Node 20 pinned ✅
- [x] CI caching: Poetry and npm dependency caching added ✅
- [ ] Frontend: ESLint skipped (no config); re-enable when config added
- [ ] Add security scanning
- [ ] Run tests on PR
- [ ] Test coverage gates

---

## 📚 Documentation Needs

### API Documentation
- [ ] Enhance OpenAPI/Swagger docs (add request/response examples, error codes)
- [x] Document error handling (standard error response format implemented: `ErrorResponse` schema) ✅
- [ ] Error code reference documentation (HTTP_XXX codes)
- [ ] Rate limiting documentation (rate limits, headers, best practices)

### Developer Documentation
- [ ] Architecture Decision Records (ADRs)
- [ ] Setup guide improvements (detailed development setup, troubleshooting)
- [ ] Contributing guidelines (how to contribute, code style guide, PR process)
- [ ] Testing guide (how to run tests, writing new tests, best practices)

### Code Documentation
- [ ] Improve docstrings (add to all backend functions, follow Google/NumPy style)
- [ ] Add JSDoc comments (document frontend functions, type documentation)
- [ ] Document complex algorithms (DPS calculation formulas, flipping margin calculations, slayer advice algorithms)

### User Documentation
- [ ] Feature usage guides (how to use flipping/gear/slayer features)
- [ ] FAQ section (common questions, troubleshooting)

---

## 🚀 Long-term Vision (6+ months)

### User Features
- [ ] User accounts & authentication (JWT authentication, user profiles)
- [ ] Data persistence (save flip lists, gear sets, task history per user)
- [ ] Portfolio tracking (track flip performance, profit/loss, historical graphs)

### Infrastructure
- [ ] Caching improvements (Redis integration, cache price data, cache gear calculations)
- [ ] Performance optimizations (database query optimization, frontend code splitting, lazy loading)
- [ ] PostgreSQL migration (for production scalability)

### Advanced Features
- [ ] Advanced gear comparison tools (multi-loadout optimization, budget-based recommendations, upgrade path suggestions)
- [ ] Slayer task tracking & history (personal task history, completion statistics, XP tracking)

---

## 📊 Progress Summary

### Overall Status
- **Total Tests**: 350 passing ✅ (248 + 102 new tests)
- **Test Coverage**: 91%+ (target: 85%+ ✅)
- **Backend Refactoring**: 100% complete ✅
- **Frontend Refactoring**: 100% complete ✅
- **Slayer Data Coverage**: ~85% (Nieve 35/41 tasks), improving
- **Test Coverage Improvements**: 102 new tests added for low-coverage modules ✅

### By Category
| Category | Completed | In Progress | Not Started |
|----------|-----------|-------------|-------------|
| High Priority | 15 | 0 | 25+ |
| Medium Priority | 0 | 0 | 20+ |
| Low Priority | 0 | 0 | 10+ |
| Technical Debt | 5 | 0 | 15+ |
| Documentation | 0 | 0 | 10+ |

---

## 🎯 Recommended Implementation Order

### Phase 1: Quick Wins (1-2 days)
1. ✅ Fix type safety issues - **COMPLETED**
2. [ ] Add task filtering (by recommendation, combat level)
3. [ ] Add task sorting (by XP, profit, weight)
4. [ ] Improve caching in hooks

### Phase 2: Core Features (3-5 days)
1. [ ] Task weight calculator with percentages
2. [ ] User stats persistence (localStorage)
3. [ ] Enhanced block/skip visual indicators
4. [ ] Task statistics dashboard

### Phase 3: Advanced Features (1-2 weeks)
1. [ ] Slayer point calculator
2. [ ] Block list optimization algorithm
3. [ ] Task history/tracking
4. [ ] Expand location data (convert remaining string-based locations)

### Phase 4: Critical Improvements (2-4 weeks)
1. [ ] Advanced DPS formulas integration
2. [ ] Price history tracking
3. [ ] Test coverage improvements (maintain 85%+; currently 91%)

---

*Last Updated: 2026-01-28*  
*Consolidated from: TODO.md, STATUS.md, FLIPPING_ISSUES.md, SLAYER_VERIFICATION.md, SLAYER_ANALYSIS.md, SLAYER_PATCHES.md, PATCHES_APPLIED.md, TEST_FIXES.md, roadmap.md, refactor.md, CHANGELOG_2026-01-27.md*
