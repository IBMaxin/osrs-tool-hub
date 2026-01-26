import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { 
  Tabs, Grid, Card, Image, Text, Group, 
  Loader, Stack, Title, Badge, Tooltip,
  Anchor, ScrollArea, Table, ActionIcon,
  Collapse, Button, Box
} from '@mantine/core';
import { IconExternalLink, IconChevronDown, IconChevronUp } from '@tabler/icons-react';
import { fetchFullProgression, type FullProgressionResponse, type ProgressionItem } from '../../lib/api';

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

function formatPrice(price: number | null): string {
  if (price === null) return 'N/A';
  if (price >= 1_000_000) return `${(price / 1_000_000).toFixed(2)}M`;
  if (price >= 1_000) return `${(price / 1_000).toFixed(1)}K`;
  return price.toString();
}

function ItemCard({ item, tier }: { item: ProgressionItem; tier: string }) {
  const [opened, setOpened] = useState(false);
  
  return (
    <Card withBorder padding="sm" radius="md" style={{ height: '100%' }}>
      <Group justify="space-between" align="flex-start" mb="xs">
        <Group gap="xs" wrap="nowrap">
          {item.icon_url ? (
            <Image 
              src={item.icon_url} 
              w={40} 
              h={40} 
              fit="contain"
              fallbackSrc="https://placehold.co/40?text=?"
            />
          ) : (
            <Box w={40} h={40} bg="gray.2" style={{ borderRadius: 4 }} />
          )}
          <Stack gap={2} style={{ flex: 1, minWidth: 0 }}>
            <Anchor
              href={item.wiki_url}
              target="_blank"
              rel="noopener noreferrer"
              size="sm"
              fw={500}
              style={{ textDecoration: 'none' }}
            >
              {item.name}
              <IconExternalLink size={12} style={{ marginLeft: 4, display: 'inline' }} />
            </Anchor>
            {item.price !== null && (
              <Text size="xs" c="dimmed" fw={600}>
                {formatPrice(item.price)} GP
              </Text>
            )}
          </Stack>
        </Group>
        <Badge size="sm" variant="light" color="blue">
          {tier}
        </Badge>
      </Group>
      
      {item.not_found && (
        <Badge color="red" size="xs" mb="xs">
          Not in database
        </Badge>
      )}
      
      {item.stats && (
        <>
          <Button
            variant="subtle"
            size="xs"
            fullWidth
            onClick={() => setOpened(!opened)}
            rightSection={opened ? <IconChevronUp size={14} /> : <IconChevronDown size={14} />}
            mb="xs"
          >
            {opened ? 'Hide' : 'Show'} Stats
          </Button>
          
          <Collapse in={opened}>
            <ScrollArea h={200}>
              <Table size="xs" striped>
                <Table.Tbody>
                  {item.stats.melee_strength > 0 && (
                    <Table.Tr>
                      <Table.Td>Melee Str</Table.Td>
                      <Table.Td>+{item.stats.melee_strength}</Table.Td>
                    </Table.Tr>
                  )}
                  {item.stats.ranged_strength > 0 && (
                    <Table.Tr>
                      <Table.Td>Ranged Str</Table.Td>
                      <Table.Td>+{item.stats.ranged_strength}</Table.Td>
                    </Table.Tr>
                  )}
                  {item.stats.magic_damage > 0 && (
                    <Table.Tr>
                      <Table.Td>Magic Dmg</Table.Td>
                      <Table.Td>+{item.stats.magic_damage}%</Table.Td>
                    </Table.Tr>
                  )}
                  {item.stats.prayer_bonus !== 0 && (
                    <Table.Tr>
                      <Table.Td>Prayer</Table.Td>
                      <Table.Td>{item.stats.prayer_bonus > 0 ? '+' : ''}{item.stats.prayer_bonus}</Table.Td>
                    </Table.Tr>
                  )}
                  {item.stats.attack_stab > 0 && (
                    <Table.Tr>
                      <Table.Td>Stab</Table.Td>
                      <Table.Td>+{item.stats.attack_stab}</Table.Td>
                    </Table.Tr>
                  )}
                  {item.stats.attack_slash > 0 && (
                    <Table.Tr>
                      <Table.Td>Slash</Table.Td>
                      <Table.Td>+{item.stats.attack_slash}</Table.Td>
                    </Table.Tr>
                  )}
                  {item.stats.attack_crush > 0 && (
                    <Table.Tr>
                      <Table.Td>Crush</Table.Td>
                      <Table.Td>+{item.stats.attack_crush}</Table.Td>
                    </Table.Tr>
                  )}
                  {item.stats.attack_magic > 0 && (
                    <Table.Tr>
                      <Table.Td>Magic</Table.Td>
                      <Table.Td>+{item.stats.attack_magic}</Table.Td>
                    </Table.Tr>
                  )}
                  {item.stats.attack_ranged > 0 && (
                    <Table.Tr>
                      <Table.Td>Ranged</Table.Td>
                      <Table.Td>+{item.stats.attack_ranged}</Table.Td>
                    </Table.Tr>
                  )}
                </Table.Tbody>
              </Table>
              
              {item.requirements && (
                <Stack gap="xs" mt="xs">
                  <Text size="xs" fw={700} c="dimmed">Requirements:</Text>
                  <Group gap="xs">
                    {item.requirements.attack > 1 && (
                      <Badge size="xs" variant="outline">Atk {item.requirements.attack}</Badge>
                    )}
                    {item.requirements.strength > 1 && (
                      <Badge size="xs" variant="outline">Str {item.requirements.strength}</Badge>
                    )}
                    {item.requirements.defence > 1 && (
                      <Badge size="xs" variant="outline">Def {item.requirements.defence}</Badge>
                    )}
                    {item.requirements.ranged > 1 && (
                      <Badge size="xs" variant="outline">Rng {item.requirements.ranged}</Badge>
                    )}
                    {item.requirements.magic > 1 && (
                      <Badge size="xs" variant="outline">Mag {item.requirements.magic}</Badge>
                    )}
                    {item.requirements.quest && (
                      <Badge size="xs" color="orange" variant="light">{item.requirements.quest}</Badge>
                    )}
                  </Group>
                </Stack>
              )}
            </ScrollArea>
          </Collapse>
        </>
      )}
    </Card>
  );
}

function SlotProgression({ slot, tiers }: { slot: string; tiers: any[] }) {
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
            <SlotProgression slot={slot} tiers={tiers} />
          </Tabs.Panel>
        ))}
      </Tabs>
    </Stack>
  );
}
