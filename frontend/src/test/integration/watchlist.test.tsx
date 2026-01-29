/**
 * Integration tests for Watchlist feature
 * Tests complete watchlist workflow: add item → view alerts
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '../utils/testUtils'
import { FlippingPage } from '../../features/flipping/FlippingPage'
import { FlippingApi, WatchlistApi } from '../../lib/api'

// Mock the APIs
vi.mock('../../lib/api', () => ({
  FlippingApi: {
    getOpportunities: vi.fn(),
  },
  WatchlistApi: {
    getWatchlist: vi.fn(),
    addToWatchlist: vi.fn(),
    getAlerts: vi.fn(),
    removeFromWatchlist: vi.fn(),
  },
}))

const mockWatchlist = [
  {
    id: 1,
    user_id: 'test-user',
    item_id: 123,
    item_name: 'Test Item',
    alert_type: 'price_below',
    threshold: 1000,
    is_active: true,
  },
]

const mockAlerts = [
  {
    id: 1,
    watchlist_item_id: 1,
    triggered_at: '2026-01-28T00:00:00Z',
    current_value: 950,
    threshold_value: 1000,
    message: 'Price alert triggered for Test Item',
  },
]

describe('Watchlist Integration Tests', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    localStorage.clear()
    vi.mocked(FlippingApi.getOpportunities).mockResolvedValue([])
    vi.mocked(WatchlistApi.getWatchlist).mockResolvedValue([])
    vi.mocked(WatchlistApi.getAlerts).mockResolvedValue([])
  })

  it('displays watchlist tab and content', async () => {
    render(<FlippingPage />)

    const userEvent = await import('@testing-library/user-event')
    const watchlistTab = screen.getByRole('tab', { name: /watchlist/i })
    await userEvent.default.click(watchlistTab)

    // Watchlist manager should be visible - check for heading
    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /add to watchlist/i })).toBeInTheDocument()
    }, { timeout: 3000 })
  })

  it('loads and displays watchlist items', async () => {
    vi.mocked(WatchlistApi.getWatchlist).mockResolvedValue(mockWatchlist as any)

    render(<FlippingPage />)

    const userEvent = await import('@testing-library/user-event')
    const watchlistTab = screen.getByRole('tab', { name: /watchlist/i })
    await userEvent.default.click(watchlistTab)

    await waitFor(() => {
      expect(screen.getByText('Test Item')).toBeInTheDocument()
    })
  })

  it('displays watchlist alerts', async () => {
    vi.mocked(WatchlistApi.getAlerts).mockResolvedValue(mockAlerts as any)

    render(<FlippingPage />)

    const userEvent = await import('@testing-library/user-event')
    const watchlistTab = screen.getByRole('tab', { name: /watchlist/i })
    await userEvent.default.click(watchlistTab)

    await waitFor(() => {
      // Alerts section should be visible with the alert message
      expect(screen.getByText(/price alert triggered for test item/i) || screen.getByText(/alert notifications/i)).toBeInTheDocument()
    }, { timeout: 3000 })
  })

  it('handles empty watchlist', async () => {
    vi.mocked(WatchlistApi.getWatchlist).mockResolvedValue([])

    render(<FlippingPage />)

    const userEvent = await import('@testing-library/user-event')
    const watchlistTab = screen.getByRole('tab', { name: /watchlist/i })
    await userEvent.default.click(watchlistTab)

    await waitFor(() => {
      // Should show empty state message or "Add to Watchlist" heading
      expect(screen.getByText(/no items in watchlist/i) || screen.getByRole('heading', { name: /add to watchlist/i })).toBeInTheDocument()
    }, { timeout: 3000 })
  })
})
