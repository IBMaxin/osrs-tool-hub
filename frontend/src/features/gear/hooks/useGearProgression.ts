import { useQuery } from '@tanstack/react-query';
import { fetchFullProgression, type FullProgressionResponse } from '../../../lib/api';
import type { UseGearProgressionOptions, UseGearProgressionReturn } from '../types';

export function useGearProgression(options: UseGearProgressionOptions): UseGearProgressionReturn {
  const { style } = options;

  const { data, isLoading, error } = useQuery<FullProgressionResponse>({
    queryKey: ['gear-progression-full', style],
    queryFn: () => fetchFullProgression(style),
  });

  return {
    data,
    isLoading,
    error: error as Error | null,
  };
}
