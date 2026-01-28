import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { WatchlistApi, WatchlistItem, WatchlistAlert, WatchlistCreateRequest } from '../../../lib/api';

/**
 * Hook for fetching watchlist items.
 */
export function useWatchlist(userId: string, includeInactive: boolean = false) {
  return useQuery({
    queryKey: ['watchlist', userId, includeInactive],
    queryFn: () => WatchlistApi.getWatchlist(userId, includeInactive),
    enabled: !!userId,
    staleTime: 30000, // 30 seconds
  });
}

/**
 * Hook for fetching watchlist alerts.
 */
export function useWatchlistAlerts(userId: string, limit: number = 50) {
  return useQuery({
    queryKey: ['watchlistAlerts', userId, limit],
    queryFn: () => WatchlistApi.getAlerts(userId, limit),
    enabled: !!userId,
    staleTime: 30000, // 30 seconds
    refetchInterval: 60000, // Refetch every minute to check for new alerts
  });
}

/**
 * Hook for adding an item to the watchlist.
 */
export function useAddToWatchlist() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (watchlist: WatchlistCreateRequest) => WatchlistApi.addToWatchlist(watchlist),
    onSuccess: (data) => {
      // Invalidate and refetch watchlist
      queryClient.invalidateQueries({ queryKey: ['watchlist', data.user_id] });
    },
  });
}

/**
 * Hook for removing an item from the watchlist.
 */
export function useRemoveFromWatchlist() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ watchlistItemId, userId }: { watchlistItemId: number; userId: string }) =>
      WatchlistApi.removeFromWatchlist(watchlistItemId, userId),
    onSuccess: (_, variables) => {
      // Invalidate and refetch watchlist and alerts
      queryClient.invalidateQueries({ queryKey: ['watchlist', variables.userId] });
      queryClient.invalidateQueries({ queryKey: ['watchlistAlerts', variables.userId] });
    },
  });
}
