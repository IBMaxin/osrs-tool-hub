import { Stack, Text, Card, Badge, Divider, Accordion } from '@mantine/core';
import { IconWand } from '@tabler/icons-react';

interface Alternative {
  name: string;
  notes: string;
  recommended_for?: string;
}

interface AlternativesSectionProps {
  alternatives: Alternative[];
}

export function AlternativesSection({ alternatives }: AlternativesSectionProps) {
  if (alternatives.length === 0) return null;

  return (
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
  );
}
