import { Stack, Title, Grid } from '@mantine/core';
import type { ProgressionItem } from '../../../lib/api/index';
import { ItemCard } from './ItemCard';

interface SlotProgressionProps {
  slot: string;
  tiers: Array<{ tier: string; items: ProgressionItem[] }>;
}

export function SlotProgression({ slot, tiers }: SlotProgressionProps) {
  return (
    <Stack gap="md">
      <Title order={4} tt="capitalize">{slot}</Title>
      <Grid>
        {tiers.map((tierData) => 
          tierData.items.map((item: ProgressionItem, idx: number) => (
            <Grid.Col key={`${tierData.tier}-${idx}`} span={{ base: 12, sm: 6, md: 4, lg: 3 }}>
              <ItemCard item={item} tier={tierData.tier} />
            </Grid.Col>
          ))
        )}
      </Grid>
    </Stack>
  );
}
