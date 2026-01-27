# Testing Guide

## Overview

The frontend uses **Vitest** for testing with **React Testing Library** for component testing.

## Quick Start

```bash
# Install dependencies (if not already done)
npm install

# Run tests
npm run test

# Run tests once (for CI)
npm run test:run

# Run tests with coverage
npm run test:coverage
```

## Test Structure

- **Component Tests**: `src/test/components/` - Unit tests for React components
- **Integration Tests**: `src/test/integration/` - API and integration tests
- **Test Utilities**: `src/test/utils/` - Shared test helpers
- **Mocks**: `src/test/mocks/` - Mock implementations

## Test Configuration

- **Vitest Config**: `vitest.config.ts`
- **Test Setup**: `src/test/setup.ts` - Global test configuration
- **Custom Render**: `src/test/utils/testUtils.tsx` - Wrapper with providers

## Writing Tests

### Component Test Example

```typescript
import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '../utils/testUtils'
import { MyComponent } from '../../components/MyComponent'

describe('MyComponent', () => {
  it('renders correctly', () => {
    render(<MyComponent />)
    expect(screen.getByText('Hello')).toBeInTheDocument()
  })
})
```

### API Mocking

```typescript
import { vi } from 'vitest'
import { MyApi } from '../../lib/api'

vi.mock('../../lib/api', () => ({
  MyApi: {
    getData: vi.fn(),
  },
}))

// In test
vi.mocked(MyApi.getData).mockResolvedValue(mockData)
```

## CI Integration

Tests run automatically in GitHub Actions:
- Frontend linting
- Type checking
- Test execution

See `.github/workflows/ci.yml` for details.

## Coverage

Generate coverage reports:
```bash
npm run test:coverage
```

Coverage reports are generated in `coverage/` directory.
