import {
  Card,
  Table,
  Text,
  Badge,
  Stack,
} from '@mantine/core';
import type { DPSComparisonResult } from '../types';

interface DPSComparisonTableProps {
  results: DPSComparisonResult[];
}

export function DPSComparisonTable({ results }: DPSComparisonTableProps) {
  if (results.length === 0) {
    return (
      <Card withBorder shadow="sm" p="md">
        <Text c="dimmed" ta="center">No comparison results. Build loadouts and compare!</Text>
      </Card>
    );
  }

  // Find the highest DPS for highlighting
  const maxDPS = Math.max(...results.map(r => r.dps));

  return (
    <Card withBorder shadow="sm" p="md">
      <Table striped highlightOnHover>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Loadout</Table.Th>
            <Table.Th style={{ textAlign: 'right' }}>DPS</Table.Th>
            <Table.Th style={{ textAlign: 'right' }}>Max Hit</Table.Th>
            <Table.Th style={{ textAlign: 'right' }}>Accuracy</Table.Th>
            <Table.Th style={{ textAlign: 'right' }}>Attack Speed</Table.Th>
            <Table.Th style={{ textAlign: 'right' }}>DPS Increase</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {results.map((result) => (
            <Table.Tr key={result.loadout_id}>
              <Table.Td>
                <Text fw={500}>{result.loadout_name}</Text>
                {result.dps === maxDPS && (
                  <Badge color="green" size="xs" mt={4}>Best</Badge>
                )}
              </Table.Td>
              <Table.Td style={{ textAlign: 'right' }}>
                <Text fw={700} size="lg" c={result.dps === maxDPS ? 'green' : 'dark'}>
                  {result.dps.toFixed(2)}
                </Text>
              </Table.Td>
              <Table.Td style={{ textAlign: 'right' }}>
                <Text>{result.max_hit}</Text>
              </Table.Td>
              <Table.Td style={{ textAlign: 'right' }}>
                <Text>{result.accuracy.toFixed(1)}%</Text>
              </Table.Td>
              <Table.Td style={{ textAlign: 'right' }}>
                <Text>{result.attack_speed} ticks</Text>
                <Text size="xs" c="dimmed">{result.attack_speed_seconds.toFixed(1)}s</Text>
              </Table.Td>
              <Table.Td style={{ textAlign: 'right' }}>
                {result.dps_increase !== undefined && result.dps_increase !== null && (
                  <Stack gap={2} align="flex-end">
                    <Text
                      c={result.dps_increase >= 0 ? 'green' : 'red'}
                      fw={500}
                    >
                      {result.dps_increase >= 0 ? '+' : ''}{result.dps_increase.toFixed(2)}
                    </Text>
                    {result.dps_increase_percent !== undefined && (
                      <Text size="xs" c="dimmed">
                        ({result.dps_increase_percent >= 0 ? '+' : ''}{result.dps_increase_percent.toFixed(1)}%)
                      </Text>
                    )}
                  </Stack>
                )}
              </Table.Td>
            </Table.Tr>
          ))}
        </Table.Tbody>
      </Table>
    </Card>
  );
}
