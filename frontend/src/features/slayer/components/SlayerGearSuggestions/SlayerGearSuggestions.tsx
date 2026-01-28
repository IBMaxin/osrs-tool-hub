import {
  Stack,
  Text,
  Group,
  Badge,
  Button,
  NumberInput,
  Divider,
  Alert,
  Box,
  ScrollArea,
  SegmentedControl,
} from '@mantine/core';
import { IconSword, IconAlertCircle } from '@tabler/icons-react';
import { Loader } from '@mantine/core';
import { EquipmentDiagram } from './EquipmentDiagram';
import { StatsInputForm } from './StatsInputForm';
import { ContentUpgradesTable } from './ContentUpgradesTable';
import { DPSSummary } from './DPSSummary';
import { useSlayerGearSuggestions } from './useSlayerGearSuggestions';

interface SlayerGearSuggestionsProps {
  taskId: number | null;
  enabled: boolean;
}

function getCombatStyleColor(style: string) {
  switch (style) {
    case 'melee': return 'osrsRed';
    case 'ranged': return 'osrsGreen';
    case 'magic': return 'osrsBlue';
    default: return 'gray';
  }
}

export function SlayerGearSuggestions({ taskId, enabled }: SlayerGearSuggestionsProps) {
  const {
    stats,
    setStats,
    budget,
    setBudget,
    ironman,
    setIronman,
    combatStyle,
    setCombatStyle,
    gearData,
    isLoading,
    error,
    handleGetSuggestions,
  } = useSlayerGearSuggestions({ taskId, enabled });

  return (
    <Stack gap="md">
      <Divider color="osrsBrown.6" />
      <Group justify="space-between">
        <Text fw={600} size="sm" c="osrsGold.4">Gear Suggestions</Text>
        <Badge leftSection={<IconSword size={12} />} color="osrsGold" variant="light">
          Based on Your Levels
        </Badge>
      </Group>

      <StatsInputForm stats={stats} onStatsChange={setStats} />

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

          {/* Content Specific Upgrades Table */}
          {gearData.primary_loadout && (
            <>
              <Divider color="osrsBrown.6" />
              <ContentUpgradesTable loadout={gearData.primary_loadout} />
            </>
          )}

          {/* DPS Stats Summary */}
          {gearData.primary_loadout && (
            <DPSSummary loadout={gearData.primary_loadout} />
          )}
        </Stack>
      )}
    </Stack>
  );
}
