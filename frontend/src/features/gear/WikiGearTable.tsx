import { useState } from 'react';
import { 
  Table, Text, Group, Stack, SegmentedControl, 
  Card, Loader
} from '@mantine/core';
import { SLOT_ORDER, type TierGroup } from './utils/wikiGearHelpers';
import { WikiTierRow } from './components/WikiTierRow';
import { useWikiGearProgression } from './hooks/useWikiGearProgression';

export function WikiGearTable() {
  const [style, setStyle] = useState("melee");
  
  const { data, isLoading, error } = useWikiGearProgression({ style });

  if (isLoading) {
    return (
      <Stack align="center" gap="md" py="xl">
        <Loader size="xl" />
        <Text c="dimmed">Loading gear progression...</Text>
      </Stack>
    );
  }

  if (error) {
    return (
      <Stack align="center" gap="md" py="xl">
        <Text c="red" fw={500}>Error loading progression data</Text>
        <Text c="dimmed" size="sm">{String(error)}</Text>
      </Stack>
    );
  }

  if (!data) {
    return null;
  }

  // Sort slots by order
  const sortedSlots = Object.entries(data).sort(
    (a, b) => (SLOT_ORDER[a[0]] || 999) - (SLOT_ORDER[b[0]] || 999)
  );

  return (
    <Stack gap="lg">
      <Group justify="space-between" align="center" wrap="wrap">
        <Text size="xl" fw={700}>OSRS Wiki Gear Progression</Text>
        <SegmentedControl
          value={style}
          onChange={setStyle}
          data={[
            { label: 'Melee', value: 'melee' },
            { label: 'Ranged', value: 'ranged' },
            { label: 'Magic', value: 'magic' },
          ]}
          color="yellow"
        />
      </Group>

      <Card withBorder padding={0} radius="md" style={{ overflow: 'hidden' }}>
        <Table.ScrollContainer minWidth={800}>
          <Table striped highlightOnHover verticalSpacing="md">
            <Table.Thead bg="gray.1">
              <Table.Tr>
                <Table.Th w={120}>Slot</Table.Th>
                <Table.Th>Progression Path (Best → Worst)</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {sortedSlots.map(([slot, tiers]) => {
                const typedTiers = tiers as TierGroup[];
                return (
                <Table.Tr key={slot}>
                  <Table.Td fw={700} tt="capitalize" fz="lg" style={{ verticalAlign: 'top', paddingTop: '1rem' }}>
                    {slot}
                  </Table.Td>
                  <Table.Td>
                    <Stack gap="sm" py="xs">
                      {typedTiers.map((tier: TierGroup) => (
                        <WikiTierRow key={tier.tier} tier={tier} />
                      ))}
                    </Stack>
                  </Table.Td>
                </Table.Tr>
                );
              })}
            </Table.Tbody>
          </Table>
        </Table.ScrollContainer>
      </Card>
    </Stack>
  );
}
