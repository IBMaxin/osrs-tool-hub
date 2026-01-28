import { Container, Tabs } from '@mantine/core'
import { ProgressionViewer } from './ProgressionViewer'
import { WikiGearTable } from './WikiGearTable'
import { DPSLab } from './components/DPSLab'

export function Gear() {
  return (
    <Container>
      <Tabs defaultValue="wiki-table">
        <Tabs.List>
          <Tabs.Tab value="wiki-table">Wiki Table View</Tabs.Tab>
          <Tabs.Tab value="detailed">Detailed View</Tabs.Tab>
          <Tabs.Tab value="dps-lab">DPS Lab</Tabs.Tab>
        </Tabs.List>

        <Tabs.Panel value="wiki-table" pt="md">
          <WikiGearTable />
        </Tabs.Panel>

        <Tabs.Panel value="detailed" pt="md">
          <ProgressionViewer />
        </Tabs.Panel>

        <Tabs.Panel value="dps-lab" pt="md">
          <DPSLab />
        </Tabs.Panel>
      </Tabs>
    </Container>
  )
}
