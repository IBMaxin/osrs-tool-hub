import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { 
  Container, 
  Title, 
  Group, 
  Text, 
  Stack,
  Button
} from '@mantine/core';
import { IconRefresh } from '@tabler/icons-react';
import { FlippingApi, FlipFilters } from '../../lib/api';
import { FiltersBar } from './components/FiltersBar';
import { ResultsTable } from './components/ResultsTable';
import { IconArrowsSort, IconSortAscending, IconSortDescending } from '@tabler/icons-react';

type SortField = 'roi' | 'margin' | 'potential_profit' | 'buy_price';
type SortDirection = 'asc' | 'desc';

export function FlippingPage() {
  // Filters State
  const [filters, setFilters] = useState<FlipFilters>({
    max_budget: undefined,
    min_roi: 0.0,
    min_volume: 0
  });

  // Sorting State
  const [sortField, setSortField] = useState<SortField>('potential_profit');
  const [sortDirection, setSortDirection] = useState<SortDirection>('desc');

  // Fetch Flips
  const { data: flips, isLoading, error, refetch, isRefetching } = useQuery({
    queryKey: ['flips', filters],
    queryFn: () => FlippingApi.getOpportunities(filters),
    staleTime: 60000, // Cache for 60s
    retry: 2,
  });

  // Sort flips
  const sortedFlips = flips ? [...flips].sort((a, b) => {
    let aVal: number;
    let bVal: number;
    
    switch (sortField) {
      case 'roi':
        aVal = a.roi;
        bVal = b.roi;
        break;
      case 'margin':
        aVal = a.margin;
        bVal = b.margin;
        break;
      case 'potential_profit':
        aVal = a.potential_profit || 0;
        bVal = b.potential_profit || 0;
        break;
      case 'buy_price':
        aVal = a.buy_price;
        bVal = b.buy_price;
        break;
      default:
        return 0;
    }
    
    if (sortDirection === 'asc') {
      return aVal - bVal;
    }
    return bVal - aVal;
  }) : [];

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('desc');
    }
  };

  const SortIcon = ({ field }: { field: SortField }) => {
    if (sortField !== field) return <IconArrowsSort size={14} />;
    return sortDirection === 'asc' ? <IconSortAscending size={14} /> : <IconSortDescending size={14} />;
  };

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
