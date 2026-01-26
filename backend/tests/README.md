# OSRS Tool Hub Test Suite

Comprehensive end-to-end and integration test suite for the OSRS Tool Hub backend.

## Test Structure

```
backend/tests/
├── conftest.py                    # Shared fixtures and test configuration
├── test_e2e_flipping.py          # E2E tests for flipping endpoints
├── test_e2e_gear.py               # E2E tests for gear endpoints
├── test_e2e_slayer.py            # E2E tests for slayer endpoints
├── test_integration_db_sync.py   # Integration tests for database sync
├── test_integration_full_flow.py # Full workflow integration tests
├── test_flipping.py              # Unit tests for flipping service
├── test_api.py                   # Basic API tests
└── test_slayer.py                # Unit tests for slayer service
```

## Running Tests

### Using the Test Runner Script

```bash
# Run all tests
./run_tests.sh

# Run specific test categories
./run_tests.sh e2e
./run_tests.sh integration
./run_tests.sh flipping
./run_tests.sh gear
./run_tests.sh slayer
./run_tests.sh unit

# Run with coverage
./run_tests.sh coverage
```

### Using Poetry

```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest backend/tests/test_e2e_flipping.py

# Run with verbose output
poetry run pytest -v

# Run specific test
poetry run pytest backend/tests/test_e2e_flipping.py::TestFlippingScannerEndpoint::test_scanner_basic

# Run with markers
poetry run pytest -m e2e
poetry run pytest -m integration
```

### Using pytest directly

```bash
pytest backend/tests/
pytest backend/tests/test_e2e_flipping.py -v
```

## Test Categories

### E2E Tests (`test_e2e_*.py`)

End-to-end tests that test complete API workflows:
- **test_e2e_flipping.py**: Tests for `/api/v1/flips/opportunities` and `/api/v1/flipping/scanner`
- **test_e2e_gear.py**: Tests for all gear endpoints (CRUD, suggestions, progression)
- **test_e2e_slayer.py**: Tests for slayer endpoints (masters, tasks, advice)

### Integration Tests (`test_integration_*.py`)

Integration tests that test component interactions:
- **test_integration_db_sync.py**: Tests database synchronization and price updates
- **test_integration_full_flow.py**: Tests complete user workflows across features

### Unit Tests (`test_*.py`)

Unit tests for individual components:
- **test_flipping.py**: Unit tests for FlippingService
- **test_slayer.py**: Unit tests for SlayerService
- **test_api.py**: Basic API health checks

## Test Fixtures

All tests use fixtures defined in `conftest.py`:

- `session`: Database session with automatic cleanup
- `client`: FastAPI test client
- `sample_items`: Pre-configured items for testing
- `sample_price_snapshots`: Price data for items
- `sample_monsters`: Monsters for slayer tests
- `sample_slayer_tasks`: Slayer tasks for testing

## Writing New Tests

1. Import necessary fixtures from `conftest.py`
2. Use descriptive test class and method names
3. Follow the pattern: Arrange → Act → Assert
4. Use appropriate markers (`@pytest.mark.e2e`, `@pytest.mark.integration`, etc.)

Example:

```python
def test_my_new_endpoint(client: TestClient, session: Session, sample_items: list[Item]):
    """Test description."""
    # Arrange
    # Act
    response = client.get("/api/v1/my/endpoint")
    # Assert
    assert response.status_code == 200
```

## Test Coverage

Run coverage report:

```bash
./run_tests.sh coverage
```

Coverage report will be generated in `htmlcov/index.html`.

## Continuous Integration

Tests are designed to run in CI/CD pipelines. All tests use in-memory SQLite databases and don't require external dependencies.

## Notes

- All tests use isolated in-memory databases
- Tests are automatically cleaned up after each run
- No external API calls are made during testing
- All test data is created using fixtures
