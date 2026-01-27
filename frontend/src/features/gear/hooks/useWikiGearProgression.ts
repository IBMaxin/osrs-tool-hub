import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../../../lib/api/client';
import type { UseGearProgressionOptions, UseGearProgressionReturn } from '../types';

export function useWikiGearProgression(options: UseGearProgressionOptions): UseGearProgressionReturn {
  const { style } = options;

  const { data, isLoading, error } = useQuery({
    queryKey: ['wiki-gear', style],
    queryFn: async () => {
      const res = await apiClient.get(`/gear/wiki-progression/${style}`);
      return res.data;
    }
  });

  return {
    data,
    isLoading,
    error: error as Error | null,
  };
}
