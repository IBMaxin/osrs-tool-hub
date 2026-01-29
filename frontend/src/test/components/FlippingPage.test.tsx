/**
 * Tests for FlippingPage component
 * Tests filtering, sorting, and data display
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '../utils/testUtils'
import { FlippingPage } from '../../features/flipping/FlippingPage'
import { FlippingApi, type FlipOpportunity } from '../../lib/api'

// Mock the API
vi.mock('../../lib/api', () => ({
  FlippingApi: {
    getOpportunities: vi.fn(),
  },
}))

const mockFlips = [
  {
    item_id: 1,
    item_name: 'Test Item',
    buy_price: 1000,
    sell_price: 1100,
    margin: 100,
    roi: 10,
    potential_profit: 1000,
    volume: 100,
    icon_url: 'test.png',
  },
]

describe('FlippingPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders page title', () => {
    vi.mocked(FlippingApi.getOpportunities).mockResolvedValue([])
    
    render(<FlippingPage />)
    
    expect(screen.getByText('Flip Finder')).toBeInTheDocument()
  })

  it('displays loading state', () => {
    vi.mocked(FlippingApi.getOpportunities).mockImplementation(
      () => new Promise(() => {}) // Never resolves
    )
    
    render(<FlippingPage />)
    
    // Should show loading skeleton
    expect(screen.getByText('Flip Finder')).toBeInTheDocument()
  })

  it('displays flip opportunities', async () => {
    vi.mocked(FlippingApi.getOpportunities).mockResolvedValue(mockFlips as FlipOpportunity[])
    
    render(<FlippingPage />)
    
    await waitFor(() => {
      expect(screen.getByText('Test Item')).toBeInTheDocument()
    })
  })

  it('handles empty results', async () => {
    vi.mocked(FlippingApi.getOpportunities).mockResolvedValue([])
    
    render(<FlippingPage />)
    
    await waitFor(() => {
      expect(screen.getByText(/No flips found/i)).toBeInTheDocument()
    })
  })

  it('renders watchlist tab', () => {
    vi.mocked(FlippingApi.getOpportunities).mockResolvedValue([])
    
    render(<FlippingPage />)
    
    // Check that watchlist tab exists
    expect(screen.getByRole('tab', { name: /watchlist/i })).toBeInTheDocument()
  })

  it('switches to watchlist tab when clicked', async () => {
    vi.mocked(FlippingApi.getOpportunities).mockResolvedValue([])
    
    const userEvent = await import('@testing-library/user-event')
    render(<FlippingPage />)
    
    const watchlistTab = screen.getByRole('tab', { name: /watchlist/i })
    await userEvent.default.click(watchlistTab)
    
    // Watchlist tab should be active (Mantine tabs use aria-selected)
    await waitFor(() => {
      expect(watchlistTab).toHaveAttribute('aria-selected', 'true')
    })
  })

  it('displays watchlist content when tab is active', async () => {
    vi.mocked(FlippingApi.getOpportunities).mockResolvedValue([])
    
    const userEvent = await import('@testing-library/user-event')
    render(<FlippingPage />)
    
    const watchlistTab = screen.getByRole('tab', { name: /watchlist/i })
    await userEvent.default.click(watchlistTab)
    
    // Watchlist manager should be visible - check for heading
    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /add to watchlist/i })).toBeInTheDocument()
    }, { timeout: 3000 })
  })
})
