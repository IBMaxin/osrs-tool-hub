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

// Trade types
export interface Trade {
  id: number;
  user_id: string;
  item_id: number;
  item_name: string;
  buy_price: number;
  sell_price: number | null;
  quantity: number;
  profit: number;
  status: 'bought' | 'sold' | 'cancelled';
  created_at: string;
  updated_at: string;
}

export interface TradeCreateRequest {
  user_id: string;
  item_id: number;
  buy_price: number;
  quantity: number;
  sell_price?: number | null;
  status?: 'bought' | 'sold' | 'cancelled';
}

export interface TradeStats {
  total_profit: number;
  total_trades: number;
  sold_trades: number;
  profit_per_hour: number;
  best_items: Array<{
    item_name: string;
    profit: number;
  }>;
  profit_by_item: Record<string, number>;
}

export interface TradeFilters {
  status?: 'bought' | 'sold' | 'cancelled';
  item_id?: number;
  start_date?: string;
  end_date?: string;
  limit?: number;
}

// Watchlist types
export interface WatchlistItem {
  id: number;
  user_id: string;
  item_id: number;
  item_name: string;
  alert_type: 'price_below' | 'price_above' | 'margin_above';
  threshold: number;
  is_active: boolean;
  created_at: string;
  last_triggered_at: string | null;
}

export interface WatchlistAlert {
  id: number;
  watchlist_item_id: number;
  triggered_at: string;
  current_value: number;
  threshold_value: number;
  message: string;
}

export interface WatchlistCreateRequest {
  user_id: string;
  item_id: number;
  alert_type: 'price_below' | 'price_above' | 'margin_above';
  threshold: number;
}
