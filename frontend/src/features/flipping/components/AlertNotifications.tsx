import {
  Card,
  Stack,
  Text,
  Alert,
  Group,
  Badge,
  Title,
} from '@mantine/core';
import { IconBell, IconAlertCircle } from '@tabler/icons-react';
import { useWatchlistAlerts } from '../hooks/useWatchlist';
import { formatNumber } from '../utils/format';
import type { WatchlistAlert } from '../types';

interface AlertNotificationsProps {
  userId: string;
}

export function AlertNotifications({ userId }: AlertNotificationsProps) {
  const { data: alerts, isLoading, error } = useWatchlistAlerts(userId, 20);

  if (error) {
    return (
      <Card withBorder shadow="sm" p="md">
        <Alert icon={<IconAlertCircle size={16} />} title="Error" color="red">
          {error instanceof Error ? error.message : 'Failed to load alerts'}
        </Alert>
      </Card>
    );
  }

  return (
    <Card withBorder shadow="sm" p="md">
      <Stack gap="md">
        <Group justify="space-between">
          <Title order={4}>Alert Notifications</Title>
          {alerts && alerts.length > 0 && (
            <Badge color="red" size="lg">{alerts.length}</Badge>
          )}
        </Group>

        {isLoading ? (
          <Text c="dimmed">Loading alerts...</Text>
        ) : !alerts || alerts.length === 0 ? (
          <Text c="dimmed">No alerts triggered. Set up watchlist items to receive alerts!</Text>
        ) : (
          <Stack gap="sm">
            {alerts.map((alert: WatchlistAlert) => (
              <Alert
                key={alert.id}
                icon={<IconBell size={16} />}
                title={alert.message}
                color="blue"
                variant="light"
              >
                <Group gap="md" mt="xs">
                  <Text size="sm">
                    Current: {formatNumber(alert.current_value)} GP
                  </Text>
                  <Text size="sm">
                    Threshold: {formatNumber(alert.threshold_value)} GP
                  </Text>
                  <Text size="xs" c="dimmed">
                    {new Date(alert.triggered_at).toLocaleString()}
                  </Text>
                </Group>
              </Alert>
            ))}
          </Stack>
        )}
      </Stack>
    </Card>
  );
}
