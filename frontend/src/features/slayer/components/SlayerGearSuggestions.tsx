import { useState } from 'react';
import {
  Stack,
  Text,
  Group,
  Badge,
  Button,
  NumberInput,
  SimpleGrid,
  Card,
  Image,
  Loader,
  Divider,
  Alert,
  Box,
  Table,
  ScrollArea,
  SegmentedControl,
} from '@mantine/core';
import { IconSword, IconAlertCircle, IconCoin } from '@tabler/icons-react';
import { useQuery } from '@tanstack/react-query';
import { GearApi, type SlayerGearResponse } from '../../../lib/api/gear';

interface SlayerGearSuggestionsProps {
  taskId: number | null;
  enabled: boolean;
}

const DEFAULT_STATS = {
  attack: 70,
  strength: 70,
  defence: 70,
  ranged: 70,
  magic: 70,
  prayer: 43,
};

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

function EquipmentDiagram({ 
  loadout, 
  tier 
}: { 
  loadout: SlayerGearResponse['primary_loadout']; 
  tier: string;
}) {
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

export function SlayerGearSuggestions({ taskId, enabled }: SlayerGearSuggestionsProps) {
  const [stats, setStats] = useState(DEFAULT_STATS);
  const [budget, setBudget] = useState(100_000_000);
  const [ironman, setIronman] = useState(false);
  const [combatStyle, setCombatStyle] = useState<'melee' | 'ranged' | 'magic' | null>(null);
  const [shouldFetch, setShouldFetch] = useState(false);

  const { data: gearData, isLoading, error } = useQuery<SlayerGearResponse>({
    queryKey: ['slayer', 'gear', taskId, stats, budget, ironman, combatStyle],
    queryFn: async () => {
      if (!taskId) {
        throw new Error('Task ID is required');
      }
      return GearApi.getSlayerGear({
        task_id: taskId,
        stats,
        budget,
        combat_style: combatStyle || undefined,
        ironman,
      });
    },
    enabled: enabled && shouldFetch && taskId !== null,
  });

  const handleGetSuggestions = () => {
    setShouldFetch(true);
  };

  const getCombatStyleColor = (style: string) => {
    switch (style) {
      case 'melee': return 'osrsRed';
      case 'ranged': return 'osrsGreen';
      case 'magic': return 'osrsBlue';
      default: return 'gray';
    }
  };

  // Get all items from primary loadout for the table
  const getAllItems = (): Array<{ slot: string; item: NonNullable<SlayerGearResponse['primary_loadout']>['slots'][string]; context: string }> => {
    if (!gearData?.primary_loadout) return [];
    
    const primaryLoadout = gearData.primary_loadout;
    const items: Array<{ slot: string; item: NonNullable<SlayerGearResponse['primary_loadout']>['slots'][string]; context: string }> = [];
    
    EQUIPMENT_GRID.flat()
      .filter((slot): slot is string => slot !== null)
      .forEach((slot) => {
        const item = primaryLoadout.slots[slot];
        if (!item) return;
        
        // Type assertion: we've already checked item is not null
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

  return (
    <Stack gap="md">
      <Divider color="osrsBrown.6" />
      <Group justify="space-between">
        <Text fw={600} size="sm" c="osrsGold.4">Gear Suggestions</Text>
        <Badge leftSection={<IconSword size={12} />} color="osrsGold" variant="light">
          Based on Your Levels
        </Badge>
      </Group>

      <SimpleGrid cols={3} spacing="xs">
        <NumberInput
          label="Attack"
          value={stats.attack}
          onChange={(val) => setStats({ ...stats, attack: Number(val) || 1 })}
          min={1}
          max={99}
          size="xs"
        />
        <NumberInput
          label="Strength"
          value={stats.strength}
          onChange={(val) => setStats({ ...stats, strength: Number(val) || 1 })}
          min={1}
          max={99}
          size="xs"
        />
        <NumberInput
          label="Defence"
          value={stats.defence}
          onChange={(val) => setStats({ ...stats, defence: Number(val) || 1 })}
          min={1}
          max={99}
          size="xs"
        />
        <NumberInput
          label="Ranged"
          value={stats.ranged}
          onChange={(val) => setStats({ ...stats, ranged: Number(val) || 1 })}
          min={1}
          max={99}
          size="xs"
        />
        <NumberInput
          label="Magic"
          value={stats.magic}
          onChange={(val) => setStats({ ...stats, magic: Number(val) || 1 })}
          min={1}
          max={99}
          size="xs"
        />
        <NumberInput
          label="Prayer"
          value={stats.prayer}
          onChange={(val) => setStats({ ...stats, prayer: Number(val) || 1 })}
          min={1}
          max={99}
          size="xs"
        />
      </SimpleGrid>

      <Group>
        <NumberInput
          label="Budget (GP)"
          value={budget}
          onChange={(val) => setBudget(Number(val) || 0)}
          min={0}
          step={1_000_000}
          size="xs"
          style={{ flex: 1 }}
        />
        <Button
          size="xs"
          variant={ironman ? 'filled' : 'outline'}
          color="osrsOrange"
          onClick={() => setIronman(!ironman)}
          style={{ marginTop: '24px' }}
        >
          {ironman ? 'Ironman' : 'Normal'}
        </Button>
      </Group>

      {/* Combat Style Selector */}
      <Stack gap="xs">
        <Text size="sm" fw={500}>Combat Style:</Text>
        <SegmentedControl
          value={combatStyle || 'auto'}
          onChange={(value) => setCombatStyle(value === 'auto' ? null : value as 'melee' | 'ranged' | 'magic')}
          data={[
            { label: 'Auto (Recommended)', value: 'auto' },
            { label: 'Melee', value: 'melee' },
            { label: 'Ranged', value: 'ranged' },
            { label: 'Magic', value: 'magic' },
          ]}
          fullWidth
          color="osrsGold"
        />
        {combatStyle && (
          <Text size="xs" c="dimmed">
            Showing gear for: {combatStyle.charAt(0).toUpperCase() + combatStyle.slice(1)}
          </Text>
        )}
      </Stack>

      <Button
        onClick={handleGetSuggestions}
        disabled={!taskId}
        color="osrsGold"
        fullWidth
      >
        Get Gear Suggestions
      </Button>

      {isLoading && (
        <Stack align="center" gap="xs" py="md">
          <Loader size="sm" color="osrsOrange" />
          <Text size="sm" c="dimmed">Loading gear suggestions...</Text>
        </Stack>
      )}

      {error && (
        <Alert icon={<IconAlertCircle size={16} />} color="red" title="Error">
          Failed to load gear suggestions. Please try again.
        </Alert>
      )}

      {gearData && (
        <Stack gap="lg">
          <Divider color="osrsBrown.6" />
          
          {/* Header with Combat Style */}
          <Group justify="space-between" align="flex-start">
            <Stack gap="xs">
              <Group gap="xs">
                <Text size="sm" fw={600}>
                  {combatStyle ? 'Selected Style:' : 'Recommended Style:'}
                </Text>
                <Badge 
                  size="lg" 
                  color={getCombatStyleColor(gearData.combat_style)} 
                  variant="filled"
                  style={{ textShadow: '1px 1px 2px rgba(0, 0, 0, 0.8)' }}
                >
                  {gearData.combat_style.charAt(0).toUpperCase() + gearData.combat_style.slice(1)}
                  {gearData.attack_type && ` (${gearData.attack_type.charAt(0).toUpperCase() + gearData.attack_type.slice(1)})`}
                </Badge>
                {combatStyle && (
                  <Badge size="sm" color="osrsGold" variant="light">
                    Custom Selection
                  </Badge>
                )}
              </Group>
              {gearData.weakness.length > 0 && (
                <Group gap="xs">
                  <Text size="xs" c="dimmed">Weaknesses:</Text>
                  {gearData.weakness.map((w, idx) => (
                    <Badge key={idx} size="sm" color="osrsOrange" variant="light">
                      {w}
                    </Badge>
                  ))}
                </Group>
              )}
            </Stack>
          </Group>

          {/* Level-Based Gear Progression - Wiki Style */}
          {gearData.tier_loadouts && gearData.tier_loadouts.length > 0 && (
            <>
              <Text fw={600} size="md" c="osrsGold.4">Gear Progression</Text>
              <ScrollArea>
                <Group align="flex-start" gap="md" wrap="nowrap" style={{ overflowX: 'auto' }}>
                  {gearData.tier_loadouts.map((tierData) => (
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
          )}

          {/* Content Specific Upgrades Table - Wiki Style */}
          {gearData.primary_loadout && (() => {
            const items = getAllItems();
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
                      // TypeScript guard: item is guaranteed non-null by getAllItems return type
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
          })()}

          {/* DPS Stats Summary */}
          {gearData.primary_loadout && (
            <Group justify="center" gap="md" mt="xs">
              <Badge size="md" color="osrsGreen" variant="light">
                DPS: {gearData.primary_loadout.dps.dps.toFixed(2)}
              </Badge>
              <Badge size="md" color="osrsOrange" variant="light">
                Max Hit: {gearData.primary_loadout.dps.max_hit}
              </Badge>
              <Badge size="md" color="osrsBlue" variant="light">
                Speed: {gearData.primary_loadout.dps.attack_speed_seconds.toFixed(1)}s
              </Badge>
            </Group>
          )}
        </Stack>
      )}
    </Stack>
  );
}
