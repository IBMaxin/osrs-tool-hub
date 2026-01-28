import {
  Card,
  Group,
  Text,
  Badge,
  Button,
  Stack,
  Tooltip,
} from '@mantine/core';
import { IconTrash, IconBell } from '@tabler/icons-react';
import { useRemoveFromWatchlist } from '../hooks/useWatchlist';
import { formatNumber } from '../utils/format';
import type { WatchlistItem } from '../types';

interface WatchlistItemCardProps {
  item: WatchlistItem;
  userId: string;
}

export function WatchlistItemCard({ item, userId }: WatchlistItemCardProps) {
  const removeFromWatchlist = useRemoveFromWatchlist();

  const handleRemove = async () => {
    try {
      await removeFromWatchlist.mutateAsync({
        watchlistItemId: item.id,
        userId: userId,
      });
    } catch (error) {
      // Error handled by mutation
    }
  };

  const getAlertTypeLabel = (type: string) => {
    switch (type) {
      case 'price_below':
        return 'Price Below';
      case 'price_above':
        return 'Price Above';
      case 'margin_above':
        return 'Margin Above';
      default:
        return type;
    }
  };

  const getAlertTypeColor = (type: string) => {
    switch (type) {
      case 'price_below':
        return 'blue';
      case 'price_above':
        return 'green';
      case 'margin_above':
        return 'orange';
      default:
        return 'gray';
    }
  };

  return (
    <Card withBorder p="sm" radius="md">
      <Group justify="space-between" wrap="nowrap">
        <Stack gap={4} style={{ flex: 1 }}>
          <Group gap="xs">
            <Text fw={500}>{item.item_name}</Text>
            <Badge color={getAlertTypeColor(item.alert_type)} variant="light" size="sm">
              {getAlertTypeLabel(item.alert_type)}
            </Badge>
          </Group>
          <Group gap="md">
            <Text size="sm" c="dimmed">
              Threshold: {formatNumber(item.threshold)} GP
            </Text>
            {item.last_triggered_at && (
              <Text size="xs" c="dimmed">
                Last triggered: {new Date(item.last_triggered_at).toLocaleString()}
              </Text>
            )}
          </Group>
        </Stack>
        <Group gap="xs">
          {item.last_triggered_at && (
            <Tooltip label="Alert triggered">
              <Badge color="red" leftSection={<IconBell size={12} />}>
                Alerted
              </Badge>
            </Tooltip>
          )}
          <Button
            size="xs"
            variant="light"
            color="red"
            leftSection={<IconTrash size={14} />}
            onClick={handleRemove}
            loading={removeFromWatchlist.isPending}
          >
            Remove
          </Button>
        </Group>
      </Group>
    </Card>
  );
}
