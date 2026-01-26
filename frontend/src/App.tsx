import { AppShell, NavLink, Stack } from '@mantine/core'
import { useState } from 'react'
import { Flipping } from './features/flipping/Flipping'
import { Gear } from './features/gear/Gear'
import { Slayer } from './features/slayer/Slayer'

function App() {
  const [activeTab, setActiveTab] = useState<string>('flipping')

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
            active={activeTab === 'flipping'}
            onClick={() => setActiveTab('flipping')}
          />
          <NavLink
            label="Gear"
            active={activeTab === 'gear'}
            onClick={() => setActiveTab('gear')}
          />
          <NavLink
            label="Slayer"
            active={activeTab === 'slayer'}
            onClick={() => setActiveTab('slayer')}
          />
        </Stack>
      </AppShell.Navbar>

      <AppShell.Main>
        {activeTab === 'flipping' && <Flipping />}
        {activeTab === 'gear' && <Gear />}
        {activeTab === 'slayer' && <Slayer />}
      </AppShell.Main>
    </AppShell>
  )
}

export default App
