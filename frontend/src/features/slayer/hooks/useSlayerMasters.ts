import { useQuery } from '@tanstack/react-query';
import { SlayerApi } from '../../../lib/api';
import type { UseSlayerMastersReturn } from '../types';

export function useSlayerMasters(): UseSlayerMastersReturn {
  const { data: masters, isLoading } = useQuery({
    queryKey: ['slayerMasters'],
    queryFn: SlayerApi.getMasters
  });

  return {
    masters,
    isLoading,
  };
}
