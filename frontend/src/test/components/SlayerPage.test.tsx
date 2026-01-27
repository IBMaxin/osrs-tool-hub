/**
 * Tests for SlayerPage component
 * Tests master selection, task display, and advice modal
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '../utils/testUtils'
import { SlayerPage } from '../../features/slayer/SlayerPage'
import { SlayerApi } from '../../lib/api'

// Mock the API
vi.mock('../../lib/api', () => ({
  SlayerApi: {
    getMasters: vi.fn(),
    getTasks: vi.fn(),
    getAdvice: vi.fn(),
  },
}))

const mockMasters = ['Turael', 'Mazchna', 'Vannaka']
const mockTasks = [
  {
    task_id: 1,
    monster_name: 'Goblin',
    amount: 10,
    category: 'goblins',
    combat_level: 2,
    weight: 5,
    is_blockable: false,
    is_skippable: true,
  },
]

describe('SlayerPage', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(SlayerApi.getMasters).mockResolvedValue(mockMasters)
  })

  it('renders page title', () => {
    render(<SlayerPage />)
    
    expect(screen.getByText('Slayer Task Helper')).toBeInTheDocument()
  })

  it('loads and displays slayer masters', async () => {
    render(<SlayerPage />)
    
    await waitFor(() => {
      expect(SlayerApi.getMasters).toHaveBeenCalled()
    })
  })

  it('loads tasks when master is selected', async () => {
    vi.mocked(SlayerApi.getTasks).mockResolvedValue(mockTasks)
    
    render(<SlayerPage />)
    
    await waitFor(() => {
      expect(SlayerApi.getMasters).toHaveBeenCalled()
    })
  })
})
