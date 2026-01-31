import { useState } from 'react'
import { Container, Tabs } from '@mantine/core'
import { ProgressionViewer } from './ProgressionViewer'
import { WikiGearTable } from './WikiGearTable'
import { WikiGuideView } from './WikiGuideView'
import { DPSLab } from './components/DPSLab'

export function Gear() {
  const [activeTab, setActiveTab] = useState<string>('wiki-guide')

  return (
    <Container size="xl">
      <Tabs value={activeTab} onChange={(value) => setActiveTab(value || 'wiki-guide')}>
        <Tabs.List>
          <Tabs.Tab value="wiki-guide">Wiki Guide (Exact)</Tabs.Tab>
          <Tabs.Tab value="wiki-table">Wiki Table View</Tabs.Tab>
          <Tabs.Tab value="detailed">Detailed View</Tabs.Tab>
          <Tabs.Tab value="dps-lab">DPS Lab</Tabs.Tab>
        </Tabs.List>

        <Tabs.Panel value="wiki-guide" pt="md">
          {activeTab === 'wiki-guide' && <WikiGuideView />}
        </Tabs.Panel>

        <Tabs.Panel value="wiki-table" pt="md">
          <WikiGearTable />
        </Tabs.Panel>

        <Tabs.Panel value="detailed" pt="md">
          <ProgressionViewer />
        </Tabs.Panel>

        <Tabs.Panel value="dps-lab" pt="md">
          {activeTab === 'dps-lab' && <DPSLab />}
        </Tabs.Panel>
      </Tabs>
    </Container>
  )
}
