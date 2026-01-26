# Refactor plan: modularization review (no code changes yet)

This document summarizes a scan of the entire repository and proposes a
modularization plan to split large files into smaller, single-responsibility
modules. No code changes are included here.

## Scope and constraints
- Goal: improve maintainability by decomposing large files and clarifying
  boundaries between API, services, models, and UI components.
- Constraint: do not edit or change any code in this iteration.
- Output: planning-only guidance for future refactors.

## Repository scan summary

### Backend (FastAPI + SQLModel)
Key files scanned:
- backend/main.py (app setup, lifespan, scheduler, seeding)
- backend/models.py (all ORM models and enums)
- backend/database.py (engine, migrations, session)
- backend/api/v1/*.py (flips, gear, slayer endpoints)
- backend/services/*.py (flipping, gear, slayer, wiki client, wiki data)
- backend/scripts/*.py (seeders and data checks)
- backend/tests/*.py (API/service tests)

Primary modularization hotspots:
- backend/services/gear.py (multiple concerns: scoring, pricing, DPS,
  presets, progression, requirements, loadout selection)
- backend/api/v1/gear.py (many endpoints + request/response models + mapping)
- backend/services/wiki_data.py (large static data structure)
- backend/models.py (all models and enums in one file)
- backend/main.py (app bootstrap plus scheduling and seeding)
- backend/scripts/seed_slayer.py (large data and seeding logic)

### Frontend (React + Vite + TypeScript)
Key files scanned:
- frontend/src/App.tsx and main.tsx
- frontend/src/features/flipping/*.tsx
- frontend/src/features/gear/*.tsx
- frontend/src/features/slayer/*.tsx
- frontend configuration (vite.config.ts, tsconfig*)

Primary modularization hotspots:
- FlippingPage.tsx (large UI, filters, sorting, and formatting)
- SlayerPage.tsx (large UI, data fetching, modal rendering, debug logs)
- ProgressionViewer.tsx and WikiGearTable.tsx (large UI + helpers)
- TaskCard.tsx (large UI + image/url formatting logic)

Notable structural gap:
- UI code imports from frontend/src/lib/api, but that directory is not present
  in the current workspace layout. This should be addressed during refactor.

## Backend modularization plan

### 1) Split backend/models.py into a package
Current: all enums and models in backend/models.py.
Proposed:
```
backend/models/
  __init__.py        # re-export public models/enums
  enums.py           # SlayerMaster, AttackStyle
  items.py           # Item, PriceSnapshot
  gear.py            # GearSet
  flipping.py        # Flip
  slayer.py          # Monster, SlayerTask
```
Benefits: clearer ownership, easier imports, smaller files.

### 2) Split backend/main.py into app lifecycle modules
Current: app creation, router mounting, scheduler, seeding in one file.
Proposed:
```
backend/app/
  __init__.py
  factory.py         # create_app()
  lifespan.py        # startup/shutdown tasks
  scheduler.py       # APScheduler configuration/jobs
  routers.py         # include_router wiring
backend/main.py       # minimal entrypoint -> create_app()
```
Benefits: testable startup logic and isolated scheduler behavior.

### 3) Split backend/database.py by responsibility
Current: engine, migration checks, session in one file.
Proposed:
```
backend/db/
  __init__.py
  engine.py          # engine creation and settings
  session.py         # get_session dependency
  migrations.py      # migrate_tables and schema checks
```
Benefits: clearer DB layer boundaries, simpler dependency injection.

### 4) Split backend/api/v1/gear.py into router + schemas + mappers
Current: many endpoints, request/response models, transformations.
Proposed:
```
backend/api/v1/gear/
  __init__.py
  router.py          # APIRouter and endpoint definitions
  schemas.py         # GearSetCreate, GearSetResponse, request models
  mappers.py         # response transforms and DTO conversions
  validators.py      # combat_style/tier validation helpers
```
Repeat pattern for flips.py and slayer.py if they grow.

### 5) Split backend/services/gear.py into focused modules
Current: large monolith handling pricing, requirements, scoring, DPS,
presets, progression, and selection.
Proposed:
```
backend/services/gear/
  __init__.py
  service.py         # orchestration and public service API
  pricing.py         # PriceSnapshot lookup and item pricing logic
  scoring.py         # item scoring per combat style
  requirements.py    # quest/achievement/stat checks
  loadouts.py        # best loadout and upgrade path selection
  dps.py             # DPS calculation
  presets.py         # static GEAR_PRESETS
  progression.py     # wiki progression enrichment
```
Benefits: explicit functional boundaries, easier test coverage.

### 6) Move static progression data out of code
Current: backend/services/wiki_data.py is a huge Python dict.
Proposed:
```
backend/data/wiki_progression/
  melee.json
  ranged.json
  magic.json
backend/services/wiki_data.py  # loader + accessors only
```
Benefits: slimmer code, easier updates, avoids massive diffs.

### 7) Reorganize scripts and seeds
Current: seed_slayer.py is large and embeds data.
Proposed:
```
backend/seeds/slayer/
  __init__.py
  monsters.py        # monster definitions
  tasks.py           # task definitions by master
  seed.py            # seed_slayer_data entrypoint
backend/scripts/     # thin wrappers to call seed modules
```
Benefits: reusable data definitions, clearer seeding logic.

### 8) Wiki client split
Current: backend/services/wiki_client.py includes API and DB sync logic.
Proposed:
```
backend/services/wiki/
  __init__.py
  client.py          # HTTP client and raw API calls
  sync.py            # sync_items_to_db and sync_prices_to_db
```
Benefits: testability of API calls vs DB sync behavior.

## Frontend modularization plan

### 1) Establish a shared API client module
Current: components import from ../../lib/api (missing).
Proposed:
```
frontend/src/lib/api/
  client.ts          # axios instance and base config
  index.ts           # shared exports
frontend/src/lib/types/  # shared API types if needed
```
Benefits: consistent HTTP behavior, typed API boundaries.

### 2) Feature-first split with hooks, components, types, utils
Proposed structure:
```
frontend/src/features/flipping/
  api.ts
  types.ts
  hooks/useFlips.ts
  utils/format.ts
  components/
    FlippingPage.tsx
    FiltersBar.tsx
    FlipsTable.tsx

frontend/src/features/gear/
  api.ts
  types.ts
  constants.ts       # SLOT_ORDER, etc
  utils/format.ts
  components/
    ProgressionViewer.tsx
    SlotProgression.tsx
    ItemCard.tsx
    WikiGearTable.tsx

frontend/src/features/slayer/
  api.ts
  types.ts
  hooks/useSlayerMasters.ts
  hooks/useSlayerTasks.ts
  components/
    SlayerPage.tsx
    TaskCard.tsx
    AdviceModal.tsx
    MasterSelector.tsx
  utils/monsterImages.ts
```
Benefits: fewer mega-components, simpler testing, clearer ownership.

### 3) Decompose large components
Targets:
- FlippingPage.tsx -> FiltersBar, ResultsTable, empty/error states, format utils
- SlayerPage.tsx -> MasterSelector, TaskGrid, AdviceModal, error blocks
- ProgressionViewer.tsx -> ItemCard, SlotProgression, helpers in utils/constants
- TaskCard.tsx -> image URL logic in utils, UI component kept focused

### 4) Consolidate formatting helpers
Current: repeated formatPrice/formatGP helpers.
Proposed: per-feature utils or shared `lib/format.ts` to avoid duplication.

## Recommended sequencing (no code changes yet)
1) Backend: split models and services into packages (small, safe moves).
2) Backend: split API routers and schemas; update imports.
3) Backend: move wiki progression data to JSON and add loaders.
4) Frontend: create lib/api client and feature-level api modules.
5) Frontend: split large components into smaller components and hooks.
6) Tests: update import paths and add unit tests for new helper modules.

## Definition of done for the refactor
- No single module handles multiple unrelated concerns.
- Feature folders have API, types, hooks, components, and utils.
- Backend services have focused modules with clear interfaces.
- Static data is isolated from business logic.
- Tests pass and remain colocated with the responsible feature/service.
