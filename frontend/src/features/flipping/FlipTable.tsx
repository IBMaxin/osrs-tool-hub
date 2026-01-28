import { useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { MantineReactTable, type MRT_ColumnDef } from 'mantine-react-table';
import { Slider, Text, Group, Paper, Title } from '@mantine/core';
import { FlippingApi, type FlipOpportunity } from '../../lib/api';

export function FlipTable() {
  const [maxBudget, setMaxBudget] = useState<number>(10000000); // 10M default
  const [minRoi, setMinRoi] = useState<number>(1); // 1% default

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['flips', maxBudget, minRoi],
    queryFn: async () => {
      try {
        console.log('Fetching flips with params:', { max_budget: maxBudget, min_roi: minRoi });
        const result = await FlippingApi.getOpportunities({ max_budget: maxBudget, min_roi: minRoi });
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
        Cell: ({ cell }) => (
          <Text c="osrsGold.4">{cell.getValue<number>().toLocaleString()}</Text>
        ),
      },
      {
        accessorKey: 'sell_price',
        header: 'Sell',
        Cell: ({ cell }) => (
          <Text c="osrsGold.4">{cell.getValue<number>().toLocaleString()}</Text>
        ),
      },
      {
        accessorKey: 'margin',
        header: 'Margin',
        Cell: ({ cell }) => {
          const val = cell.getValue<number>();
          return (
            <Text c={val > 0 ? 'osrsGreen.4' : 'osrsRed.4'} fw={700}>
              {val.toLocaleString()}
            </Text>
          );
        },
      },
      {
        accessorKey: 'roi',
        header: 'ROI %',
        Cell: ({ cell }) => (
          <Text c="osrsOrange.4" fw={600}>
            {cell.getValue<number>().toFixed(2)}%
          </Text>
        ),
      },
      {
        accessorKey: 'potential_profit',
        header: 'Potential Profit',
        accessorFn: (row) => row.potential_profit || 0, // Helper for sorting
        Cell: ({ row }) => {
          const val = row.original.potential_profit;
          return val ? (
            <Text fw={700} c="osrsGreen.4">
              {val.toLocaleString()}
            </Text>
          ) : (
            <Text c="dimmed">N/A</Text>
          );
        },
      },
      {
        accessorKey: 'limit',
        header: 'Limit',
        Cell: ({ cell }) => (
          <Text c="osrsGold.4">{cell.getValue<number>()}</Text>
        ),
      },
    ],
    []
  );

  return (
    <Paper p="md" shadow="sm" withBorder>
      <Title order={3} mb="md" c="osrsGold.4">Flip Finder</Title>
      
      <Group mb="lg" grow>
        <div>
          <Text size="sm" c="osrsGold.4" fw={600}>Max Budget: {maxBudget.toLocaleString()} gp</Text>
          <Slider
            value={maxBudget}
            onChange={setMaxBudget}
            min={100000}
            max={100000000}
            step={100000}
            color="osrsGold"
          />
        </div>
        <div>
          <Text size="sm" c="osrsGold.4" fw={600}>Min ROI: {minRoi}%</Text>
          <Slider
            value={minRoi}
            onChange={setMinRoi}
            min={0}
            max={20}
            step={0.5}
            color="osrsGold"
          />
        </div>
      </Group>

      {isError && (
        <Text c="osrsRed.4" mb="md" fw={600}>
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
        mantineTableProps={{
          striped: false,
          highlightOnHover: true,
          withColumnBorders: false,
          withTableBorder: true,
          // @ts-expect-error MRT/Mantine sx typing mismatch
          sx: {
            backgroundColor: '#2B1B0E',
            border: '2px solid #4A360C',
          },
        }}
        mantineTableHeadCellProps={{
          // @ts-expect-error MRT/Mantine sx typing mismatch
          sx: {
            backgroundColor: '#4A360C',
            color: '#FFE799',
            fontWeight: 700,
            borderBottom: '2px solid #8B6914',
            '& .mantine-TableHeadCell-Content': {
              justifyContent: 'space-between',
            },
          },
        }}
        mantineTableBodyCellProps={{
          // @ts-expect-error MRT/Mantine sx typing mismatch
          sx: {
            backgroundColor: '#2B1B0E',
            borderBottom: '1px solid #4A360C',
          },
        }}
        mantineTableBodyRowProps={((_props: { row?: unknown }) => ({
          sx: {
            backgroundColor: '#2B1B0E',
            '&:hover': { backgroundColor: '#4A360C' },
            cursor: 'default',
          },
        })) as any}
        mantinePaginationProps={{
          // @ts-expect-error MRT/Mantine sx typing mismatch
          sx: {
            backgroundColor: '#2B1B0E',
            '& button': {
              color: '#D4AF37',
              '&:hover': { backgroundColor: '#4A360C' },
              '&[data-active]': {
                backgroundColor: '#8B6914',
                color: '#FFE799',
              },
            },
          },
        }}
        mantineProgressProps={{ color: 'osrsOrange' } as any}
      />
    </Paper>
  );
}
