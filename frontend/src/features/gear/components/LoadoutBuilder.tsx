import {
  Card,
  Stack,
  TextInput,
  NumberInput,
  Button,
  Group,
  Text,
  ActionIcon,
} from '@mantine/core';
import { IconPlus, IconTrash } from '@tabler/icons-react';
import type { LoadoutInput } from '../types';

interface LoadoutBuilderProps {
  loadouts: LoadoutInput[];
  onLoadoutsChange: (loadouts: LoadoutInput[]) => void;
}

const EQUIPMENT_SLOTS = [
  'weapon',
  'head',
  'cape',
  'neck',
  'ammo',
  'body',
  'legs',
  'feet',
  'hands',
  'shield',
  'ring',
];

export function LoadoutBuilder({ loadouts, onLoadoutsChange }: LoadoutBuilderProps) {
  const addLoadout = () => {
    const newLoadout: LoadoutInput = {
      name: `Loadout ${loadouts.length + 1}`,
      loadout: {},
    };
    onLoadoutsChange([...loadouts, newLoadout]);
  };

  const removeLoadout = (index: number) => {
    onLoadoutsChange(loadouts.filter((_, i) => i !== index));
  };

  const updateLoadoutName = (index: number, name: string) => {
    const updated = [...loadouts];
    updated[index].name = name;
    onLoadoutsChange(updated);
  };

  const updateLoadoutItem = (loadoutIndex: number, slot: string, itemId: number | null) => {
    const updated = [...loadouts];
    updated[loadoutIndex].loadout[slot] = itemId;
    onLoadoutsChange(updated);
  };

  return (
    <Card withBorder shadow="sm" p="md">
      <Stack gap="md">
        <Group justify="space-between">
          <Text fw={500} size="lg">Loadouts</Text>
          <Button
            size="xs"
            leftSection={<IconPlus size={14} />}
            onClick={addLoadout}
            disabled={loadouts.length >= 10}
          >
            Add Loadout
          </Button>
        </Group>

        {loadouts.map((loadout, loadoutIndex) => (
          <Card key={loadoutIndex} withBorder p="sm" radius="md">
            <Stack gap="sm">
              <Group justify="space-between">
                <TextInput
                  placeholder="Loadout name"
                  value={loadout.name}
                  onChange={(e) => updateLoadoutName(loadoutIndex, e.target.value)}
                  style={{ flex: 1 }}
                />
                {loadouts.length > 1 && (
                  <ActionIcon
                    color="red"
                    variant="light"
                    onClick={() => removeLoadout(loadoutIndex)}
                  >
                    <IconTrash size={16} />
                  </ActionIcon>
                )}
              </Group>

              <Group gap="xs">
                {EQUIPMENT_SLOTS.map((slot) => (
                  <NumberInput
                    key={slot}
                    placeholder={slot}
                    value={loadout.loadout[slot] || ''}
                    onChange={(value) => updateLoadoutItem(loadoutIndex, slot, value ? Number(value) : null)}
                    min={1}
                    style={{ width: 120 }}
                    size="xs"
                  />
                ))}
              </Group>
            </Stack>
          </Card>
        ))}

        {loadouts.length === 0 && (
          <Text c="dimmed" ta="center" py="md">
            No loadouts added. Click "Add Loadout" to get started!
          </Text>
        )}
      </Stack>
    </Card>
  );
}
