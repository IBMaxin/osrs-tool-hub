import { SimpleGrid, NumberInput } from '@mantine/core';

interface StatsInputFormProps {
  stats: {
    attack: number;
    strength: number;
    defence: number;
    ranged: number;
    magic: number;
    prayer: number;
  };
  onStatsChange: (stats: {
    attack: number;
    strength: number;
    defence: number;
    ranged: number;
    magic: number;
    prayer: number;
  }) => void;
}

export function StatsInputForm({ stats, onStatsChange }: StatsInputFormProps) {
  return (
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
  );
}
