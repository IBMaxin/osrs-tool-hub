/**
 * Hook to fetch wiki guide data for a combat style.
 */

import { useQuery } from '@tanstack/react-query';
import { fetchWikiGuide } from '../../../lib/api/gear';

export function useWikiGuide(style: string) {
  return useQuery({
    queryKey: ['wiki-guide', style],
    queryFn: () => fetchWikiGuide(style),
    staleTime: 1000 * 60 * 10, // 10 minutes
  });
}
