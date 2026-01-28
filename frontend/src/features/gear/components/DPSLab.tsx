import { useState } from 'react';
import {
  Container,
  Stack,
  Group,
  Button,
  Select,
  NumberInput,
  Text,
  Alert,
  Title,
  Card,
} from '@mantine/core';
import { IconCalculator, IconAlertCircle } from '@tabler/icons-react';
import { LoadoutBuilder } from './LoadoutBuilder';
import { DPSComparisonTable } from './DPSComparisonTable';
import { MarginalGainAnalysis } from './MarginalGainAnalysis';
import { useCompareDPS } from '../hooks/useDPSLab';
import type { LoadoutInput, DPSComparisonRequest } from '../types';

export function DPSLab() {
  const [loadouts, setLoadouts] = useState<LoadoutInput[]>([
    { name: 'Loadout 1', loadout: {} },
  ]);
  const [combatStyle, setCombatStyle] = useState<'melee' | 'ranged' | 'magic'>('melee');
  const [attackType, setAttackType] = useState<'stab' | 'slash' | 'crush' | ''>('');
  const [playerStats, setPlayerStats] = useState({
    attack: 99,
    strength: 99,
    ranged: 99,
    magic: 99,
  });

  const compareDPS = useCompareDPS();

  const handleCompare = async () => {
    if (loadouts.length < 1) {
      return;
    }

    const request: DPSComparisonRequest = {
      loadouts,
      combat_style: combatStyle,
      attack_type: attackType || undefined,
      player_stats: playerStats,
    };

    try {
      await compareDPS.mutateAsync(request);
    } catch (error) {
      // Error handled by mutation
    }
  };

  return (
    <Container size="xl" py="xl">
      <Stack gap="lg">
        <Group justify="space-between">
          <div>
            <Title order={2} mb={4}>DPS Lab</Title>
            <Text c="dimmed" size="sm">Compare multiple loadouts side-by-side</Text>
          </div>
        </Group>

        <Card withBorder shadow="sm" p="md">
          <Stack gap="md">
            <Title order={4}>Configuration</Title>
            <Group grow>
              <Select
                label="Combat Style"
                value={combatStyle}
                onChange={(value) => setCombatStyle(value as typeof combatStyle)}
                data={[
                  { value: 'melee', label: 'Melee' },
                  { value: 'ranged', label: 'Ranged' },
                  { value: 'magic', label: 'Magic' },
                ]}
              />
              {combatStyle === 'melee' && (
                <Select
                  label="Attack Type"
                  value={attackType}
                  onChange={(value) => setAttackType(value || '')}
                  data={[
                    { value: '', label: 'Auto' },
                    { value: 'stab', label: 'Stab' },
                    { value: 'slash', label: 'Slash' },
                    { value: 'crush', label: 'Crush' },
                  ]}
                />
              )}
            </Group>

            <Group grow>
              <NumberInput
                label="Attack Level"
                value={playerStats.attack}
                onChange={(value) => setPlayerStats({ ...playerStats, attack: Number(value) || 1 })}
                min={1}
                max={99}
              />
              {combatStyle === 'melee' && (
                <NumberInput
                  label="Strength Level"
                  value={playerStats.strength}
                  onChange={(value) => setPlayerStats({ ...playerStats, strength: Number(value) || 1 })}
                  min={1}
                  max={99}
                />
              )}
              {combatStyle === 'ranged' && (
                <NumberInput
                  label="Ranged Level"
                  value={playerStats.ranged}
                  onChange={(value) => setPlayerStats({ ...playerStats, ranged: Number(value) || 1 })}
                  min={1}
                  max={99}
                />
              )}
              {combatStyle === 'magic' && (
                <NumberInput
                  label="Magic Level"
                  value={playerStats.magic}
                  onChange={(value) => setPlayerStats({ ...playerStats, magic: Number(value) || 1 })}
                  min={1}
                  max={99}
                />
              )}
            </Group>
          </Stack>
        </Card>

        <LoadoutBuilder loadouts={loadouts} onLoadoutsChange={setLoadouts} />

        {compareDPS.isError && (
          <Alert icon={<IconAlertCircle size={16} />} title="Error" color="red">
            {compareDPS.error instanceof Error ? compareDPS.error.message : 'Failed to compare DPS'}
          </Alert>
        )}

        <Button
          leftSection={<IconCalculator size={16} />}
          onClick={handleCompare}
          loading={compareDPS.isPending}
          size="lg"
          fullWidth
        >
          Compare DPS
        </Button>

        {compareDPS.isSuccess && compareDPS.data && (
          <>
            <DPSComparisonTable results={compareDPS.data.results} />
            <MarginalGainAnalysis results={compareDPS.data.results} />
          </>
        )}
      </Stack>
    </Container>
  );
}
