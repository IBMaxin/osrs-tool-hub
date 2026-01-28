import { Table, Group, Text, Image } from '@mantine/core';
import { IconCoin } from '@tabler/icons-react';
import type { SlayerGearResponse } from '../../../../lib/api/gear';

const EQUIPMENT_GRID = [
  ['head', 'cape', 'neck'],
  ['weapon', 'body', 'shield'],
  ['legs', 'hands', 'feet'],
  ['ring', 'ammo', null],
];

interface ContentUpgradesTableProps {
  loadout: SlayerGearResponse['primary_loadout'];
}

export function ContentUpgradesTable({ loadout }: ContentUpgradesTableProps) {
  if (!loadout) return null;

  const getAllItems = (): Array<{ 
    slot: string; 
    item: NonNullable<SlayerGearResponse['primary_loadout']>['slots'][string]; 
    context: string;
  }> => {
    const items: Array<{ 
      slot: string; 
      item: NonNullable<SlayerGearResponse['primary_loadout']>['slots'][string]; 
      context: string;
    }> = [];
    
    EQUIPMENT_GRID.flat()
      .filter((slot): slot is string => slot !== null)
      .forEach((slot) => {
        const item = loadout.slots[slot];
        if (!item) return;
        
        const nonNullItem = item as NonNullable<typeof item>;
        
        // Determine context/use case based on item name and slot
        let context = '';
        if (slot === 'weapon') {
          if (nonNullItem.name.toLowerCase().includes('whip') || nonNullItem.name.toLowerCase().includes('tentacle')) {
            context = 'General Slayer';
          } else if (nonNullItem.name.toLowerCase().includes('rapier')) {
            context = 'Combat training / Slayer';
          } else if (nonNullItem.name.toLowerCase().includes('blade')) {
            context = 'Slash weak enemies';
          }
        } else if (slot === 'head' && nonNullItem.name.toLowerCase().includes('serpentine')) {
          context = 'Venom immunity';
        } else if (slot === 'body' && nonNullItem.name.toLowerCase().includes('bandos')) {
          context = 'Strength bonus';
        }
        
        items.push({
          slot,
          item: nonNullItem,
          context,
        });
      });
    
    return items;
  };

  const items = getAllItems();
  if (items.length === 0) return null;

  return (
    <>
      <Text fw={600} size="md" c="osrsGold.4" mb="xs">Content specific upgrades</Text>
      <Table striped highlightOnHover withTableBorder withColumnBorders>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Content specific upgrades</Table.Th>
            <Table.Th style={{ textAlign: 'right' }}>Cost (Buy)</Table.Th>
            <Table.Th style={{ textAlign: 'right' }}>Cost (Upkeep, 1 Hour)</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {items.map((entry) => {
            const { slot, item, context } = entry;
            if (!item) return null;
            
            return (
              <Table.Tr key={`${slot}-${item.id}`}>
                <Table.Td>
                  <Group gap="xs">
                    {item.icon_url && (
                      <Image
                        src={item.icon_url}
                        alt={item.name}
                        width={32}
                        height={32}
                        fit="contain"
                        style={{ 
                          imageRendering: 'auto',
                        }}
                        fallbackSrc="https://placehold.co/32x32?text=?"
                      />
                    )}
                    <div>
                      <Text size="sm" fw={500}>
                        {item.name}
                      </Text>
                      {context && (
                        <Text size="xs" c="dimmed" style={{ fontStyle: 'italic' }}>
                          ({context})
                        </Text>
                      )}
                    </div>
                  </Group>
                </Table.Td>
                <Table.Td style={{ textAlign: 'right' }}>
                  <Group gap={4} justify="flex-end">
                    <IconCoin size={14} color="#d4af37" />
                    <Text size="sm" style={{ fontFamily: 'monospace' }}>
                      {item.price.toLocaleString()}
                    </Text>
                  </Group>
                </Table.Td>
                <Table.Td style={{ textAlign: 'right' }}>
                  <Text size="sm" c="dimmed">N/A</Text>
                </Table.Td>
              </Table.Tr>
            );
          })}
        </Table.Tbody>
      </Table>
    </>
  );
}
