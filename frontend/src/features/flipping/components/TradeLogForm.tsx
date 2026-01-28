import { useState } from 'react';
import {
  Card,
  Stack,
  TextInput,
  NumberInput,
  Select,
  Button,
  Group,
  Text,
  Alert,
} from '@mantine/core';
import { IconCheck, IconAlertCircle } from '@tabler/icons-react';
import { useLogTrade } from '../hooks/useTrades';
import type { TradeCreateRequest } from '../types';

interface TradeLogFormProps {
  userId: string;
  defaultItemId?: number;
  defaultItemName?: string;
  onSuccess?: () => void;
}

export function TradeLogForm({ userId, defaultItemId, defaultItemName, onSuccess }: TradeLogFormProps) {
  const [itemId, setItemId] = useState<number | ''>(defaultItemId || '');
  const [itemName, setItemName] = useState(defaultItemName || '');
  const [buyPrice, setBuyPrice] = useState<number | ''>('');
  const [sellPrice, setSellPrice] = useState<number | ''>('');
  const [quantity, setQuantity] = useState<number | ''>(1);
  const [status, setStatus] = useState<'bought' | 'sold' | 'cancelled'>('bought');

  const logTrade = useLogTrade();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!itemId || !buyPrice || !quantity) {
      return;
    }

    const tradeData: TradeCreateRequest = {
      user_id: userId,
      item_id: Number(itemId),
      buy_price: Number(buyPrice),
      quantity: Number(quantity),
      sell_price: sellPrice ? Number(sellPrice) : null,
      status: status,
    };

    try {
      await logTrade.mutateAsync(tradeData);
      // Reset form
      setItemId('');
      setItemName('');
      setBuyPrice('');
      setSellPrice('');
      setQuantity(1);
      setStatus('bought');
      onSuccess?.();
    } catch (error) {
      // Error is handled by mutation
    }
  };

  return (
    <Card withBorder shadow="sm" p="md">
      <form onSubmit={handleSubmit}>
        <Stack gap="md">
          <Text fw={500} size="lg">Log Trade</Text>

          {logTrade.isError && (
            <Alert icon={<IconAlertCircle size={16} />} title="Error" color="red">
              {logTrade.error instanceof Error ? logTrade.error.message : 'Failed to log trade'}
            </Alert>
          )}

          {logTrade.isSuccess && (
            <Alert icon={<IconCheck size={16} />} title="Success" color="green">
              Trade logged successfully!
            </Alert>
          )}

          <Group grow>
            <NumberInput
              label="Item ID"
              placeholder="Enter item ID"
              value={itemId}
              onChange={(value) => setItemId(value === '' ? '' : Number(value))}
              required
              min={1}
            />
            <TextInput
              label="Item Name"
              placeholder="Item name (optional)"
              value={itemName}
              onChange={(e) => setItemName(e.target.value)}
            />
          </Group>

          <Group grow>
            <NumberInput
              label="Buy Price (GP)"
              placeholder="Price per item"
              value={buyPrice}
              onChange={(value) => setBuyPrice(value === '' ? '' : Number(value))}
              required
              min={1}
              leftSection={<Text size="xs">GP</Text>}
            />
            <NumberInput
              label="Sell Price (GP)"
              placeholder="Price per item (if sold)"
              value={sellPrice}
              onChange={(value) => setSellPrice(value === '' ? '' : Number(value))}
              min={1}
              leftSection={<Text size="xs">GP</Text>}
            />
          </Group>

          <Group grow>
            <NumberInput
              label="Quantity"
              placeholder="Number of items"
              value={quantity}
              onChange={(value) => setQuantity(value === '' ? '' : Number(value))}
              required
              min={1}
            />
            <Select
              label="Status"
              value={status}
              onChange={(value) => setStatus(value as 'bought' | 'sold' | 'cancelled')}
              data={[
                { value: 'bought', label: 'Bought' },
                { value: 'sold', label: 'Sold' },
                { value: 'cancelled', label: 'Cancelled' },
              ]}
            />
          </Group>

          <Button
            type="submit"
            loading={logTrade.isPending}
            fullWidth
          >
            Log Trade
          </Button>
        </Stack>
      </form>
    </Card>
  );
}
