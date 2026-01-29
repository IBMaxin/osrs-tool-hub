import {
  Stack,
  Text,
  Group,
  Card,
  Image,
  Box,
} from '@mantine/core';
import { IconCoin } from '@tabler/icons-react';
import type { SlayerGearResponse } from '../../../../lib/api/gear';

// Equipment slots arranged in wiki-style grid layout
// Row 1: Head, Cape, Neck
// Row 2: Weapon, Body, Shield  
// Row 3: Legs, Hands, Feet
// Row 4: Ring, Ammo
const EQUIPMENT_GRID = [
  ['head', 'cape', 'neck'],
  ['weapon', 'body', 'shield'],
  ['legs', 'hands', 'feet'],
  ['ring', 'ammo', null],
];

interface EquipmentDiagramProps {
  loadout: SlayerGearResponse['primary_loadout'];
  tier: string;
}

export function EquipmentDiagram({ loadout, tier }: EquipmentDiagramProps) {
  if (!loadout) return null;

  return (
    <Card withBorder p="sm" style={{ backgroundColor: '#fafafa' }}>
      <Stack gap="sm">
        <Text fw={600} size="sm" ta="center" c="osrsGold.4">
          Level {tier}
        </Text>
        
        {/* Equipment Grid */}
        <Box style={{ display: 'flex', justifyContent: 'center' }}>
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: '6px',
            maxWidth: '280px',
          }}>
            {EQUIPMENT_GRID.map((row, rowIdx) =>
              row.map((slot, colIdx) => {
                if (!slot) return <div key={`empty-${rowIdx}-${colIdx}`} />;
                
                const item = loadout.slots[slot];
                const slotLabel = slot.charAt(0).toUpperCase() + slot.slice(1);
                
                return (
                  <Card
                    key={slot}
                    p={4}
                    withBorder
                    radius="xs"
                    style={{
                      minHeight: '70px',
                      minWidth: '70px',
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      justifyContent: 'center',
                      backgroundColor: item ? 'white' : '#f5f5f5',
                      border: item ? '2px solid #d4af37' : '1px solid #ddd',
                      boxShadow: item ? '0 2px 4px rgba(0,0,0,0.1)' : 'none',
                    }}
                  >
                    {item ? (
                      <Stack gap={2} align="center" style={{ width: '100%' }}>
                        {item.icon_url && (
                          <Image
                            src={item.icon_url}
                            alt={item.name}
                            width={56}
                            height={56}
                            fit="contain"
                            style={{ 
                              imageRendering: 'auto',
                            }}
                            fallbackSrc="https://placehold.co/56x56?text=?"
                          />
                        )}
                      </Stack>
                    ) : (
                      <Text size="xs" c="dimmed" ta="center" style={{ fontSize: '8px' }}>
                        {slotLabel}
                      </Text>
                    )}
                  </Card>
                );
              })
            )}
          </div>
        </Box>

        {/* Total Cost */}
        <Group justify="center" gap={4} mt="xs">
          <IconCoin size={16} color="#d4af37" />
          <Text fw={600} size="sm" c="osrsGold" style={{ fontFamily: 'monospace' }}>
            {loadout.total_cost.toLocaleString()}
          </Text>
        </Group>
      </Stack>
    </Card>
  );
}
