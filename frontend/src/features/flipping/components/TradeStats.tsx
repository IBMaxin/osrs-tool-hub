import { useState } from 'react';
import {
  Card,
  Grid,
  Text,
  Stack,
  Group,
  Badge,
  NumberInput,
  Button,
  Table,
  Title,
} from '@mantine/core';
import { IconCoins, IconTrendingUp, IconClock } from '@tabler/icons-react';
import { useTradeStats } from '../hooks/useTrades';
import { formatNumber } from '../utils/format';

interface TradeStatsProps {
  userId: string;
}

export function TradeStats({ userId }: TradeStatsProps) {
  const [days, setDays] = useState<number | ''>('');

  const { data: stats, isLoading, error } = useTradeStats(userId, days ? Number(days) : undefined);

  if (error) {
    return (
      <Card withBorder shadow="sm" p="md">
        <Text c="red">Error loading stats: {error instanceof Error ? error.message : 'Unknown error'}</Text>
      </Card>
    );
  }

  if (isLoading || !stats) {
    return (
      <Card withBorder shadow="sm" p="md">
        <Text c="dimmed">Loading stats...</Text>
      </Card>
    );
  }

  return (
    <Stack gap="md">
      <Card withBorder shadow="sm" p="md">
        <Group justify="space-between" mb="md">
          <Title order={4}>Trade Statistics</Title>
          <Group>
            <NumberInput
              placeholder="Days (all time if empty)"
              value={days}
              onChange={(value) => setDays(value)}
              min={1}
              style={{ width: 150 }}
            />
            <Button onClick={() => setDays('')} variant="light" size="xs">
              All Time
            </Button>
          </Group>
        </Group>

        <Grid>
          <Grid.Col span={{ base: 12, sm: 6, md: 3 }}>
            <Card withBorder p="sm" style={{ textAlign: 'center' }}>
              <IconCoins size={32} color="gold" style={{ margin: '0 auto 8px' }} />
              <Text size="xs" c="dimmed">Total Profit</Text>
              <Text fw={700} size="xl" c={stats.total_profit >= 0 ? 'green' : 'red'}>
                {formatNumber(stats.total_profit)} GP
              </Text>
            </Card>
          </Grid.Col>

          <Grid.Col span={{ base: 12, sm: 6, md: 3 }}>
            <Card withBorder p="sm" style={{ textAlign: 'center' }}>
              <IconTrendingUp size={32} color="blue" style={{ margin: '0 auto 8px' }} />
              <Text size="xs" c="dimmed">Total Trades</Text>
              <Text fw={700} size="xl">{stats.total_trades}</Text>
            </Card>
          </Grid.Col>

          <Grid.Col span={{ base: 12, sm: 6, md: 3 }}>
            <Card withBorder p="sm" style={{ textAlign: 'center' }}>
              <Badge color="green" size="lg" variant="light" style={{ marginBottom: 8 }}>
                Sold
              </Badge>
              <Text size="xs" c="dimmed">Sold Trades</Text>
              <Text fw={700} size="xl">{stats.sold_trades}</Text>
            </Card>
          </Grid.Col>

          <Grid.Col span={{ base: 12, sm: 6, md: 3 }}>
            <Card withBorder p="sm" style={{ textAlign: 'center' }}>
              <IconClock size={32} color="orange" style={{ margin: '0 auto 8px' }} />
              <Text size="xs" c="dimmed">Profit/Hour</Text>
              <Text fw={700} size="xl">
                {formatNumber(stats.profit_per_hour)} GP/h
              </Text>
            </Card>
          </Grid.Col>
        </Grid>
      </Card>

      {stats.best_items && stats.best_items.length > 0 && (
        <Card withBorder shadow="sm" p="md">
          <Title order={4} mb="md">Top Items by Profit</Title>
          <Table>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Item</Table.Th>
                <Table.Th>Total Profit</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {stats.best_items.map((item, index) => (
                <Table.Tr key={index}>
                  <Table.Td>
                    <Text fw={500}>{item.item_name}</Text>
                  </Table.Td>
                  <Table.Td>
                    <Text c="green" fw={500}>{formatNumber(item.profit)} GP</Text>
                  </Table.Td>
                </Table.Tr>
              ))}
            </Table.Tbody>
          </Table>
        </Card>
      )}
    </Stack>
  );
}
