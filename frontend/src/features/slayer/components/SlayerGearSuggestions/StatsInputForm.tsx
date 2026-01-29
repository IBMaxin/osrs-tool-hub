import {
  Stack,
  Text,
  Group,
  Button,
  NumberInput,
  SimpleGrid,
  SegmentedControl,
} from '@mantine/core';

interface StatsInputFormProps {
  stats: {
    attack: number;
    strength: number;
    defence: number;
    ranged: number;
    magic: number;
    prayer: number;
  };
  onStatsChange: (stats: StatsInputFormProps['stats']) => void;
  budget: number;
  onBudgetChange: (budget: number) => void;
  ironman: boolean;
  onIronmanToggle: () => void;
  combatStyle: 'melee' | 'ranged' | 'magic' | null;
  onCombatStyleChange: (style: 'melee' | 'ranged' | 'magic' | null) => void;
}

export function StatsInputForm({
  stats,
  onStatsChange,
  budget,
  onBudgetChange,
  ironman,
  onIronmanToggle,
  combatStyle,
  onCombatStyleChange,
}: StatsInputFormProps) {
  return (
    <>
      <SimpleGrid cols={3} spacing="xs">
        <NumberInput
          label="Attack"
          value={stats.attack}
          onChange={(val) => onStatsChange({ ...stats, attack: Number(val) || 1 })}
          min={1}
          max={99}
          size="xs"
        />
        <NumberInput
          label="Strength"
          value={stats.strength}
          onChange={(val) => onStatsChange({ ...stats, strength: Number(val) || 1 })}
          min={1}
          max={99}
          size="xs"
        />
        <NumberInput
          label="Defence"
          value={stats.defence}
          onChange={(val) => onStatsChange({ ...stats, defence: Number(val) || 1 })}
          min={1}
          max={99}
          size="xs"
        />
        <NumberInput
          label="Ranged"
          value={stats.ranged}
          onChange={(val) => onStatsChange({ ...stats, ranged: Number(val) || 1 })}
          min={1}
          max={99}
          size="xs"
        />
        <NumberInput
          label="Magic"
          value={stats.magic}
          onChange={(val) => onStatsChange({ ...stats, magic: Number(val) || 1 })}
          min={1}
          max={99}
          size="xs"
        />
        <NumberInput
          label="Prayer"
          value={stats.prayer}
          onChange={(val) => onStatsChange({ ...stats, prayer: Number(val) || 1 })}
          min={1}
          max={99}
          size="xs"
        />
      </SimpleGrid>

      <Group>
        <NumberInput
          label="Budget (GP)"
          value={budget}
          onChange={(val) => onBudgetChange(Number(val) || 0)}
          min={0}
          step={1_000_000}
          size="xs"
          style={{ flex: 1 }}
        />
        <Button
          size="xs"
          variant={ironman ? 'filled' : 'outline'}
          color="osrsOrange"
          onClick={onIronmanToggle}
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
          onChange={(value) => onCombatStyleChange(value === 'auto' ? null : value as 'melee' | 'ranged' | 'magic')}
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
    </>
  );
}
