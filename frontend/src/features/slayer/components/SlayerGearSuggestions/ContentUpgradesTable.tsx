import { Text, Group, Table, Image, Divider } from '@mantine/core';
import { IconCoin } from '@tabler/icons-react';
import { getAllItems } from './utils';
import type { SlayerGearResponse } from '../../../../lib/api/gear';

interface ContentUpgradesTableProps {
  gearData: SlayerGearResponse;
}

export function ContentUpgradesTable({ gearData }: ContentUpgradesTableProps) {
  if (!gearData.primary_loadout) return null;

  const items = getAllItems(gearData);
  if (items.length === 0) return null;

  return (
    <>
      <Divider color="osrsBrown.6" />
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
