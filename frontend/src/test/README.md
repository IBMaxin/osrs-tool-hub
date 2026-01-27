# Frontend Testing

This directory contains tests for the OSRS Tool Hub frontend application.

## Test Structure

```
src/test/
├── setup.ts              # Test environment setup
├── utils/
│   └── testUtils.tsx     # Custom render utilities
├── mocks/
│   └── apiClient.ts      # API mocking utilities
├── components/           # Component unit tests
└── integration/          # Integration and E2E tests
```

## Running Tests

```bash
# Run tests in watch mode
npm run test

# Run tests with UI
npm run test:ui

# Run tests once (CI mode)
npm run test:run

# Run tests with coverage
npm run test:coverage
```

## Test Types

### Component Tests
- Test individual React components in isolation
- Mock dependencies and API calls
- Verify rendering and user interactions

### Integration Tests
- Test API client configuration
- Test component interactions
- Verify data flow

### E2E Tests
- Test complete user flows
- Test navigation between features
- Verify end-to-end functionality

## Writing Tests

### Example Component Test

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

### Mocking APIs

```typescript
import { vi } from 'vitest'
import { MyApi } from '../../lib/api'

vi.mock('../../lib/api', () => ({
  MyApi: {
    getData: vi.fn(),
  },
}))

// In your test
vi.mocked(MyApi.getData).mockResolvedValue(mockData)
```

## Best Practices

1. **Keep tests focused**: Test one thing per test
2. **Use descriptive names**: Test names should describe what they test
3. **Mock external dependencies**: Don't make real API calls in tests
4. **Test user interactions**: Use `@testing-library/user-event` for clicks, typing, etc.
5. **Clean up**: Tests should clean up after themselves
6. **Stay under 250 lines**: Follow the project's file size limit
