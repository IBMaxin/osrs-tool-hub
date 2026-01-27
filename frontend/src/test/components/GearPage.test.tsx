/**
 * Tests for Gear components
 * Tests gear progression display and wiki table
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '../utils/testUtils'
import { Gear } from '../../features/gear/Gear'

// Mock the gear components
vi.mock('../../features/gear/WikiGearTable', () => ({
  WikiGearTable: () => <div>Wiki Gear Table</div>,
}))

vi.mock('../../features/gear/ProgressionViewer', () => ({
  ProgressionViewer: () => <div>Progression Viewer</div>,
}))

describe('Gear', () => {
  it('renders tabs for different views', () => {
    render(<Gear />)
    
    expect(screen.getByText('Wiki Table View')).toBeInTheDocument()
    expect(screen.getByText('Detailed View')).toBeInTheDocument()
  })

  it('displays wiki table view by default', () => {
    render(<Gear />)
    
    expect(screen.getByText('Wiki Gear Table')).toBeInTheDocument()
  })
})
