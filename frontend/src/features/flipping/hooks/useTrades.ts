import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { TradeApi, TradeCreateRequest, TradeFilters } from '../../../lib/api';

/**
 * Hook for fetching trade history with filters.
 */
export function useTrades(userId: string, filters: TradeFilters = {}) {
  return useQuery({
    queryKey: ['trades', userId, filters],
    queryFn: () => TradeApi.getTrades(userId, filters),
    enabled: !!userId,
    staleTime: 30000, // 30 seconds
  });
}

/**
 * Hook for fetching trade statistics.
 */
export function useTradeStats(userId: string, days?: number) {
  return useQuery({
    queryKey: ['tradeStats', userId, days],
    queryFn: () => TradeApi.getStats(userId, days),
    enabled: !!userId,
    staleTime: 60000, // 1 minute
  });
}

/**
 * Hook for logging a new trade.
 */
export function useLogTrade() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (trade: TradeCreateRequest) => TradeApi.createTrade(trade),
    onSuccess: (data) => {
      // Invalidate and refetch trades and stats
      queryClient.invalidateQueries({ queryKey: ['trades', data.user_id] });
      queryClient.invalidateQueries({ queryKey: ['tradeStats', data.user_id] });
    },
  });
}
