/**
 * Types specific to the flipping feature.
 */

export type SortField = 'roi' | 'margin' | 'potential_profit' | 'buy_price';
export type SortDirection = 'asc' | 'desc';

import type { FlipFilters } from '../../lib/api';

export interface UseFlipsOptions {
  filters: FlipFilters;
}

import type { ReactElement } from 'react';

export interface UseFlipsReturn {
  flips: any[];
  sortedFlips: any[];
  isLoading: boolean;
  error: Error | null;
  refetch: () => void;
  isRefetching: boolean;
  sortField: SortField;
  sortDirection: SortDirection;
  handleSort: (field: SortField) => void;
  SortIcon: ({ field }: { field: SortField }) => ReactElement;
}
