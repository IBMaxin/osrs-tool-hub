import { useState } from 'react';
import { 
  Container, 
  Title, 
  Group, 
  Text, 
  Stack,
  Button
} from '@mantine/core';
import { IconRefresh } from '@tabler/icons-react';
import { FlipFilters } from '../../lib/api';
import { FiltersBar } from './components/FiltersBar';
import { ResultsTable } from './components/ResultsTable';
import { useFlips } from './hooks/useFlips';

export function FlippingPage() {
  // Filters State
  const [filters, setFilters] = useState<FlipFilters>({
    max_budget: undefined,
    min_roi: 0.0,
    min_volume: 0
  });

  // Use custom hook for flips data and sorting
  const {
    sortedFlips,
    isLoading,
    error,
    refetch,
    isRefetching,
    sortField,
    sortDirection,
    handleSort,
    SortIcon,
  } = useFlips({ filters });

  return (
    <Container size="xl" py="xl">
      <Stack gap="lg">
        <Group justify="space-between" wrap="wrap">
          <div>
            <Title order={2} mb={4}>Flip Finder</Title>
            <Text c="dimmed" size="sm">Find profitable Grand Exchange flips</Text>
          </div>
          <Button 
            leftSection={<IconRefresh size={16} />} 
            onClick={() => refetch()} 
            loading={isRefetching}
            variant="light"
          >
            Refresh
          </Button>
        </Group>
        
        <FiltersBar filters={filters} onFiltersChange={setFilters} />

        <ResultsTable
          flips={sortedFlips}
          isLoading={isLoading}
          error={error}
          sortField={sortField}
          sortDirection={sortDirection}
          onSort={handleSort}
          SortIcon={SortIcon}
        />
      </Stack>
    </Container>
  );
}
