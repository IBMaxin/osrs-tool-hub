import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { 
  Table, Image, Text, Group, Stack, SegmentedControl, 
  Badge, Anchor, Card, Loader, Box
} from '@mantine/core';
import { api } from '../../lib/api';

interface WikiItem {
  id: number | null;
  name: string;
  icon: string;
  price: number | null;
  wiki_url: string;
}

interface TierGroup {
  tier: string;
  items: WikiItem[];
}

// Helper to format large numbers (e.g. 1.2m, 450k)
const formatPrice = (price: number | null) => {
  if (price === null || price === 0) return 'Untradeable';
  if (price >= 1000000) return `${(price / 1000000).toFixed(1)}m`;
  if (price >= 1000) return `${(price / 1000).toFixed(0)}k`;
  return `${price} gp`;
};

const getTierColor = (tierName: string): string => {
  const upperTier = tierName.toLowerCase();
  if (upperTier.includes('torva') || upperTier.includes('bis') || upperTier.includes('shadow') || 
      upperTier.includes('twisted') || upperTier.includes('ancestral') || upperTier.includes('masori')) {
    return 'orange';
  }
  if (upperTier.includes('inquisitor') || upperTier.includes('oathplate') || 
      upperTier.includes('zaryte') || upperTier.includes('virtus')) {
    return 'red';
  }
  if (upperTier.includes('bandos') || upperTier.includes('neitiznot') || 
      upperTier.includes('crystal') || upperTier.includes('ahrim')) {
    return 'blue';
  }
  return 'gray';
};

const SLOT_ORDER: Record<string, number> = {
  "head": 1,
  "cape": 2,
  "neck": 3,
  "weapon": 4,
  "body": 5,
  "shield": 6,
  "legs": 7,
  "hands": 8,
  "feet": 9,
  "ring": 10,
  "ammo": 11,
};

export function WikiGearTable() {
  const [style, setStyle] = useState("melee");
  
  const { data, isLoading, error } = useQuery({
    queryKey: ['wiki-gear', style],
    queryFn: async () => {
      const res = await api.get(`/gear/wiki-progression/${style}`);
      return res.data;
    }
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
  const sortedSlots = Object.entries(data).sort(
    (a, b) => (SLOT_ORDER[a[0]] || 999) - (SLOT_ORDER[b[0]] || 999)
  );

  return (
    <Stack gap="lg">
      <Group justify="space-between" align="center">
        <Text size="xl" fw={700}>OSRS Wiki Gear Progression</Text>
        <SegmentedControl
          value={style}
          onChange={setStyle}
          data={[
            { label: 'Melee', value: 'melee' },
            { label: 'Ranged', value: 'ranged' },
            { label: 'Magic', value: 'magic' },
          ]}
        />
      </Group>

      <Card withBorder padding={0} radius="md" style={{ overflow: 'hidden' }}>
        <Table striped highlightOnHover verticalSpacing="md">
          <Table.Thead bg="gray.1">
            <Table.Tr>
              <Table.Th w={120}>Slot</Table.Th>
              <Table.Th>Progression Path (Best → Worst)</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {sortedSlots.map(([slot, tiers]: [string, TierGroup[]]) => (
              <Table.Tr key={slot}>
                <Table.Td fw={700} tt="capitalize" fz="lg" style={{ verticalAlign: 'top', paddingTop: '1rem' }}>
                  {slot}
                </Table.Td>
                <Table.Td>
                  <Stack gap="sm" py="xs">
                    {tiers.map((tier: TierGroup) => (
                      <Group key={tier.tier} wrap="nowrap" align="flex-start" gap="md">
                        {/* Tier Label */}
                        <Badge 
                          variant="filled" 
                          color={getTierColor(tier.tier)}
                          w={100}
                          size="md"
                          style={{ flexShrink: 0 }}
                        >
                          {tier.tier}
                        </Badge>

                        {/* Items in this tier */}
                        <Group gap="xs" style={{ flex: 1, flexWrap: 'wrap' }}>
                          {tier.items.map((item) => (
                            <Group 
                              key={item.name} 
                              gap={6} 
                              p={6} 
                              bg="white"
                              style={{ 
                                border: '1px solid #e0e0e0', 
                                borderRadius: 6,
                                boxShadow: '0 1px 2px rgba(0,0,0,0.05)',
                                transition: 'all 0.2s',
                              }}
                              className="hover:shadow-md"
                            >
                              {item.icon ? (
                                <Image 
                                  src={item.icon} 
                                  w={32} 
                                  h={32} 
                                  fit="contain"
                                  fallbackSrc="https://placehold.co/32?text=?"
                                />
                              ) : (
                                <Box w={32} h={32} bg="gray.2" style={{ borderRadius: 4 }} />
                              )}
                              <Stack gap={0} style={{ minWidth: 0 }}>
                                <Anchor 
                                  href={item.wiki_url} 
                                  target="_blank" 
                                  rel="noopener noreferrer"
                                  size="sm" 
                                  fw={600} 
                                  c="dark" 
                                  underline="hover"
                                  style={{ 
                                    textDecoration: 'none',
                                    whiteSpace: 'nowrap',
                                    overflow: 'hidden',
                                    textOverflow: 'ellipsis',
                                    maxWidth: '200px'
                                  }}
                                >
                                  {item.name}
                                </Anchor>
                                <Text 
                                  size="xs" 
                                  c={item.price && item.price > 0 ? "dimmed" : "orange"}
                                  fw={500}
                                >
                                  {formatPrice(item.price)}
                                </Text>
                              </Stack>
                            </Group>
                          ))}
                        </Group>
                      </Group>
                    ))}
                  </Stack>
                </Table.Td>
              </Table.Tr>
            ))}
          </Table.Tbody>
        </Table>
      </Card>
    </Stack>
  );
}
