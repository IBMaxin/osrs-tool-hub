import {
  Stack,
  Text,
  Card,
  Group,
  Badge,
  Divider,
  List,
  ThemeIcon,
  Box,
  SimpleGrid,
  Accordion,
  Alert,
} from '@mantine/core';
import {
  IconMapPin,
  IconCheck,
  IconX,
  IconShield,
  IconSword,
  IconFlame,
  IconWand,
  IconPackage,
  IconUsers,
  IconInfoCircle,
} from '@tabler/icons-react';

interface Location {
  name: string;
  requirements: string[];
  multi_combat: boolean | null;
  cannon: boolean | null;
  safespot: boolean | null;
  notes: string;
  pros: string[];
  cons: string[];
  best_for: string;
}

interface Alternative {
  name: string;
  notes: string;
  recommended_for?: string;
}

interface LocationSectionProps {
  locations: Location[];
  strategy: string;
  weaknesses: string[];
  itemsNeeded: string[];
  alternatives: Alternative[];
  hasDetailedData: boolean;
}

export function LocationSection({
  locations,
  strategy,
  weaknesses,
  itemsNeeded,
  alternatives,
  hasDetailedData,
}: LocationSectionProps) {
  if (!hasDetailedData || locations.length === 0) {
    return (
      <Alert icon={<IconInfoCircle size={16} />} color="yellow" variant="light">
        <Text size="sm">Location data not yet available for this task.</Text>
      </Alert>
    );
  }

  return (
    <Stack gap="md">
      {/* Section Header */}
      <Group gap="xs">
        <IconMapPin size={20} style={{ color: 'var(--mantine-color-osrsGold-5)' }} />
        <Text fw={700} size="lg" c="osrsGold.4">
          WHERE TO KILL
        </Text>
      </Group>

      {/* Location Cards */}
      <SimpleGrid cols={{ base: 1, sm: 2 }} spacing="md">
        {locations.map((location, index) => (
          <Card
            key={index}
            padding="md"
            radius="md"
            withBorder
            style={{
              borderColor: 'var(--mantine-color-osrsBrown-6)',
              borderWidth: '2px',
              backgroundColor: 'var(--mantine-color-osrsBrown-9)',
            }}
          >
            <Stack gap="sm">
              {/* Location Name */}
              <Group justify="space-between">
                <Text fw={700} size="md" c="osrsGold.4">
                  {location.name}
                </Text>
              </Group>

              {/* Requirements */}
              {location.requirements.length > 0 && (
                <Group gap="xs">
                  {location.requirements.map((req, i) => (
                    <Badge key={i} size="xs" color="yellow" variant="dot">
                      {req}
                    </Badge>
                  ))}
                </Group>
              )}

              {/* Attributes */}
              <Group gap="md">
                <Group gap={4}>
                  <ThemeIcon
                    size="sm"
                    color={location.multi_combat ? 'osrsGreen' : 'gray'}
                    variant="light"
                  >
                    <IconUsers size={14} />
                  </ThemeIcon>
                  <Text size="xs" c={location.multi_combat ? 'osrsGreen.4' : 'dimmed'}>
                    Multi
                  </Text>
                </Group>

                <Group gap={4}>
                  <ThemeIcon
                    size="sm"
                    color={location.cannon ? 'osrsGreen' : 'gray'}
                    variant="light"
                  >
                    <IconFlame size={14} />
                  </ThemeIcon>
                  <Text size="xs" c={location.cannon ? 'osrsGreen.4' : 'dimmed'}>
                    Cannon
                  </Text>
                </Group>

                <Group gap={4}>
                  <ThemeIcon
                    size="sm"
                    color={location.safespot ? 'osrsGreen' : 'gray'}
                    variant="light"
                  >
                    <IconShield size={14} />
                  </ThemeIcon>
                  <Text size="xs" c={location.safespot ? 'osrsGreen.4' : 'dimmed'}>
                    Safe
                  </Text>
                </Group>
              </Group>

              <Divider color="osrsBrown.6" />

              {/* Pros */}
              {location.pros.length > 0 && (
                <Box>
                  <Text size="xs" fw={600} c="osrsGreen.4" mb={4}>
                    PROS
                  </Text>
                  <List
                    size="xs"
                    spacing={4}
                    icon={
                      <ThemeIcon size={14} color="osrsGreen" radius="xl">
                        <IconCheck size={10} />
                      </ThemeIcon>
                    }
                  >
                    {location.pros.map((pro, i) => (
                      <List.Item key={i}>
                        <Text size="xs">{pro}</Text>
                      </List.Item>
                    ))}
                  </List>
                </Box>
              )}

              {/* Cons */}
              {location.cons.length > 0 && (
                <Box>
                  <Text size="xs" fw={600} c="osrsRed.4" mb={4}>
                    CONS
                  </Text>
                  <List
                    size="xs"
                    spacing={4}
                    icon={
                      <ThemeIcon size={14} color="osrsRed" radius="xl">
                        <IconX size={10} />
                      </ThemeIcon>
                    }
                  >
                    {location.cons.map((con, i) => (
                      <List.Item key={i}>
                        <Text size="xs">{con}</Text>
                      </List.Item>
                    ))}
                  </List>
                </Box>
              )}

              {/* Best For */}
              <Badge size="sm" color="osrsOrange" variant="light" fullWidth>
                BEST FOR: {location.best_for}
              </Badge>

              {/* Notes */}
              {location.notes && (
                <Text size="xs" c="dimmed" fs="italic">
                  {location.notes}
                </Text>
              )}
            </Stack>
          </Card>
        ))}
      </SimpleGrid>

      {/* Combat Strategy */}
      {strategy && (
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
      )}

      {/* Weaknesses */}
      {weaknesses.length > 0 && (
        <Group gap="xs">
          <Text size="sm" fw={600} c="dimmed">
            Weaknesses:
          </Text>
          {weaknesses.map((weakness, i) => (
            <Badge key={i} size="sm" color="osrsRed" variant="light">
              {weakness}
            </Badge>
          ))}
        </Group>
      )}

      {/* Items Needed */}
      {itemsNeeded.length > 0 && (
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
      )}

      {/* Alternatives */}
      {alternatives.length > 0 && (
        <>
          <Divider color="osrsBrown.6" />
          <Accordion variant="separated" radius="md">
            <Accordion.Item value="alternatives">
              <Accordion.Control
                icon={
                  <IconWand size={18} style={{ color: 'var(--mantine-color-osrsOrange-5)' }} />
                }
              >
                <Text fw={700} c="osrsOrange.4">
                  ALTERNATIVE MONSTERS ({alternatives.length})
                </Text>
              </Accordion.Control>
              <Accordion.Panel>
                <Stack gap="sm">
                  {alternatives.map((alt, i) => (
                    <Card key={i} padding="sm" withBorder radius="sm">
                      <Text fw={600} size="sm" c="osrsGold.4">
                        {alt.name}
                      </Text>
                      <Text size="xs" c="dimmed" mt={4}>
                        {alt.notes}
                      </Text>
                      {alt.recommended_for && (
                        <Badge size="xs" color="osrsOrange" variant="light" mt={4}>
                          Recommended for: {alt.recommended_for}
                        </Badge>
                      )}
                    </Card>
                  ))}
                </Stack>
              </Accordion.Panel>
            </Accordion.Item>
          </Accordion>
        </>
      )}
    </Stack>
  );
}
