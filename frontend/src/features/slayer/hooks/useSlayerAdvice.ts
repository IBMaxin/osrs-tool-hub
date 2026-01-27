import { useQuery } from '@tanstack/react-query';
import { SlayerApi } from '../../../lib/api';
import type { UseSlayerAdviceOptions, UseSlayerAdviceReturn } from '../types';

export function useSlayerAdvice(options: UseSlayerAdviceOptions): UseSlayerAdviceReturn {
  const { selectedTaskId, enabled } = options;

  const { data: advice, isLoading } = useQuery({
    queryKey: ['taskAdvice', selectedTaskId],
    queryFn: () => SlayerApi.getAdvice(selectedTaskId!),
    enabled: enabled && !!selectedTaskId
  });

  return {
    advice,
    isLoading,
  };
}
