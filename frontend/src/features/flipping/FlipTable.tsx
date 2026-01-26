import { useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { MantineReactTable, type MRT_ColumnDef } from 'mantine-react-table';
import { Slider, Text, Group, Paper, Title } from '@mantine/core';
import { fetchFlips, type FlipOpportunity } from '../../lib/api';

export function FlipTable() {
  const [maxBudget, setMaxBudget] = useState<number>(10000000); // 10M default
  const [minRoi, setMinRoi] = useState<number>(1); // 1% default

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['flips', maxBudget, minRoi],
    queryFn: async () => {
      try {
        console.log('Fetching flips with params:', { max_budget: maxBudget, min_roi: minRoi });
        const result = await fetchFlips({ max_budget: maxBudget, min_roi: minRoi });
        console.log('Fetched Data:', result);
        console.log('Data length:', result?.length || 0);
        return result;
      } catch (err) {
        console.error('Fetch Error:', err);
        throw err;
      }
    },
    refetchInterval: 60000, // Refresh every minute
  });

  const columns = useMemo<MRT_ColumnDef<FlipOpportunity>[]>(
    () => [
      {
        accessorKey: 'item_name',
        header: 'Item',
        Cell: ({ row }) => (
          <Group gap="xs">
            <img 
              src={row.original.icon_url} 
              alt={row.original.item_name} 
              style={{ width: 32, height: 32 }} 
            />
            <Text fw={500}>{row.original.item_name}</Text>
          </Group>
        ),
      },
      {
        accessorKey: 'buy_price',
        header: 'Buy',
        Cell: ({ cell }) => cell.getValue<number>().toLocaleString(),
      },
      {
        accessorKey: 'sell_price',
        header: 'Sell',
        Cell: ({ cell }) => cell.getValue<number>().toLocaleString(),
      },
      {
        accessorKey: 'margin',
        header: 'Margin',
        Cell: ({ cell }) => {
          const val = cell.getValue<number>();
          return (
            <Text c={val > 0 ? 'green' : 'red'} fw={700}>
              {val.toLocaleString()}
            </Text>
          );
        },
      },
      {
        accessorKey: 'roi',
        header: 'ROI %',
        Cell: ({ cell }) => `${cell.getValue<number>().toFixed(2)}%`,
      },
      {
        accessorKey: 'potential_profit',
        header: 'Potential Profit',
        accessorFn: (row) => row.potential_profit || 0, // Helper for sorting
        Cell: ({ row }) => {
          const val = row.original.potential_profit;
          return val ? (
            <Text fw={700} c="blue">
              {val.toLocaleString()}
            </Text>
          ) : 'N/A';
        },
      },
      {
        accessorKey: 'limit',
        header: 'Limit',
      },
    ],
    []
  );

  return (
    <Paper p="md" shadow="sm" withBorder>
      <Title order={3} mb="md">Flip Finder</Title>
      
      <Group mb="lg" grow>
        <div>
          <Text size="sm">Max Budget: {maxBudget.toLocaleString()} gp</Text>
          <Slider
            value={maxBudget}
            onChange={setMaxBudget}
            min={100000}
            max={100000000}
            step={100000}
          />
        </div>
        <div>
          <Text size="sm">Min ROI: {minRoi}%</Text>
          <Slider
            value={minRoi}
            onChange={setMinRoi}
            min={0}
            max={20}
            step={0.5}
          />
        </div>
      </Group>

      {isError && (
        <Text c="red" mb="md">
          Error loading data: {error instanceof Error ? error.message : 'Unknown error'}
        </Text>
      )}
      
      {!isLoading && !isError && (!data || data.length === 0) && (
        <Text c="dimmed" mb="md" ta="center">
          No flip opportunities found. The database may not have price data yet.
        </Text>
      )}

      <MantineReactTable
        columns={columns}
        data={data || []}
        state={{ isLoading, showProgressBars: isLoading }}
        initialState={{ 
          sorting: [{ id: 'potential_profit', desc: true }],
          pagination: { pageSize: 15, pageIndex: 0 }
        }}
      />
    </Paper>
  );
}
