import {
  Stack,
  Text,
  Group,
  Badge,
  Button,
  Loader,
  Divider,
  Alert,
} from '@mantine/core';
import { IconSword, IconAlertCircle } from '@tabler/icons-react';
import { useSlayerGearSuggestions } from './useSlayerGearSuggestions';
import { getCombatStyleColor } from './utils';
import { StatsInputForm } from './StatsInputForm';
import { GearProgressionDisplay } from './GearProgressionDisplay';
import { ContentUpgradesTable } from './ContentUpgradesTable';

interface SlayerGearSuggestionsProps {
  taskId: number | null;
  enabled: boolean;
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

      <StatsInputForm
        stats={stats}
        onStatsChange={setStats}
        budget={budget}
        onBudgetChange={setBudget}
        ironman={ironman}
        onIronmanToggle={() => setIronman(!ironman)}
        combatStyle={combatStyle}
        onCombatStyleChange={setCombatStyle}
      />

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
          <GearProgressionDisplay tierLoadouts={gearData.tier_loadouts} />

          {/* Content Specific Upgrades Table */}
          <ContentUpgradesTable gearData={gearData} />

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
