import { useState } from 'react';
import {
  Card,
  Table,
  Select,
  Group,
  Text,
  Stack,
  Badge,
  NumberInput,
} from '@mantine/core';
import { useTrades } from '../hooks/useTrades';
import type { Trade, TradeFilters } from '../types';
import { formatNumber } from '../utils/format';

interface TradeHistoryProps {
  userId: string;
}

export function TradeHistory({ userId }: TradeHistoryProps) {
  const [filters, setFilters] = useState<TradeFilters>({
    limit: 50,
  });

  const { data: trades, isLoading, error } = useTrades(userId, filters);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'sold':
        return 'green';
      case 'bought':
        return 'blue';
      case 'cancelled':
        return 'red';
      default:
        return 'gray';
    }
  };

  if (error) {
    return (
      <Card withBorder shadow="sm" p="md">
        <Text c="red">Error loading trade history: {error instanceof Error ? error.message : 'Unknown error'}</Text>
      </Card>
    );
  }

  return (
    <Card withBorder shadow="sm" p="md">
      <Stack gap="md">
        <Group justify="space-between">
          <Text fw={500} size="lg">Trade History</Text>
          <Group>
            <Select
              placeholder="Filter by status"
              value={filters.status || ''}
              onChange={(value) => setFilters({ ...filters, status: value as TradeFilters['status'] || undefined })}
              data={[
                { value: '', label: 'All' },
                { value: 'bought', label: 'Bought' },
                { value: 'sold', label: 'Sold' },
                { value: 'cancelled', label: 'Cancelled' },
              ]}
              clearable
            />
            <NumberInput
              placeholder="Limit"
              value={filters.limit || 50}
              onChange={(value) => setFilters({ ...filters, limit: Number(value) || 50 })}
              min={1}
              max={1000}
              style={{ width: 100 }}
            />
          </Group>
        </Group>

        {isLoading ? (
          <Text c="dimmed">Loading trades...</Text>
        ) : !trades || trades.length === 0 ? (
          <Text c="dimmed">No trades found. Log your first trade to get started!</Text>
        ) : (
          <Table striped highlightOnHover>
            <Table.Thead>
              <Table.Tr>
                <Table.Th>Item</Table.Th>
                <Table.Th>Status</Table.Th>
                <Table.Th>Quantity</Table.Th>
                <Table.Th>Buy Price</Table.Th>
                <Table.Th>Sell Price</Table.Th>
                <Table.Th>Profit</Table.Th>
                <Table.Th>Date</Table.Th>
              </Table.Tr>
            </Table.Thead>
            <Table.Tbody>
              {trades.map((trade: Trade) => (
                <Table.Tr key={trade.id}>
                  <Table.Td>
                    <Text fw={500}>{trade.item_name}</Text>
                    <Text size="xs" c="dimmed">ID: {trade.item_id}</Text>
                  </Table.Td>
                  <Table.Td>
                    <Badge color={getStatusColor(trade.status)}>{trade.status}</Badge>
                  </Table.Td>
                  <Table.Td>{formatNumber(trade.quantity)}</Table.Td>
                  <Table.Td>{formatNumber(trade.buy_price)} GP</Table.Td>
                  <Table.Td>
                    {trade.sell_price ? `${formatNumber(trade.sell_price)} GP` : '-'}
                  </Table.Td>
                  <Table.Td>
                    <Text c={trade.profit >= 0 ? 'green' : 'red'} fw={500}>
                      {formatNumber(trade.profit)} GP
                    </Text>
                  </Table.Td>
                  <Table.Td>
                    <Text size="xs">{new Date(trade.created_at).toLocaleDateString()}</Text>
                    <Text size="xs" c="dimmed">{new Date(trade.created_at).toLocaleTimeString()}</Text>
                  </Table.Td>
                </Table.Tr>
              ))}
            </Table.Tbody>
          </Table>
        )}
      </Stack>
    </Card>
  );
}
