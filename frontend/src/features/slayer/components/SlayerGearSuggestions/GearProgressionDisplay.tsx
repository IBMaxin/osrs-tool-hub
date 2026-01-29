import { Text, Box, ScrollArea, Group } from '@mantine/core';
import { EquipmentDiagram } from './EquipmentDiagram';
import type { SlayerGearResponse } from '../../../../lib/api/gear';

interface GearProgressionDisplayProps {
  tierLoadouts: SlayerGearResponse['tier_loadouts'];
}

export function GearProgressionDisplay({ tierLoadouts }: GearProgressionDisplayProps) {
  if (!tierLoadouts || tierLoadouts.length === 0) return null;

  return (
    <>
      <Text fw={600} size="md" c="osrsGold.4">Gear Progression</Text>
      <ScrollArea>
        <Group align="flex-start" gap="md" wrap="nowrap" style={{ overflowX: 'auto' }}>
          {tierLoadouts.map((tierData) => (
            <Box key={tierData.tier} style={{ minWidth: '200px', flexShrink: 0 }}>
              <EquipmentDiagram 
                loadout={tierData.loadout} 
                tier={tierData.tier}
              />
            </Box>
          ))}
        </Group>
      </ScrollArea>
    </>
  );
}
