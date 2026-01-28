import { Stack, Text, Group, Divider } from '@mantine/core';
import { IconSword } from '@tabler/icons-react';

interface StrategySectionProps {
  strategy: string;
}

export function StrategySection({ strategy }: StrategySectionProps) {
  if (!strategy) return null;

  return (
    <>
      <Divider color="osrsBrown.6" />
      <Stack gap="xs">
        <Group gap="xs">
          <IconSword size={18} style={{ color: 'var(--mantine-color-osrsOrange-5)' }} />
          <Text fw={700} c="osrsOrange.4">
            COMBAT STRATEGY
          </Text>
        </Group>
        <Text size="sm" style={{ lineHeight: 1.6 }}>
          {strategy}
        </Text>
      </Stack>
    </>
  );
}
