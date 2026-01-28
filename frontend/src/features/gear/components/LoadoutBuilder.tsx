import { useState } from 'react';
import {
  Card,
  Stack,
  TextInput,
  Button,
  Group,
  Text,
  ActionIcon,
  SimpleGrid,
} from '@mantine/core';
import { IconPlus, IconTrash } from '@tabler/icons-react';
import type { LoadoutInput } from '../types';
import { ItemPickerModal } from './ItemPickerModal';
import { LoadoutItemDisplay } from './LoadoutItemDisplay';

interface LoadoutBuilderProps {
  loadouts: LoadoutInput[];
  onLoadoutsChange: (loadouts: LoadoutInput[]) => void;
  combatStyle?: 'melee' | 'ranged' | 'magic';
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

export function LoadoutBuilder({
  loadouts,
  onLoadoutsChange,
  combatStyle = 'melee',
}: LoadoutBuilderProps) {
  const [pickerModal, setPickerModal] = useState<{
    opened: boolean;
    loadoutIndex: number;
    slot: string;
  }>({ opened: false, loadoutIndex: -1, slot: '' });

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

  const openPicker = (loadoutIndex: number, slot: string) => {
    setPickerModal({ opened: true, loadoutIndex, slot });
  };

  const handleItemSelect = (itemId: number) => {
    updateLoadoutItem(pickerModal.loadoutIndex, pickerModal.slot, itemId);
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

              <SimpleGrid cols={{ base: 2, sm: 3, md: 4 }} spacing="xs">
                {EQUIPMENT_SLOTS.map((slot) => (
                  <LoadoutItemDisplay
                    key={slot}
                    itemId={loadout.loadout[slot] ?? null}
                    slot={slot}
                    onClick={() => openPicker(loadoutIndex, slot)}
                    onRemove={() => updateLoadoutItem(loadoutIndex, slot, null)}
                  />
                ))}
              </SimpleGrid>
            </Stack>
          </Card>
        ))}

        {loadouts.length === 0 && (
          <Text c="dimmed" ta="center" py="md">
            No loadouts added. Click "Add Loadout" to get started!
          </Text>
        )}
      </Stack>

      {pickerModal.opened && (
        <ItemPickerModal
          opened={pickerModal.opened}
          onClose={() => setPickerModal({ opened: false, loadoutIndex: -1, slot: '' })}
          slot={pickerModal.slot}
          combatStyle={combatStyle}
          onSelect={handleItemSelect}
        />
      )}
    </Card>
  );
}
