import { AppShell, Badge, Box, Burger, NavLink, Stack } from '@mantine/core'
import { useDisclosure } from '@mantine/hooks'
import { useState } from 'react'
import { Flipping } from './features/flipping/Flipping'
import { Gear } from './features/gear/Gear'
import { Slayer } from './features/slayer/Slayer'
import { SkipLink } from './lib/components/SkipLink'

function App() {
  const [activeTab, setActiveTab] = useState<string>('flipping/scanner')
  const [opened, { toggle, close }] = useDisclosure()

  const handleNavClick = (tab: string) => {
    setActiveTab(tab)
    close() // Close drawer on mobile after navigation
  }

  return (
    <>
      <SkipLink targetId="main-content">Skip to main content</SkipLink>
      <AppShell
        header={{ height: { base: 60, sm: 0 } }}
        navbar={{
          width: 200,
          breakpoint: 'sm',
          collapsed: { mobile: !opened },
        }}
      >
        <AppShell.Header hiddenFrom="sm">
          <Box p="md" style={{ display: 'flex', alignItems: 'center' }}>
            <Burger
              opened={opened}
              onClick={toggle}
              aria-label="Toggle navigation menu"
              size="sm"
            />
            <Box ml="md" style={{ fontWeight: 700, color: '#FFE799', fontSize: '18px' }}>
              OSRS Tool Hub
            </Box>
          </Box>
        </AppShell.Header>

        <AppShell.Navbar>
          <Box component="nav" aria-label="Main navigation" role="navigation">
            <Stack gap={0}>
              <NavLink
                label="Flipping"
                description="Find and track flips"
                childrenOffset={28}
                defaultOpened={activeTab.startsWith('flipping')}
                active={activeTab.startsWith('flipping')}
                onClick={() => handleNavClick('flipping/scanner')}
                aria-label="Flipping tools - Find and track flip opportunities"
                aria-expanded={activeTab.startsWith('flipping')}
              >
                <NavLink
                  label="Scanner"
                  active={activeTab === 'flipping/scanner'}
                  onClick={() => handleNavClick('flipping/scanner')}
                  aria-label="Flip scanner - Find profitable items to flip"
                  aria-current={activeTab === 'flipping/scanner' ? 'page' : undefined}
                />
                <NavLink
                  label="Profit Tracker"
                  active={activeTab === 'flipping/tracker'}
                  onClick={() => handleNavClick('flipping/tracker')}
                  rightSection={<Badge size="xs" color="profit" variant="light" aria-label="New feature">New</Badge>}
                  aria-label="Profit tracker - Track your flipping profits"
                  aria-current={activeTab === 'flipping/tracker' ? 'page' : undefined}
                />
                <NavLink
                  label="Trade History"
                  active={activeTab === 'flipping/history'}
                  onClick={() => handleNavClick('flipping/history')}
                  aria-label="Trade history - View your past trades"
                  aria-current={activeTab === 'flipping/history' ? 'page' : undefined}
                />
              </NavLink>

              <NavLink
                label="Gear"
                description="Build and compare loadouts"
                childrenOffset={28}
                defaultOpened={activeTab.startsWith('gear')}
                active={activeTab.startsWith('gear')}
                onClick={() => handleNavClick('gear/builder')}
                aria-label="Gear tools - Build and compare loadouts"
                aria-expanded={activeTab.startsWith('gear')}
              >
                <NavLink
                  label="Loadout Builder"
                  active={activeTab === 'gear/builder'}
                  onClick={() => handleNavClick('gear/builder')}
                  aria-label="Loadout builder - Create custom gear setups"
                  aria-current={activeTab === 'gear/builder' ? 'page' : undefined}
                />
                <NavLink
                  label="DPS Lab"
                  active={activeTab === 'gear/dps-lab'}
                  onClick={() => handleNavClick('gear/dps-lab')}
                  rightSection={<Badge size="xs" color="warning" variant="light" aria-label="Beta feature">Beta</Badge>}
                  aria-label="DPS lab - Compare damage per second across loadouts"
                  aria-current={activeTab === 'gear/dps-lab' ? 'page' : undefined}
                />
                <NavLink
                  label="Progression"
                  active={activeTab === 'gear/progression'}
                  onClick={() => handleNavClick('gear/progression')}
                  aria-label="Gear progression - View gear upgrade paths"
                  aria-current={activeTab === 'gear/progression' ? 'page' : undefined}
                />
              </NavLink>

              <NavLink
                label="Slayer"
                description="Task management & advice"
                childrenOffset={28}
                defaultOpened={activeTab.startsWith('slayer')}
                active={activeTab.startsWith('slayer')}
                onClick={() => handleNavClick('slayer/advisor')}
                aria-label="Slayer tools - Task management and advice"
                aria-expanded={activeTab.startsWith('slayer')}
              >
                <NavLink
                  label="Task Advisor"
                  active={activeTab === 'slayer/advisor'}
                  onClick={() => handleNavClick('slayer/advisor')}
                  aria-label="Task advisor - Get advice on slayer tasks"
                  aria-current={activeTab === 'slayer/advisor' ? 'page' : undefined}
                />
                <NavLink
                  label="Monster Database"
                  active={activeTab === 'slayer/monsters'}
                  onClick={() => handleNavClick('slayer/monsters')}
                  aria-label="Monster database - Browse slayer monsters"
                  aria-current={activeTab === 'slayer/monsters' ? 'page' : undefined}
                />
              </NavLink>
            </Stack>
          </Box>
        </AppShell.Navbar>

        <AppShell.Main>
          <Box id="main-content" tabIndex={-1} component="main" role="main" aria-label="Main content">
            {activeTab.startsWith('flipping') && <Flipping />}
            {activeTab.startsWith('gear') && <Gear />}
            {activeTab.startsWith('slayer') && <Slayer />}
          </Box>
        </AppShell.Main>
      </AppShell>
    </>
  )
}

export default App
