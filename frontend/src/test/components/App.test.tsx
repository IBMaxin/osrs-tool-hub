/**
 * Tests for App component
 * Verifies navigation and routing functionality
 */

import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '../utils/testUtils'
import App from '../../App'

// Mock the feature components
vi.mock('../../features/flipping/Flipping', () => ({
  Flipping: () => <div>Flipping Page</div>,
}))

vi.mock('../../features/gear/Gear', () => ({
  Gear: () => <div>Gear Page</div>,
}))

vi.mock('../../features/slayer/Slayer', () => ({
  Slayer: () => <div>Slayer Page</div>,
}))

describe('App', () => {
  it('renders navigation links', () => {
    render(<App />)
    
    expect(screen.getByText('Flipping')).toBeInTheDocument()
    expect(screen.getByText('Gear')).toBeInTheDocument()
    expect(screen.getByText('Slayer')).toBeInTheDocument()
  })

  it('displays flipping page by default', () => {
    render(<App />)
    
    expect(screen.getByText('Flipping Page')).toBeInTheDocument()
  })

  it('switches pages when navigation links are clicked', async () => {
    const userEvent = await import('@testing-library/user-event')
    render(<App />)
    
    const gearLink = screen.getByText('Gear')
    await userEvent.default.click(gearLink)
    
    expect(screen.getByText('Gear Page')).toBeInTheDocument()
    expect(screen.queryByText('Flipping Page')).not.toBeInTheDocument()
  })

  it('renders hierarchical dropdown nav with sub-links', () => {
    render(<App />)
    expect(screen.getByText('Scanner')).toBeInTheDocument()
    expect(screen.getByText('Profit Tracker')).toBeInTheDocument()
    expect(screen.getByText('Trade History')).toBeInTheDocument()
    expect(screen.getByText('Loadout Builder')).toBeInTheDocument()
    expect(screen.getByText('DPS Lab')).toBeInTheDocument()
    expect(screen.getByText('Progression')).toBeInTheDocument()
    expect(screen.getByText('Task Advisor')).toBeInTheDocument()
    expect(screen.getByText('Monster Database')).toBeInTheDocument()
  })
})
