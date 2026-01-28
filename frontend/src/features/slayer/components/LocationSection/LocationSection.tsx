import {
  Stack,
  Text,
  Group,
  SimpleGrid,
  Alert,
} from '@mantine/core';
import {
  IconMapPin,
  IconInfoCircle,
} from '@tabler/icons-react';
import { LocationCard } from './LocationCard';
import { StrategySection } from './StrategySection';
import { WeaknessesSection } from './WeaknessesSection';
import { ItemsNeededSection } from './ItemsNeededSection';
import { AlternativesSection } from './AlternativesSection';

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
          <LocationCard key={index} location={location} index={index} />
        ))}
      </SimpleGrid>

      {/* Combat Strategy */}
      <StrategySection strategy={strategy} />

      {/* Weaknesses */}
      <WeaknessesSection weaknesses={weaknesses} />

      {/* Items Needed */}
      <ItemsNeededSection itemsNeeded={itemsNeeded} />

      {/* Alternatives */}
      <AlternativesSection alternatives={alternatives} />
    </Stack>
  );
}
