import { Table, Group, Text, Badge, Avatar, Stack, Button, Tooltip, Menu } from '@mantine/core';
import { IconPlus, IconBell } from '@tabler/icons-react';
import { FlipOpportunity } from '../../../lib/api';
import { formatGP, formatNumber, formatPrice } from '../utils/format';
import { useLogTrade } from '../hooks/useTrades';
import { useAddToWatchlist } from '../hooks/useWatchlist';

interface ResultsTableRowProps {
  flip: FlipOpportunity;
  userId?: string;
}

export function ResultsTableRow({ flip, userId }: ResultsTableRowProps) {
  const logTrade = useLogTrade();
  const addToWatchlist = useAddToWatchlist();

  const handleLogTrade = async () => {
    if (!userId) return;

    try {
      await logTrade.mutateAsync({
        user_id: userId,
        item_id: flip.item_id,
        buy_price: flip.buy_price,
        sell_price: flip.sell_price,
        quantity: 1,
        status: 'bought',
      });
    } catch (error) {
      // Error handled by mutation
    }
  };

  const handleAddToWatchlist = async (alertType: 'price_below' | 'price_above' | 'margin_above') => {
    if (!userId) return;

    const threshold = alertType === 'margin_above' 
      ? flip.margin 
      : alertType === 'price_below'
      ? flip.buy_price
      : flip.sell_price;

    try {
      await addToWatchlist.mutateAsync({
        user_id: userId,
        item_id: flip.item_id,
        alert_type: alertType,
        threshold: Math.max(1, Math.floor(threshold)),
      });
    } catch (error) {
      // Error handled by mutation
    }
  };

  return (
    <Table.Tr key={flip.item_id}>
      <Table.Td>
        <Group gap="sm">
          <Avatar src={flip.icon_url} size="md" radius="sm" bg="gray.1">
            {flip.item_name.charAt(0)}
          </Avatar>
          <Stack gap={4}>
            <Group gap="xs" align="center">
              <Text size="md" fw={700} lineClamp={1}>{flip.item_name}</Text>
              {flip.limit && (
                <Badge variant="light" color="blue" size="sm">
                  Limit: {formatNumber(flip.limit)}
                </Badge>
              )}
            </Group>
          </Stack>
        </Group>
      </Table.Td>
      <Table.Td style={{ textAlign: 'right' }}>
        <Text size="sm" ff="monospace" fw={500}>
          {formatPrice(flip.buy_price)}
        </Text>
      </Table.Td>
      <Table.Td style={{ textAlign: 'right' }}>
        <Text size="sm" ff="monospace" fw={500}>
          {formatPrice(flip.sell_price)}
        </Text>
      </Table.Td>
      <Table.Td style={{ textAlign: 'right' }}>
        <Stack gap={2} align="flex-end">
          <Text c={flip.margin > 0 ? 'green' : 'red'} fw={700} size="sm">
            {flip.margin > 0 ? '+' : ''}{formatPrice(flip.margin)}
          </Text>
          {flip.tax && (
            <Text size="xs" c="dimmed">Tax: {formatPrice(flip.tax)}</Text>
          )}
        </Stack>
      </Table.Td>
      <Table.Td style={{ textAlign: 'right' }}>
        <Badge 
          variant="light" 
          color={
            flip.roi >= 10 ? 'green' : 
            flip.roi >= 5 ? 'teal' : 
            flip.roi >= 2 ? 'blue' : 
            flip.roi >= 0 ? 'gray' : 'red'
          }
          size="lg"
        >
          {flip.roi >= 0 ? '+' : ''}{flip.roi.toFixed(2)}%
        </Badge>
      </Table.Td>
      <Table.Td style={{ textAlign: 'right' }}>
        <Text 
          fw={700} 
          size="sm"
          c={
            (flip.potential_profit || 0) >= 10_000_000 ? 'orange' :
            (flip.potential_profit || 0) >= 1_000_000 ? 'yellow' :
            'dark'
          }
        >
          {flip.potential_profit ? formatPrice(flip.potential_profit) : 'N/A'}
        </Text>
      </Table.Td>
      <Table.Td style={{ textAlign: 'center' }}>
        <Text size="sm" c={flip.volume > 0 ? 'dark' : 'dimmed'}>
          {flip.volume > 0 ? formatGP(flip.volume) : 'N/A'}
        </Text>
      </Table.Td>
      {userId && (
        <Table.Td style={{ textAlign: 'center' }}>
          <Group gap="xs" justify="center">
            <Tooltip label="Log this trade">
              <Button
                size="xs"
                variant="light"
                leftSection={<IconPlus size={14} />}
                onClick={handleLogTrade}
                loading={logTrade.isPending}
              >
                Log
              </Button>
            </Tooltip>
            <Menu shadow="md" width={200}>
              <Menu.Target>
                <Button
                  size="xs"
                  variant="light"
                  leftSection={<IconBell size={14} />}
                  loading={addToWatchlist.isPending}
                >
                  Watch
                </Button>
              </Menu.Target>
              <Menu.Dropdown>
                <Menu.Label>Add Alert</Menu.Label>
                <Menu.Item onClick={() => handleAddToWatchlist('price_below')}>
                  Price Below {formatPrice(flip.buy_price)}
                </Menu.Item>
                <Menu.Item onClick={() => handleAddToWatchlist('price_above')}>
                  Price Above {formatPrice(flip.sell_price)}
                </Menu.Item>
                <Menu.Item onClick={() => handleAddToWatchlist('margin_above')}>
                  Margin Above {formatPrice(flip.margin)}
                </Menu.Item>
              </Menu.Dropdown>
            </Menu>
          </Group>
        </Table.Td>
      )}
    </Table.Tr>
  );
}
