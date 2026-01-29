# Contributing to OSRS Tool Hub

Thank you for your interest in contributing to OSRS Tool Hub! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Code Style Guidelines](#code-style-guidelines)
5. [Testing Requirements](#testing-requirements)
6. [Pull Request Process](#pull-request-process)
7. [Project Structure](#project-structure)
8. [AI Contributors](#ai-contributors)

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Follow the project's coding standards
- Test your changes thoroughly
- Document significant changes

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/osrs-tool-hub.git
   cd osrs-tool-hub
   ```
3. **Set up the development environment** (see [Development Setup](#development-setup))
4. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Prerequisites

- **Python 3.13+** (managed via Poetry)
- **Node.js 20.x** (see `.nvmrc`)
- **Poetry** (Python dependency management)
- **npm** (Node package manager)

### Backend Setup

1. **Install Poetry** (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Install dependencies**:
   ```bash
   poetry install --with dev
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run database migrations**:
   ```bash
   poetry run python -m backend.db.migrations
   ```

5. **Start the backend** (development mode):
   ```bash
   poetry run uvicorn backend.main:app --reload
   ```
   Backend runs on `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the frontend** (development mode):
   ```bash
   npm run dev
   ```
   Frontend runs on `http://localhost:5173`

### Running Both Together

From the frontend directory:
```bash
npm run dev:both
```

This runs both backend and frontend concurrently.

## Code Style Guidelines

### Python (Backend)

- **Type Hints**: All public functions, services, and routes must have type hints
- **Formatting**: Use Black (line length: 100)
- **Linting**: Use Ruff (follows Black's line length)
- **Type Checking**: Use MyPy (strict mode)
- **Docstrings**: Google style for non-trivial public functions

**Format code**:
```bash
poetry run black backend
poetry run ruff check backend --fix
poetry run mypy backend
```

**Example**:
```python
from typing import List, Optional
from sqlmodel import Session

def get_items(
    session: Session,
    limit: Optional[int] = None
) -> List[Item]:
    """
    Get items from database.
    
    Args:
        session: Database session
        limit: Optional limit on number of items
        
    Returns:
        List of Item models
    """
    query = session.query(Item)
    if limit:
        query = query.limit(limit)
    return query.all()
```

### TypeScript (Frontend)

- **Strict Mode**: TypeScript strict mode is required
- **No `any`**: Avoid `any` types (use `unknown` if necessary)
- **No Unsafe Casts**: Avoid `as unknown as` patterns
- **API Client**: All API calls must go through `frontend/src/lib/api/**`
- **Components**: Use functional components with hooks

**Lint and type check**:
```bash
cd frontend
npm run lint
npm run build  # Type checks during build
```

**Example**:
```typescript
import { useQuery } from '@tanstack/react-query';
import { FlippingApi, type FlipOpportunity } from '../../lib/api';

interface FlipTableProps {
  maxBudget: number;
  minRoi: number;
}

export function FlipTable({ maxBudget, minRoi }: FlipTableProps) {
  const { data, isLoading } = useQuery<FlipOpportunity[]>({
    queryKey: ['flips', maxBudget, minRoi],
    queryFn: () => FlippingApi.getOpportunities({ max_budget: maxBudget, min_roi: minRoi }),
  });
  
  // Component implementation
}
```

## Testing Requirements

### Test Coverage

- **Overall Coverage**: 70%+ required (currently 96.7%)
- **Per File**: 85%+ for production code
- **Test Types**: Unit, integration, and E2E tests

### Running Tests

**Backend**:
```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=backend --cov-report=html

# Run specific test file
poetry run pytest backend/tests/test_flipping.py

# Run E2E tests
poetry run pytest -m e2e

# Run integration tests
poetry run pytest -m integration
```

**Frontend**:
```bash
cd frontend

# Run tests
npm run test

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage

# Run tests once (CI mode)
npm run test:run
```

### Writing Tests

**Backend Test Structure**:
```python
import pytest
from sqlmodel import Session
from backend.services.flipping import FlippingService

def test_get_flip_opportunities(session: Session):
    """Test getting flip opportunities."""
    service = FlippingService(session)
    # Create test data
    # Call service method
    # Assert results
```

**Frontend Test Structure**:
```typescript
import { render, screen } from '@testing-library/react';
import { FlipTable } from './FlipTable';

describe('FlipTable', () => {
  it('renders flip opportunities', () => {
    render(<FlipTable maxBudget={1000000} minRoi={1} />);
    // Assertions
  });
});
```

### Test Requirements

All new features must include:
- **Happy path** tests
- **Validation failure** tests
- **Error path** tests (where applicable)
- **Contract tests** for public APIs

## Pull Request Process

### Before Submitting

1. **Ensure tests pass**:
   ```bash
   poetry run pytest
   cd frontend && npm run test:run
   ```

2. **Run linters**:
   ```bash
   poetry run ruff check backend
   poetry run black --check backend
   poetry run mypy backend
   cd frontend && npm run lint
   ```

3. **Update documentation** if needed
4. **Update CHANGELOG.md** for user-facing changes

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Tests added/updated and passing
- [ ] Test coverage maintained (70%+ overall, 85%+ per file)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (if applicable)
- [ ] No breaking changes (or documented if necessary)
- [ ] Backward compatibility maintained

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] E2E tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] No breaking changes
```

### Review Process

1. **Automated Checks**: CI runs tests, linters, and type checks
2. **Code Review**: At least one maintainer must approve
3. **Merge**: Squash and merge preferred for clean history

## Project Structure

### Backend Structure

```
backend/
├── api/v1/              # API routes (thin layer only)
│   ├── flips.py
│   ├── gear/
│   └── slayer.py
├── services/            # Business logic
│   ├── flipping.py
│   ├── gear/
│   └── slayer.py
├── models/              # SQLModel database models
├── db/                  # Database configuration
│   ├── session.py
│   └── migrations.py
├── app/                 # Application factory and lifecycle
│   ├── factory.py
│   ├── lifespan.py
│   └── middleware.py
└── tests/               # Test suite
    ├── services/        # Unit tests
    ├── api/             # API/contract tests
    └── e2e/             # E2E tests
```

**Rules**:
- Routes are thin: `request → validate → service → response`
- Business logic goes in `services/`
- Database models in `models/`
- No business logic in routes

### Frontend Structure

```
frontend/src/
├── features/            # Feature modules
│   ├── flipping/
│   ├── gear/
│   └── slayer/
├── lib/                 # Shared utilities
│   ├── api/            # Typed API client
│   ├── components/     # Shared components
│   └── hooks/          # Shared hooks
└── theme/              # Theme configuration
```

**Rules**:
- Features are self-contained
- API calls through `lib/api/**`
- Shared code in `lib/`
- No direct fetch/axios in components

## Important Rules

### Backward Compatibility

- **Never remove or rename**:
  - API routes
  - Request/response fields
  - Shared TypeScript types
- Changes must be **additive only** unless explicitly approved

### Error Handling

- All errors must conform to `ErrorResponse` / `ErrorDetail` schema
- Routes must declare `response_model`
- No alternative error formats

### No Cleanup Refactors

- Don't reformat files "for clarity"
- Don't rename symbols unless necessary
- Don't reorganize folders
- Only touch what the task requires

### Database Changes

- Use migrations for schema changes
- Never make silent schema changes
- Test migrations thoroughly
- Document breaking changes

## AI Contributors

If you're an AI assistant contributing to this project, see [AGENTS.md](AGENTS.md) for detailed guidelines on:
- Operating modes (ANALYSIS_ONLY, SAFE_PATCH, FEATURE_ADD)
- Required workflows (PLAN → ACT → VERIFY → REVISE)
- Release-safe feature checklist
- Prohibited changes

## Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Open an Issue with reproduction steps
- **Feature Requests**: Open an Issue with use case description
- **Security Issues**: See [SECURITY.md](SECURITY.md)

## Versioning

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

Version numbers are managed in:
- `pyproject.toml` (backend)
- `frontend/package.json` (frontend)

---

Thank you for contributing to OSRS Tool Hub! 🎮
