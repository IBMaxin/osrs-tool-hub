import { useState } from 'react';
import {
  Card,
  Stack,
  NumberInput,
  Select,
  Button,
  Group,
  Text,
  Alert,
  Title,
} from '@mantine/core';
import { IconCheck, IconAlertCircle, IconPlus } from '@tabler/icons-react';
import { useWatchlist, useAddToWatchlist } from '../hooks/useWatchlist';
import { WatchlistItemCard } from './WatchlistItemCard';
import type { WatchlistCreateRequest } from '../types';

interface WatchlistManagerProps {
  userId: string;
}

export function WatchlistManager({ userId }: WatchlistManagerProps) {
  const [itemId, setItemId] = useState<number | ''>('');
  const [alertType, setAlertType] = useState<'price_below' | 'price_above' | 'margin_above'>('price_below');
  const [threshold, setThreshold] = useState<number | ''>('');

  const { data: watchlist, isLoading, error } = useWatchlist(userId);
  const addToWatchlist = useAddToWatchlist();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!itemId || !threshold) {
      return;
    }

    const watchlistData: WatchlistCreateRequest = {
      user_id: userId,
      item_id: Number(itemId),
      alert_type: alertType,
      threshold: Number(threshold),
    };

    try {
      await addToWatchlist.mutateAsync(watchlistData);
      // Reset form
      setItemId('');
      setThreshold('');
    } catch (error) {
      // Error is handled by mutation
    }
  };

  return (
    <Stack gap="md">
      <Card withBorder shadow="sm" p="md">
        <Stack gap="md">
          <Title order={4}>Add to Watchlist</Title>

          {addToWatchlist.isError && (
            <Alert icon={<IconAlertCircle size={16} />} title="Error" color="red">
              {addToWatchlist.error instanceof Error ? addToWatchlist.error.message : 'Failed to add to watchlist'}
            </Alert>
          )}

          {addToWatchlist.isSuccess && (
            <Alert icon={<IconCheck size={16} />} title="Success" color="green">
              Item added to watchlist!
            </Alert>
          )}

          <form onSubmit={handleSubmit}>
            <Stack gap="md">
              <Group grow>
                <NumberInput
                  label="Item ID"
                  placeholder="Enter item ID"
                  value={itemId}
                  onChange={(value) => setItemId(value === '' ? '' : Number(value))}
                  required
                  min={1}
                />
                <Select
                  label="Alert Type"
                  value={alertType}
                  onChange={(value) => setAlertType(value as typeof alertType)}
                  data={[
                    { value: 'price_below', label: 'Price Below' },
                    { value: 'price_above', label: 'Price Above' },
                    { value: 'margin_above', label: 'Margin Above' },
                  ]}
                />
              </Group>

              <NumberInput
                label="Threshold (GP)"
                placeholder="Alert threshold"
                value={threshold}
                onChange={(value) => setThreshold(value === '' ? '' : Number(value))}
                required
                min={1}
                leftSection={<Text size="xs">GP</Text>}
              />

              <Button
                type="submit"
                loading={addToWatchlist.isPending}
                leftSection={<IconPlus size={16} />}
                fullWidth
              >
                Add to Watchlist
              </Button>
            </Stack>
          </form>
        </Stack>
      </Card>

      <Card withBorder shadow="sm" p="md">
        <Stack gap="md">
          <Title order={4}>My Watchlist</Title>

          {error && (
            <Alert icon={<IconAlertCircle size={16} />} title="Error" color="red">
              {error instanceof Error ? error.message : 'Failed to load watchlist'}
            </Alert>
          )}

          {isLoading ? (
            <Text c="dimmed">Loading watchlist...</Text>
          ) : !watchlist || watchlist.length === 0 ? (
            <Text c="dimmed">No items in watchlist. Add items above to get started!</Text>
          ) : (
            <Stack gap="sm">
              {watchlist.map((item) => (
                <WatchlistItemCard key={item.id} item={item} userId={userId} />
              ))}
            </Stack>
          )}
        </Stack>
      </Card>
    </Stack>
  );
}
