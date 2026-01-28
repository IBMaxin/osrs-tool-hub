/**
 * Gear API client
 * Handles all gear-related API requests
 */

import { apiClient } from './client';
import type { DPSComparisonRequest, DPSComparisonResponse } from '../../features/gear/types';
import type { FullProgressionResponse } from './types';

export class GearApi {
  /**
   * Compare DPS for multiple loadouts side-by-side
   */
  static async compareDPS(request: DPSComparisonRequest): Promise<DPSComparisonResponse> {
    const response = await apiClient.post<DPSComparisonResponse>('/dps/compare', request);
    return response.data;
  }
}

/** Fetch full gear progression for a combat style (melee, ranged, magic). */
export async function fetchFullProgression(style: string): Promise<FullProgressionResponse> {
  const response = await apiClient.get<FullProgressionResponse>(`/gear/progression/${style}`);
  return response.data;
}
