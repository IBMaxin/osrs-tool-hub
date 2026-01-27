import { useQuery } from '@tanstack/react-query';
import { SlayerApi } from '../../../lib/api';
import type { UseSlayerTasksOptions, UseSlayerTasksReturn } from '../types';

export function useSlayerTasks(options: UseSlayerTasksOptions): UseSlayerTasksReturn {
  const { selectedMaster } = options;

  const { data: tasks, isLoading, error } = useQuery({
    queryKey: ['slayerTasks', selectedMaster],
    queryFn: async () => {
      try {
        const result = await SlayerApi.getTasks(selectedMaster!);
        if (!Array.isArray(result)) {
          console.error('ERROR: Result is not an array!', result);
          return [];
        }
        return result;
      } catch (error: any) {
        console.error('API Error:', error);
        throw error;
      }
    },
    enabled: !!selectedMaster,
    staleTime: 0,
    gcTime: 0,
    refetchOnMount: true,
    refetchOnWindowFocus: true,
    retry: 1
  });

  return {
    tasks,
    isLoading,
    error: error as Error | null,
  };
}
