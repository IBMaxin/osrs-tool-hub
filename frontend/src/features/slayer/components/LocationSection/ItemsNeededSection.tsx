import { Stack, Text, Group, Badge, Divider } from '@mantine/core';
import { IconPackage } from '@tabler/icons-react';

interface ItemsNeededSectionProps {
  itemsNeeded: string[];
}

export function ItemsNeededSection({ itemsNeeded }: ItemsNeededSectionProps) {
  if (itemsNeeded.length === 0) return null;

  return (
    <>
      <Divider color="osrsBrown.6" />
      <Stack gap="xs">
        <Group gap="xs">
          <IconPackage size={18} style={{ color: 'var(--mantine-color-osrsGold-5)' }} />
          <Text fw={700} c="osrsGold.4">
            ITEMS NEEDED
          </Text>
        </Group>
        <Group gap="xs">
          {itemsNeeded.map((item, i) => (
            <Badge key={i} size="md" color="osrsGold" variant="dot">
              {item}
            </Badge>
          ))}
        </Group>
      </Stack>
    </>
  );
}
