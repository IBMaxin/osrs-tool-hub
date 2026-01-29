import {
  Stack,
  Text,
  Group,
  Badge,
  Divider,
  Accordion,
  Card,
} from '@mantine/core';
import {
  IconSword,
  IconPackage,
  IconWand,
} from '@tabler/icons-react';

export interface Alternative {
  name: string;
  notes: string;
  recommended_for?: string;
}

interface StrategySectionProps {
  strategy: string;
  weaknesses: string[];
  itemsNeeded: string[];
  alternatives: Alternative[];
}

export function StrategySection({
  strategy,
  weaknesses,
  itemsNeeded,
  alternatives,
}: StrategySectionProps) {
  return (
    <>
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
    </>
  );
}
