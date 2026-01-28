import { apiClient } from './client';
import type { FlipFilters, FlipOpportunity } from './types';

/**
 * Flipping API client.
 */
export class FlippingApi {
  /**
   * Get flip opportunities based on filters.
   */
  static async getOpportunities(filters: FlipFilters = {}): Promise<FlipOpportunity[]> {
    const params = new URLSearchParams();
    
    if (filters.max_budget !== undefined) {
      params.append('max_budget', filters.max_budget.toString());
    }
    if (filters.min_roi !== undefined) {
      params.append('min_roi', filters.min_roi.toString());
    }
    if (filters.min_volume !== undefined) {
      params.append('min_volume', filters.min_volume.toString());
    }

    const response = await apiClient.get<FlipOpportunity[]>(
      `/flips/opportunities?${params.toString()}`
    );
    return response.data;
  }
}

/**
 * Legacy function export for backward compatibility.
 * @deprecated Use FlippingApi.getOpportunities instead
 */
export async function fetchFlips(filters: FlipFilters = {}): Promise<FlipOpportunity[]> {
  return FlippingApi.getOpportunities(filters);
}
