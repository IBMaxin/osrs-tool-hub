import { useMutation } from '@tanstack/react-query';
import { GearApi, DPSComparisonRequest } from '../../../lib/api';

/**
 * Hook for comparing DPS of multiple loadouts.
 */
export function useCompareDPS() {
  return useMutation({
    mutationFn: (request: DPSComparisonRequest) => GearApi.compareDPS(request),
  });
}
