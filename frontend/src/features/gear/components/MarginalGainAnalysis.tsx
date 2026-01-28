import {
  Card,
  Stack,
  Text,
  Group,
  Progress,
  Badge,
} from '@mantine/core';
import type { DPSComparisonResult } from '../types';

interface MarginalGainAnalysisProps {
  results: DPSComparisonResult[];
}

export function MarginalGainAnalysis({ results }: MarginalGainAnalysisProps) {
  if (results.length < 2) {
    return (
      <Card withBorder shadow="sm" p="md">
        <Text c="dimmed" ta="center">
          Add at least 2 loadouts to see marginal gain analysis
        </Text>
      </Card>
    );
  }

  // Sort by DPS increase
  const sortedResults = [...results]
    .filter(r => r.dps_increase !== undefined && r.dps_increase !== null)
    .sort((a, b) => (b.dps_increase || 0) - (a.dps_increase || 0));

  const maxIncrease = Math.max(...sortedResults.map(r => Math.abs(r.dps_increase || 0)));

  return (
    <Card withBorder shadow="sm" p="md">
      <Stack gap="md">
        <Text fw={500} size="lg">Marginal Gain Analysis</Text>
        <Text size="sm" c="dimmed">
          DPS increase compared to baseline loadout ({results[0]?.loadout_name})
        </Text>

        {sortedResults.map((result) => {
          const increase = result.dps_increase || 0;
          const percent = result.dps_increase_percent || 0;
          const progressValue = maxIncrease > 0 ? (Math.abs(increase) / maxIncrease) * 100 : 0;

          return (
            <Card key={result.loadout_id} withBorder p="sm" radius="md">
              <Stack gap="xs">
                <Group justify="space-between">
                  <Text fw={500}>{result.loadout_name}</Text>
                  <Badge color={increase >= 0 ? 'green' : 'red'} variant="light">
                    {increase >= 0 ? '+' : ''}{increase.toFixed(2)} DPS
                    {percent !== 0 && ` (${percent >= 0 ? '+' : ''}${percent.toFixed(1)}%)`}
                  </Badge>
                </Group>
                <Progress
                  value={progressValue}
                  color={increase >= 0 ? 'green' : 'red'}
                  size="sm"
                  radius="xl"
                />
              </Stack>
            </Card>
          );
        })}
      </Stack>
    </Card>
  );
}
