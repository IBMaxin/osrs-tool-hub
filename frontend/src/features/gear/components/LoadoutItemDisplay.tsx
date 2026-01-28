import { Card, Group, Text, ActionIcon } from '@mantine/core';
import { IconX } from '@tabler/icons-react';
import { useQuery } from '@tanstack/react-query';
import { GearApi } from '../../../lib/api/gear';

interface LoadoutItemDisplayProps {
  itemId: number | null;
  slot: string;
  onRemove?: () => void;
  onClick?: () => void;
}

export function LoadoutItemDisplay({
  itemId,
  slot,
  onRemove,
  onClick,
}: LoadoutItemDisplayProps) {
  const { data: item, isLoading, error } = useQuery({
    queryKey: ['item', itemId],
    queryFn: () => {
      if (!itemId) return null;
      return GearApi.getItem(itemId);
    },
    enabled: !!itemId,
    staleTime: 1000 * 60 * 60, // Cache for 1 hour
    retry: 1,
  });

  if (!itemId) {
    return (
      <Card
        p="xs"
        withBorder
        style={{
          cursor: onClick ? 'pointer' : 'default',
          minHeight: 60,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
        onClick={onClick}
      >
        <Text size="sm" c="dimmed">
          {slot.charAt(0).toUpperCase() + slot.slice(1)}
        </Text>
      </Card>
    );
  }

  if (isLoading) {
    return (
      <Card p="xs" withBorder style={{ minHeight: 60 }}>
        <Text size="sm" c="dimmed">
          Loading...
        </Text>
      </Card>
    );
  }

  if (error) {
    return (
      <Card p="xs" withBorder style={{ minHeight: 60 }}>
        <Text size="sm" c="red">
          Error loading item
        </Text>
      </Card>
    );
  }

  if (!item) {
    return (
      <Card p="xs" withBorder style={{ minHeight: 60 }}>
        <Text size="sm" c="red">
          Item {itemId} not found
        </Text>
      </Card>
    );
  }

  return (
    <Card
      p="xs"
      withBorder
      style={{
        cursor: onClick ? 'pointer' : 'default',
        minHeight: 60,
      }}
      onClick={onClick}
    >
      <Group gap="xs" justify="space-between">
        <Group gap="xs" style={{ flex: 1 }}>
          {item.icon_url && (
            <img
              src={item.icon_url}
              alt={item.name}
              width={24}
              height={24}
              style={{ objectFit: 'contain' }}
            />
          )}
          <Text size="sm" fw={500} style={{ flex: 1 }}>
            {item.name}
          </Text>
        </Group>
        {onRemove && (
          <ActionIcon
            size="sm"
            variant="subtle"
            color="red"
            onClick={(e) => {
              e.stopPropagation();
              onRemove();
            }}
          >
            <IconX size={14} />
          </ActionIcon>
        )}
      </Group>
    </Card>
  );
}
