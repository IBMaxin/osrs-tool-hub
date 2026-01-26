# E2E Integration Tests

Comprehensive end-to-end integration tests for the OSRS Tool Hub API.

## Structure

Tests are organized by feature domain for maintainability and scalability:

```
e2e/
├── __init__.py
├── base.py              # Base test classes with common utilities
├── helpers.py            # Shared test utilities and fixtures
├── slayer/               # Slayer endpoint tests
│   ├── test_masters.py
│   ├── test_tasks.py
│   └── test_advice.py
├── gear/                 # Gear endpoint tests
│   ├── test_gear_sets.py
│   ├── test_suggestions.py
│   ├── test_progression.py
│   └── test_advanced.py
├── flipping/             # Flipping endpoint tests
│   ├── test_opportunities.py
│   ├── test_scanner.py
│   └── test_calculations.py
├── health/               # Health check tests
│   └── test_health.py
└── admin/                # Admin endpoint tests
    └── test_sync.py
```

## Design Principles

1. **Maintainability**: Each test file focuses on a single endpoint or feature
2. **Scalability**: Easy to add new tests without modifying existing files
3. **File Size**: All files are kept under 200 lines of code
4. **Reusability**: Shared utilities in `helpers.py` and base classes in `base.py`
5. **Comprehensiveness**: Full coverage of all API endpoints

## Running Tests

Run all E2E tests:
```bash
pytest backend/tests/e2e -v
```

Run tests for a specific feature:
```bash
pytest backend/tests/e2e/slayer -v
pytest backend/tests/e2e/gear -v
pytest backend/tests/e2e/flipping -v
```

Run with markers:
```bash
pytest -m e2e -v
```

## Test Organization

### Base Classes
- `BaseE2ETest`: Provides common HTTP request methods and assertions

### Helpers
- `assert_successful_response()`: Assert and parse successful responses
- `assert_error_response()`: Assert and parse error responses
- `create_test_item()`: Create test items in database
- `create_test_price_snapshot()`: Create test price data
- `create_test_monster()`: Create test monsters
- `create_test_slayer_task()`: Create test slayer tasks
- `get_task_id_from_response()`: Extract task IDs from responses

## Coverage

### Slayer Endpoints
- ✅ `/api/v1/slayer/masters` - Get slayer masters
- ✅ `/api/v1/slayer/tasks/{master}` - Get tasks for master
- ✅ `/api/v1/slayer/advice/{task_id}` - Get task advice

### Gear Endpoints
- ✅ `/api/v1/gear` - CRUD operations for gear sets
- ✅ `/api/v1/gear/suggestions` - Gear suggestions
- ✅ `/api/v1/gear/progression/{style}` - Gear progression
- ✅ `/api/v1/gear/progression/{style}/{slot}` - Slot progression
- ✅ `/api/v1/gear/wiki-progression/{style}` - Wiki-style progression
- ✅ `/api/v1/gear/preset` - Preset loadouts
- ✅ `/api/v1/gear/best-loadout` - Best loadout calculator
- ✅ `/api/v1/gear/upgrade-path` - Upgrade path recommendations
- ✅ `/api/v1/gear/dps` - DPS calculations

### Flipping Endpoints
- ✅ `/api/v1/flips/opportunities` - Flip opportunities
- ✅ `/api/v1/flipping/scanner` - GE Tracker-style scanner

### Health & Admin
- ✅ `/` - Root endpoint
- ✅ `/health` - Health check
- ✅ `/api/v1/admin/sync-stats` - Admin sync endpoint

## Adding New Tests

1. Identify the feature domain (slayer, gear, flipping, etc.)
2. Create or update the appropriate test file in the domain directory
3. Use `BaseE2ETest` for common functionality
4. Use helpers from `helpers.py` for data creation
5. Keep files under 200 lines - split if needed

## Best Practices

- Use descriptive test names that explain what is being tested
- Test both success and error cases
- Verify response structure and data correctness
- Use fixtures from `conftest.py` for test data
- Keep tests independent - each test should be able to run in isolation
