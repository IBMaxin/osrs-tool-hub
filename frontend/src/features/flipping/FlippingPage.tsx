import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { 
  Container, 
  Title, 
  Table, 
  Group, 
  Text, 
  Badge, 
  Stack,
  Loader,
  Center,
  NumberInput,
  Grid,
  Button,
  Avatar,
  Alert,
  Card,
  Select,
  Box,
  Divider
} from '@mantine/core';
import { IconCoins, IconFilter, IconAlertCircle, IconRefresh, IconArrowsSort, IconSortAscending, IconSortDescending } from '@tabler/icons-react';
import { FlippingApi, FlipFilters } from '../../lib/api';

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
        aVal = a.potential_profit;
        bVal = b.potential_profit;
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

  // Format GP (e.g., 1.5M, 500k)
  const formatGP = (val: number) => {
    if (val >= 1_000_000) return `${(val / 1_000_000).toFixed(1)}M`;
    if (val >= 1_000) return `${(val / 1_000).toFixed(0)}k`;
    return val.toString();
  };

  const formatNumber = (val: number) => {
    return new Intl.NumberFormat().format(val);
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
        
        {/* Filters Bar */}
        <Card withBorder shadow="sm" p="md">
          <Stack gap="md">
            <Group gap="xs">
              <IconFilter size={18} />
              <Text fw={500} size="sm">Filters</Text>
            </Group>
            <Divider />
            <Grid align="end">
              <Grid.Col span={{ base: 12, sm: 4 }}>
                <NumberInput
                  label="Max Budget (GP)"
                  placeholder="Unlimited"
                  thousandSeparator=","
                  min={0}
                  leftSection={<IconCoins size={16} />}
                  value={filters.max_budget || ''}
                  onChange={(val) => setFilters(prev => ({ ...prev, max_budget: val as number | undefined }))}
                  clearable
                />
              </Grid.Col>
              <Grid.Col span={{ base: 6, sm: 4 }}>
                <NumberInput
                  label="Min ROI (%)"
                  placeholder="0.0"
                  min={0}
                  max={100}
                  step={0.1}
                  decimalScale={1}
                  suffix="%"
                  value={filters.min_roi}
                  onChange={(val) => setFilters(prev => ({ ...prev, min_roi: val as number }))}
                />
              </Grid.Col>
              <Grid.Col span={{ base: 6, sm: 4 }}>
                <NumberInput
                  label="Min Volume"
                  placeholder="0"
                  min={0}
                  value={filters.min_volume}
                  onChange={(val) => setFilters(prev => ({ ...prev, min_volume: val as number }))}
                />
              </Grid.Col>
            </Grid>
          </Stack>
        </Card>

        {/* Error State */}
        {error && (
          <Alert icon={<IconAlertCircle size={16} />} title="Error loading flips" color="red">
            {error instanceof Error ? error.message : 'Failed to load flip opportunities. Please try again.'}
          </Alert>
        )}

        {/* Results Table */}
        <Card withBorder shadow="sm" p={0}>
          {isLoading ? (
            <Center p="xl">
              <Stack align="center" gap="md">
                <Loader size="lg" />
                <Text c="dimmed">Loading flip opportunities...</Text>
              </Stack>
            </Center>
          ) : sortedFlips.length === 0 ? (
            <Center p="xl">
              <Stack align="center" gap="md">
                <IconCoins size={48} stroke={1.5} color="var(--mantine-color-gray-5)" />
                <div style={{ textAlign: 'center' }}>
                  <Text fw={500} size="lg" mb={4}>No flips found</Text>
                  <Text c="dimmed" size="sm">
                    {filters.min_roi > 0 || filters.max_budget || filters.min_volume > 0
                      ? 'Try adjusting your filters to see more results.'
                      : 'No profitable opportunities found at the moment.'}
                  </Text>
                </div>
              </Stack>
            </Center>
          ) : (
            <Box p="md">
              <Group justify="space-between" mb="md">
                <Text fw={500} size="sm" c="dimmed">
                  Found {sortedFlips.length} opportunity{sortedFlips.length !== 1 ? 'ies' : ''}
                </Text>
                <Select
                  placeholder="Sort by"
                  value={sortField}
                  onChange={(val) => val && handleSort(val as SortField)}
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
              <Table.ScrollContainer minWidth={900}>
                <Table striped highlightOnHover verticalSpacing="md">
                  <Table.Thead>
                    <Table.Tr>
                      <Table.Th>Item</Table.Th>
                      <Table.Th style={{ textAlign: 'right' }}>
                        <Group gap={4} justify="flex-end" style={{ cursor: 'pointer' }} onClick={() => handleSort('buy_price')}>
                          <Text size="sm">Buy Price</Text>
                          <SortIcon field="buy_price" />
                        </Group>
                      </Table.Th>
                      <Table.Th style={{ textAlign: 'right' }}>Sell Price</Table.Th>
                      <Table.Th style={{ textAlign: 'right' }}>
                        <Group gap={4} justify="flex-end" style={{ cursor: 'pointer' }} onClick={() => handleSort('margin')}>
                          <Text size="sm">Margin</Text>
                          <SortIcon field="margin" />
                        </Group>
                      </Table.Th>
                      <Table.Th style={{ textAlign: 'right' }}>
                        <Group gap={4} justify="flex-end" style={{ cursor: 'pointer' }} onClick={() => handleSort('roi')}>
                          <Text size="sm">ROI</Text>
                          <SortIcon field="roi" />
                        </Group>
                      </Table.Th>
                      <Table.Th style={{ textAlign: 'right' }}>
                        <Group gap={4} justify="flex-end" style={{ cursor: 'pointer' }} onClick={() => handleSort('potential_profit')}>
                          <Text size="sm">Potential Profit</Text>
                          <SortIcon field="potential_profit" />
                        </Group>
                      </Table.Th>
                      <Table.Th style={{ textAlign: 'center' }}>Volume</Table.Th>
                    </Table.Tr>
                  </Table.Thead>
                  <Table.Tbody>
                    {sortedFlips.map((flip) => (
                      <Table.Tr key={flip.item_id}>
                        <Table.Td>
                          <Group gap="sm">
                            <Avatar src={flip.icon_url} size="md" radius="sm" bg="gray.1">
                              {flip.item_name.charAt(0)}
                            </Avatar>
                            <Stack gap={2}>
                              <Text size="sm" fw={500} lineClamp={1}>{flip.item_name}</Text>
                              <Text size="xs" c="dimmed">Limit: {flip.limit ? formatNumber(flip.limit) : 'N/A'}</Text>
                            </Stack>
                          </Group>
                        </Table.Td>
                        <Table.Td style={{ textAlign: 'right' }}>
                          <Text size="sm" ff="monospace" fw={500}>
                            {formatNumber(flip.buy_price)} GP
                          </Text>
                        </Table.Td>
                        <Table.Td style={{ textAlign: 'right' }}>
                          <Text size="sm" ff="monospace" fw={500}>
                            {formatNumber(flip.sell_price)} GP
                          </Text>
                        </Table.Td>
                        <Table.Td style={{ textAlign: 'right' }}>
                          <Stack gap={2} align="flex-end">
                            <Text c={flip.margin > 0 ? 'green' : 'red'} fw={700} size="sm">
                              {flip.margin > 0 ? '+' : ''}{formatGP(flip.margin)}
                            </Text>
                            <Text size="xs" c="dimmed">Tax: {formatGP(flip.tax)}</Text>
                          </Stack>
                        </Table.Td>
                        <Table.Td style={{ textAlign: 'right' }}>
                          <Badge 
                            variant="light" 
                            color={
                              flip.roi >= 10 ? 'green' : 
                              flip.roi >= 5 ? 'teal' : 
                              flip.roi >= 2 ? 'blue' : 
                              flip.roi >= 0 ? 'gray' : 'red'
                            }
                            size="lg"
                          >
                            {flip.roi >= 0 ? '+' : ''}{flip.roi.toFixed(2)}%
                          </Badge>
                        </Table.Td>
                        <Table.Td style={{ textAlign: 'right' }}>
                          <Text 
                            fw={700} 
                            size="sm"
                            c={
                              flip.potential_profit >= 10_000_000 ? 'orange' :
                              flip.potential_profit >= 1_000_000 ? 'yellow' :
                              'dark'
                            }
                          >
                            {formatGP(flip.potential_profit)}
                          </Text>
                        </Table.Td>
                        <Table.Td style={{ textAlign: 'center' }}>
                          <Text size="sm" c={flip.volume > 0 ? 'dark' : 'dimmed'}>
                            {flip.volume > 0 ? formatGP(flip.volume) : 'N/A'}
                          </Text>
                        </Table.Td>
                      </Table.Tr>
                    ))}
                  </Table.Tbody>
                </Table>
              </Table.ScrollContainer>
            </Box>
          )}
        </Card>
      </Stack>
    </Container>
  );
}
