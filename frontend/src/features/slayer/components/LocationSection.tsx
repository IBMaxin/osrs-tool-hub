import {
  Stack,
  Text,
  Group,
  Alert,
  SimpleGrid,
} from '@mantine/core';
import {
  IconMapPin,
  IconInfoCircle,
} from '@tabler/icons-react';
import { LocationCard, type Location } from './LocationSection/LocationCard';
import { StrategySection, type Alternative } from './LocationSection/StrategySection';

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
          <LocationCard key={index} location={location} />
        ))}
      </SimpleGrid>

      {/* Strategy Section */}
      <StrategySection
        strategy={strategy}
        weaknesses={weaknesses}
        itemsNeeded={itemsNeeded}
        alternatives={alternatives}
      />
    </Stack>
  );
}
