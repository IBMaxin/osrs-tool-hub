import { useState, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { IconArrowsSort, IconSortAscending, IconSortDescending } from '@tabler/icons-react';
import { FlippingApi } from '../../../lib/api';
import type { SortField, SortDirection, UseFlipsOptions, UseFlipsReturn } from '../types';

export function useFlips(options: UseFlipsOptions): UseFlipsReturn {
  const { filters } = options;

  // Sorting State
  const [sortField, setSortField] = useState<SortField>('potential_profit');
  const [sortDirection, setSortDirection] = useState<SortDirection>('desc');

  // Fetch Flips
  const { data: flips, isLoading, error, refetch, isRefetching } = useQuery({
    queryKey: ['flips', filters],
    queryFn: () => FlippingApi.getOpportunities(filters),
    staleTime: 300000, // Cache for 5 minutes (matches backend update interval)
    retry: 2,
  });

  // Sort flips
  const sortedFlips = useMemo(() => {
    if (!flips) return [];
    
    return [...flips].sort((a, b) => {
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
    });
  }, [flips, sortField, sortDirection]);

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

  return {
    flips: flips || [],
    sortedFlips,
    isLoading,
    error: error as Error | null,
    refetch,
    isRefetching,
    sortField,
    sortDirection,
    handleSort,
    SortIcon,
  };
}
