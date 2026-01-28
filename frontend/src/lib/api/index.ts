/**
 * API client exports
 * Centralized exports for all API clients and types
 */

import { apiClient } from './client';
import type {
  Trade,
  TradeCreateRequest,
  TradeStats,
  TradeFilters,
  WatchlistItem,
  WatchlistAlert,
  WatchlistCreateRequest,
} from '../../features/flipping/types';

export { apiClient } from './client';
export { FlippingApi } from './flipping';
export { GearApi, fetchFullProgression, type SlayerGearResponse } from './gear';
export { SlayerApi, type SlayerStats } from './slayer';

// Legacy function exports for backward compatibility
export { fetchFullProgression as fetchWikiProgression } from './gear';

export type {
  FlipFilters,
  FlipOpportunity,
  SlayerTask,
  TaskAdvice,
  ProgressionItem,
  ProgressionTier,
  FullProgressionResponse,
  SlotProgressionResponse,
} from './types';
export type {
  DPSComparisonRequest,
  DPSComparisonResponse,
  DPSComparisonResult,
  LoadoutInput,
} from '../../features/gear/types';
export type {
  Trade,
  TradeCreateRequest,
  TradeStats,
  TradeFilters,
  WatchlistItem,
  WatchlistAlert,
  WatchlistCreateRequest,
} from '../../features/flipping/types';

// Trade API
export const TradeApi = {
  getTrades: async (userId: string, filters: TradeFilters = {}): Promise<Trade[]> => {
    const params = new URLSearchParams();
    params.append('user_id', userId);
    if (filters.status) params.append('status', filters.status);
    if (filters.item_id != null) params.append('item_id', filters.item_id.toString());
    if (filters.start_date) params.append('start_date', filters.start_date);
    if (filters.end_date) params.append('end_date', filters.end_date);
    if (filters.limit != null) params.append('limit', filters.limit.toString());
    const res = await apiClient.get<Trade[]>('/trades', { params });
    return res.data;
  },
  getStats: async (userId: string, days?: number): Promise<TradeStats> => {
    const params = new URLSearchParams();
    params.append('user_id', userId);
    if (days != null) params.append('days', days.toString());
    const res = await apiClient.get<TradeStats>('/trades/stats', { params });
    return res.data;
  },
  createTrade: async (trade: TradeCreateRequest): Promise<Trade> => {
    const res = await apiClient.post<Trade>('/trades', trade);
    return res.data;
  },
  updateTrade: async (id: number, trade: Partial<TradeCreateRequest>): Promise<Trade> => {
    const res = await apiClient.put<Trade>(`/trades/${id}`, trade);
    return res.data;
  },
  deleteTrade: async (id: number): Promise<void> => {
    await apiClient.delete(`/trades/${id}`);
  },
};

// Watchlist API
export const WatchlistApi = {
  getWatchlist: async (userId: string, includeInactive = false): Promise<WatchlistItem[]> => {
    const params = new URLSearchParams();
    params.append('user_id', userId);
    if (includeInactive) params.append('include_inactive', 'true');
    const res = await apiClient.get<WatchlistItem[]>('/watchlist', { params });
    return res.data;
  },
  getAlerts: async (userId: string, limit = 50): Promise<WatchlistAlert[]> => {
    const params = new URLSearchParams();
    params.append('user_id', userId);
    params.append('limit', limit.toString());
    const res = await apiClient.get<WatchlistAlert[]>('/watchlist/alerts', { params });
    return res.data;
  },
  addToWatchlist: async (watchlist: WatchlistCreateRequest): Promise<WatchlistItem> => {
    const res = await apiClient.post<WatchlistItem>('/watchlist', watchlist);
    return res.data;
  },
  removeFromWatchlist: async (watchlistItemId: number, userId: string): Promise<void> => {
    const params = new URLSearchParams();
    params.append('user_id', userId);
    await apiClient.delete(`/watchlist/${watchlistItemId}`, { params });
  },
};
