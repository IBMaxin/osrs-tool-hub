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
} from '@mantine/core';
import {
  IconCheck,
  IconX,
  IconShield,
  IconFlame,
  IconUsers,
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

interface LocationCardProps {
  location: Location;
  index: number;
}

export function LocationCard({ location, index }: LocationCardProps) {
  return (
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
  );
}
