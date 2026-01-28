import { Group, Badge } from '@mantine/core';
import type { SlayerGearResponse } from '../../../../lib/api/gear';

interface DPSSummaryProps {
  loadout: SlayerGearResponse['primary_loadout'];
}

export function DPSSummary({ loadout }: DPSSummaryProps) {
  if (!loadout) return null;

  return (
    <Group justify="center" gap="md" mt="xs">
      <Badge size="md" color="osrsGreen" variant="light">
        DPS: {loadout.dps.dps.toFixed(2)}
      </Badge>
      <Badge size="md" color="osrsOrange" variant="light">
        Max Hit: {loadout.dps.max_hit}
      </Badge>
      <Badge size="md" color="osrsBlue" variant="light">
        Speed: {loadout.dps.attack_speed_seconds.toFixed(1)}s
      </Badge>
    </Group>
  );
}
