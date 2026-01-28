import { useState } from 'react';
import {
  Modal,
  TextInput,
  Stack,
  Card,
  Group,
  Text,
  Loader,
  Center,
  ScrollArea,
} from '@mantine/core';
import { useQuery } from '@tanstack/react-query';
import { GearApi } from '../../../lib/api/gear';

interface ItemPickerModalProps {
  opened: boolean;
  onClose: () => void;
  slot: string;
  combatStyle: 'melee' | 'ranged' | 'magic';
  onSelect: (itemId: number) => void;
}

export function ItemPickerModal({
  opened,
  onClose,
  slot,
  combatStyle,
  onSelect,
}: ItemPickerModalProps) {
  const [search, setSearch] = useState('');

  const { data: items, isLoading, error } = useQuery({
    queryKey: ['items', slot, combatStyle],
    queryFn: () => GearApi.getItemsBySlot(slot, combatStyle),
    enabled: opened,
    staleTime: 1000 * 60 * 60, // Cache for 1 hour
    retry: 1,
  });

  const filteredItems = items?.filter((item) =>
    item.name.toLowerCase().includes(search.toLowerCase())
  ) ?? [];

  const handleSelect = (itemId: number) => {
    onSelect(itemId);
    onClose();
    setSearch('');
  };

  return (
    <Modal
      opened={opened}
      onClose={onClose}
      title={`Select ${slot.charAt(0).toUpperCase() + slot.slice(1)}`}
      size="lg"
    >
      <Stack gap="md">
        <TextInput
          placeholder="Search items..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        {isLoading ? (
          <Center py="xl">
            <Loader />
          </Center>
        ) : error ? (
          <Center py="xl">
            <Text c="red">Failed to load items</Text>
          </Center>
        ) : filteredItems.length === 0 ? (
          <Center py="xl">
            <Text c="dimmed">No items found</Text>
          </Center>
        ) : (
          <ScrollArea h={400}>
            <Stack gap="xs">
              {filteredItems.map((item) => (
                <Card
                  key={item.id}
                  p="sm"
                  withBorder
                  onClick={() => handleSelect(item.id)}
                  style={{ cursor: 'pointer' }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.backgroundColor = 'var(--mantine-color-gray-0)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.backgroundColor = 'transparent';
                  }}
                >
                  <Group gap="sm" align="flex-start">
                    {item.icon && (
                      <img
                        src={item.icon}
                        alt={item.name}
                        width={32}
                        height={32}
                        style={{ objectFit: 'contain' }}
                        onError={(e) => {
                          // Hide image if it fails to load
                          e.currentTarget.style.display = 'none';
                        }}
                      />
                    )}
                    <div style={{ flex: 1 }}>
                      <Text fw={500} size="sm" mb={4}>
                        {item.name}
                      </Text>
                      <Group gap="xs" style={{ flexWrap: 'wrap' }}>
                        {combatStyle === 'melee' && (
                          <>
                            {item.stats.melee_strength > 0 && (
                              <Text size="xs" c="blue">
                                Str: +{item.stats.melee_strength}
                              </Text>
                            )}
                            {Math.max(item.stats.attack_stab, item.stats.attack_slash, item.stats.attack_crush) > 0 && (
                              <Text size="xs" c="orange">
                                Atk: +{Math.max(item.stats.attack_stab, item.stats.attack_slash, item.stats.attack_crush)}
                              </Text>
                            )}
                          </>
                        )}
                        {combatStyle === 'ranged' && (
                          <>
                            {item.stats.ranged_strength > 0 && (
                              <Text size="xs" c="blue">
                                Rng Str: +{item.stats.ranged_strength}
                              </Text>
                            )}
                            {item.stats.attack_ranged > 0 && (
                              <Text size="xs" c="orange">
                                Rng Atk: +{item.stats.attack_ranged}
                              </Text>
                            )}
                          </>
                        )}
                        {combatStyle === 'magic' && (
                          <>
                            {item.stats.magic_damage > 0 && (
                              <Text size="xs" c="blue">
                                Magic Dmg: +{item.stats.magic_damage}%
                              </Text>
                            )}
                            {item.stats.attack_magic > 0 && (
                              <Text size="xs" c="orange">
                                Magic Atk: +{item.stats.attack_magic}
                              </Text>
                            )}
                          </>
                        )}
                        {item.stats.prayer_bonus > 0 && (
                          <Text size="xs" c="yellow">
                            Prayer: +{item.stats.prayer_bonus}
                          </Text>
                        )}
                        {(item.stats.defence_stab + item.stats.defence_slash + item.stats.defence_crush + item.stats.defence_magic + item.stats.defence_ranged) > 0 && (
                          <Text size="xs" c="green">
                            Def: +{item.stats.defence_stab + item.stats.defence_slash + item.stats.defence_crush + item.stats.defence_magic + item.stats.defence_ranged}
                          </Text>
                        )}
                      </Group>
                    </div>
                  </Group>
                </Card>
              ))}
            </Stack>
          </ScrollArea>
        )}
      </Stack>
    </Modal>
  );
}
