import { AppShell, Badge, NavLink, Stack } from '@mantine/core'
import { useState } from 'react'
import { Flipping } from './features/flipping/Flipping'
import { Gear } from './features/gear/Gear'
import { Slayer } from './features/slayer/Slayer'

function App() {
  const [activeTab, setActiveTab] = useState<string>('flipping/scanner')

  return (
    <AppShell
      navbar={{
        width: 200,
        breakpoint: 'sm',
      }}
    >
      <AppShell.Navbar>
        <Stack gap={0}>
          <NavLink
            label="Flipping"
            description="Find and track flips"
            childrenOffset={28}
            defaultOpened={activeTab.startsWith('flipping')}
            active={activeTab.startsWith('flipping')}
            onClick={() => setActiveTab('flipping/scanner')}
          >
            <NavLink
              label="Scanner"
              active={activeTab === 'flipping/scanner'}
              onClick={() => setActiveTab('flipping/scanner')}
            />
            <NavLink
              label="Profit Tracker"
              active={activeTab === 'flipping/tracker'}
              onClick={() => setActiveTab('flipping/tracker')}
              rightSection={<Badge size="xs" color="profit" variant="light">New</Badge>}
            />
            <NavLink
              label="Trade History"
              active={activeTab === 'flipping/history'}
              onClick={() => setActiveTab('flipping/history')}
            />
          </NavLink>

          <NavLink
            label="Gear"
            description="Build and compare loadouts"
            childrenOffset={28}
            defaultOpened={activeTab.startsWith('gear')}
            active={activeTab.startsWith('gear')}
            onClick={() => setActiveTab('gear/builder')}
          >
            <NavLink
              label="Loadout Builder"
              active={activeTab === 'gear/builder'}
              onClick={() => setActiveTab('gear/builder')}
            />
            <NavLink
              label="DPS Lab"
              active={activeTab === 'gear/dps-lab'}
              onClick={() => setActiveTab('gear/dps-lab')}
              rightSection={<Badge size="xs" color="warning" variant="light">Beta</Badge>}
            />
            <NavLink
              label="Progression"
              active={activeTab === 'gear/progression'}
              onClick={() => setActiveTab('gear/progression')}
            />
          </NavLink>

          <NavLink
            label="Slayer"
            description="Task management & advice"
            childrenOffset={28}
            defaultOpened={activeTab.startsWith('slayer')}
            active={activeTab.startsWith('slayer')}
            onClick={() => setActiveTab('slayer/advisor')}
          >
            <NavLink
              label="Task Advisor"
              active={activeTab === 'slayer/advisor'}
              onClick={() => setActiveTab('slayer/advisor')}
            />
            <NavLink
              label="Monster Database"
              active={activeTab === 'slayer/monsters'}
              onClick={() => setActiveTab('slayer/monsters')}
            />
          </NavLink>
        </Stack>
      </AppShell.Navbar>

      <AppShell.Main>
        {activeTab.startsWith('flipping') && <Flipping />}
        {activeTab.startsWith('gear') && <Gear />}
        {activeTab.startsWith('slayer') && <Slayer />}
      </AppShell.Main>
    </AppShell>
  )
}

export default App
