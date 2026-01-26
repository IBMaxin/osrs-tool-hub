import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { 
  Container, 
  Title, 
  Table, 
  Paper, 
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
  Tooltip
} from '@mantine/core';
import { IconCoins, IconTrendingUp, IconFilter } from '@tabler/icons-react';
import { FlippingApi, FlipFilters } from '../../lib/api';

export function FlippingPage() {
  // Filters State
  const [filters, setFilters] = useState<FlipFilters>({
    max_budget: undefined,
    min_roi: 1.0,
    min_volume: 10
  });

  // Fetch Flips
  const { data: flips, isLoading, refetch, isRefetching } = useQuery({
    queryKey: ['flips', filters],
    queryFn: () => FlippingApi.getOpportunities(filters),
    staleTime: 60000, // Cache for 60s
  });

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
        <Group justify="space-between">
          <Title order={2}>Real-time Flip Finder</Title>
          <Button 
            leftSection={<IconTrendingUp size={16} />} 
            onClick={() => refetch()} 
            loading={isRefetching}
            variant="light"
          >
            Refresh Prices
          </Button>
        </Group>
        
        {/* Filters Bar */}
        <Paper p="md" withBorder>
          <Grid align="end">
            <Grid.Col span={{ base: 12, sm: 4 }}>
              <NumberInput
                label="Max Budget (GP)"
                placeholder="Unlimited"
                thousandSeparator=","
                min={0}
                leftSection={<IconCoins size={16} />}
                value={filters.max_budget}
                onChange={(val) => setFilters(prev => ({ ...prev, max_budget: val as number | undefined }))}
              />
            </Grid.Col>
            <Grid.Col span={{ base: 6, sm: 4 }}>
              <NumberInput
                label="Min ROI (%)"
                placeholder="1.0"
                min={0}
                max={100}
                suffix="%"
                value={filters.min_roi}
                onChange={(val) => setFilters(prev => ({ ...prev, min_roi: val as number }))}
              />
            </Grid.Col>
            <Grid.Col span={{ base: 6, sm: 4 }}>
               <NumberInput
                label="Min Volume"
                placeholder="10"
                min={0}
                value={filters.min_volume}
                onChange={(val) => setFilters(prev => ({ ...prev, min_volume: val as number }))}
              />
            </Grid.Col>
          </Grid>
        </Paper>

        {/* Results Table */}
        <Paper p="md" withBorder>
          {isLoading ? (
             <Center p="xl"><Loader /></Center>
          ) : (
            <Table.ScrollContainer minWidth={800}>
              <Table striped highlightOnHover verticalSpacing="sm">
                <Table.Thead>
                  <Table.Tr>
                    <Table.Th>Item</Table.Th>
                    <Table.Th style={{ textAlign: 'right' }}>Buy Price</Table.Th>
                    <Table.Th style={{ textAlign: 'right' }}>Sell Price</Table.Th>
                    <Table.Th style={{ textAlign: 'right' }}>Margin</Table.Th>
                    <Table.Th style={{ textAlign: 'right' }}>ROI</Table.Th>
                    <Table.Th style={{ textAlign: 'right' }}>Potential Profit</Table.Th>
                    <Table.Th style={{ textAlign: 'center' }}>Volume</Table.Th>
                  </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                  {flips?.length === 0 ? (
                    <Table.Tr>
                      <Table.Td colSpan={7} style={{ textAlign: 'center', padding: '2rem' }}>
                        <Text c="dimmed">No profitable flips found with current filters.</Text>
                      </Table.Td>
                    </Table.Tr>
                  ) : (
                    flips?.map((flip) => (
                      <Table.Tr key={flip.item_id}>
                        <Table.Td>
                          <Group gap="sm">
                            <Avatar src={flip.icon_url} size="sm" radius="sm" bg="transparent" />
                            <Stack gap={0}>
                              <Text size="sm" fw={500}>{flip.item_name}</Text>
                              <Text size="xs" c="dimmed">Limit: {flip.limit || '?'}</Text>
                            </Stack>
                          </Group>
                        </Table.Td>
                        <Table.Td style={{ textAlign: 'right', fontFamily: 'monospace' }}>
                           {formatNumber(flip.buy_price)}
                        </Table.Td>
                        <Table.Td style={{ textAlign: 'right', fontFamily: 'monospace' }}>
                           {formatNumber(flip.sell_price)}
                        </Table.Td>
                        <Table.Td style={{ textAlign: 'right' }}>
                          <Text c="green" fw={700} size="sm">
                            {formatGP(flip.margin)}
                          </Text>
                          <Text size="xs" c="dimmed">Tax: {formatGP(flip.tax)}</Text>
                        </Table.Td>
                        <Table.Td style={{ textAlign: 'right' }}>
                          <Badge 
                            variant="light" 
                            color={flip.roi > 5 ? 'green' : flip.roi > 2 ? 'blue' : 'gray'}
                          >
                            {flip.roi.toFixed(2)}%
                          </Badge>
                        </Table.Td>
                        <Table.Td style={{ textAlign: 'right' }}>
                          <Text fw={700} c={flip.potential_profit > 1_000_000 ? 'orange' : 'dark'}>
                             {formatGP(flip.potential_profit)}
                          </Text>
                        </Table.Td>
                        <Table.Td style={{ textAlign: 'center' }}>
                          <Text size="sm">{formatGP(flip.volume)}</Text>
                        </Table.Td>
                      </Table.Tr>
                    ))
                  )}
                </Table.Tbody>
              </Table>
            </Table.ScrollContainer>
          )}
        </Paper>
      </Stack>
    </Container>
  );
}
