import { 
  Card, 
  Box, 
  Table, 
  Group, 
  Text, 
  Stack,
  Center, 
  Select,
  Alert
} from '@mantine/core';
import { IconCoins, IconAlertCircle, IconArrowsSort } from '@tabler/icons-react';
import { FlipOpportunity } from '../../../lib/api';
import { ResultsTableSkeleton } from './ResultsTableSkeleton';
import { ResultsTableHeader } from './ResultsTableHeader';
import { ResultsTableRow } from './ResultsTableRow';

type SortField = 'roi' | 'margin' | 'potential_profit' | 'buy_price';
type SortDirection = 'asc' | 'desc';

interface ResultsTableProps {
  flips: FlipOpportunity[];
  isLoading: boolean;
  error: Error | null;
  sortField: SortField;
  sortDirection: SortDirection; // Used by parent component for sorting logic
  onSort: (field: SortField) => void;
  SortIcon: ({ field }: { field: SortField }) => JSX.Element;
  userId?: string;
}

export function ResultsTable({
  flips,
  isLoading,
  error,
  sortField,
  sortDirection: _sortDirection,
  onSort,
  SortIcon,
  userId
}: ResultsTableProps) {
  if (error) {
    return (
      <Alert icon={<IconAlertCircle size={16} />} title="Error loading flips" color="red">
        {error instanceof Error ? error.message : 'Failed to load flip opportunities. Please try again.'}
      </Alert>
    );
  }

  return (
    <Card withBorder shadow="sm" p={0}>
      {isLoading ? (
        <ResultsTableSkeleton />
      ) : flips.length === 0 ? (
        <Center p="xl">
          <Stack align="center" gap="md">
            <IconCoins size={48} stroke={1.5} color="var(--mantine-color-gray-5)" />
            <div style={{ textAlign: 'center' }}>
              <Text fw={500} size="lg" mb={4}>No flips found</Text>
              <Text c="dimmed" size="sm">
                Try adjusting your filters to see more results.
              </Text>
            </div>
          </Stack>
        </Center>
      ) : (
        <Box p="md">
          <Group justify="space-between" mb="md">
            <Text fw={500} size="sm" c="dimmed">
              Found {flips.length} opportunity{flips.length !== 1 ? 'ies' : ''}
            </Text>
            <Select
              placeholder="Sort by"
              value={sortField}
              onChange={(val) => val && onSort(val as SortField)}
              data={[
                { value: 'potential_profit', label: 'Potential Profit' },
                { value: 'roi', label: 'ROI %' },
                { value: 'margin', label: 'Margin' },
                { value: 'buy_price', label: 'Buy Price' },
              ]}
              leftSection={<IconArrowsSort size={16} />}
              w={200}
            />
          </Group>
          <Table.ScrollContainer minWidth={900} type="native">
            <Table striped highlightOnHover verticalSpacing="md" stickyHeader>
              <ResultsTableHeader sortField={sortField} onSort={onSort} SortIcon={SortIcon} showLogTrade={!!userId} />
              <Table.Tbody>
                {flips.map((flip) => (
                  <ResultsTableRow key={flip.item_id} flip={flip} userId={userId} />
                ))}
              </Table.Tbody>
            </Table>
          </Table.ScrollContainer>
        </Box>
      )}
    </Card>
  );
}
