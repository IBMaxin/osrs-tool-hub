import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { 
  Tabs, 
  Text, 
  Group, 
  Loader, 
  Stack, 
  Title,
  ScrollArea
} from '@mantine/core';
import { fetchFullProgression, type FullProgressionResponse } from '../../lib/api';
import { SlotProgression } from './components/SlotProgression';
import { SLOT_ORDER } from './constants';

export function ProgressionViewer() {
  const [style, setStyle] = useState<string>("melee");

  const { data, isLoading, error } = useQuery<FullProgressionResponse>({
    queryKey: ['gear-progression-full', style],
    queryFn: () => fetchFullProgression(style),
  });

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
  const sortedSlots = Object.entries(data.slots).sort(
    (a, b) => (SLOT_ORDER[a[0]] || 999) - (SLOT_ORDER[b[0]] || 999)
  );

  return (
    <Stack gap="lg">
      <Group justify="space-between" align="center">
        <Title order={2}>Gear Progression Guide</Title>
        
        <Tabs value={style} onChange={(val) => setStyle(val || "melee")}>
          <Tabs.List>
            <Tabs.Tab value="melee">Melee</Tabs.Tab>
            <Tabs.Tab value="ranged">Ranged</Tabs.Tab>
            <Tabs.Tab value="magic">Magic</Tabs.Tab>
          </Tabs.List>
        </Tabs>
      </Group>

      <Text c="dimmed" size="sm">
        Best-in-Slot → Downgrades for each equipment slot. Click items to view on OSRS Wiki.
        Prices update from live GE data.
      </Text>

      <Tabs defaultValue={sortedSlots[0]?.[0] || "head"}>
        <Tabs.List>
          <ScrollArea type="scroll">
            <Group gap="xs">
              {sortedSlots.map(([slot]) => (
                <Tabs.Tab key={slot} value={slot} tt="capitalize">
                  {slot}
                </Tabs.Tab>
              ))}
            </Group>
          </ScrollArea>
        </Tabs.List>

        {sortedSlots.map(([slot, tiers]) => (
          <Tabs.Panel key={slot} value={slot} pt="md">
            <SlotProgression slot={slot} tiers={tiers as Array<{ tier: string; items: any[] }>} />
          </Tabs.Panel>
        ))}
      </Tabs>
    </Stack>
  );
}
