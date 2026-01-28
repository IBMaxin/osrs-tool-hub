/**
 * End-to-end integration tests
 * Tests complete user flows across features
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '../utils/testUtils'
import App from '../../App'

// Mock all APIs
vi.mock('../../lib/api', () => ({
  FlippingApi: {
    getOpportunities: vi.fn(),
  },
  SlayerApi: {
    getMasters: vi.fn(),
    getTasks: vi.fn(),
    getAdvice: vi.fn(),
  },
}))

// Mock feature components to avoid complex dependencies
vi.mock('../../features/flipping/Flipping', () => ({
  Flipping: () => <div>Flipping Feature</div>,
}))

vi.mock('../../features/gear/Gear', () => ({
  Gear: () => <div>Gear Feature</div>,
}))

vi.mock('../../features/slayer/Slayer', () => ({
  Slayer: () => <div>Slayer Feature</div>,
}))

describe('E2E Integration Tests', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the full application', () => {
    render(<App />)
    
    expect(screen.getByText('Flipping')).toBeInTheDocument()
    expect(screen.getByText('Gear')).toBeInTheDocument()
    expect(screen.getByText('Slayer')).toBeInTheDocument()
  })

  it('navigates between features', async () => {
    const userEvent = await import('@testing-library/user-event')
    render(<App />)
    
    // Start on Flipping
    expect(screen.getByText('Flipping Feature')).toBeInTheDocument()
    
    // Navigate to Gear
    const gearLink = screen.getByText('Gear')
    await userEvent.default.click(gearLink)
    expect(screen.getByText('Gear Feature')).toBeInTheDocument()
    
    // Navigate to Slayer
    const slayerLink = screen.getByText('Slayer')
    await userEvent.default.click(slayerLink)
    expect(screen.getByText('Slayer Feature')).toBeInTheDocument()
  })
})
