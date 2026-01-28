import { apiClient } from './client';
import type { SlayerTask, TaskAdvice, TaskLocationData } from './types';

export interface SlayerStats {
  slayer_level?: number;
  combat_level?: number;
}

/**
 * Slayer API client.
 */
export class SlayerApi {
  static async getMasters(): Promise<string[]> {
    const response = await apiClient.get<string[]>('/slayer/masters');
    return response.data;
  }

  static async getTasks(master: string): Promise<SlayerTask[]> {
    const response = await apiClient.get<SlayerTask[]>(`/slayer/tasks/${master}`);
    return response.data;
  }

  static async getAdvice(taskId: number, stats?: SlayerStats): Promise<TaskAdvice> {
    const params = new URLSearchParams();
    
    // Default to level 85 slayer and 110 combat if not provided
    if (stats?.slayer_level !== undefined) {
      params.append('slayer_level', stats.slayer_level.toString());
    } else {
      params.append('slayer_level', '85');
    }
    
    if (stats?.combat_level !== undefined) {
      params.append('combat_level', stats.combat_level.toString());
    } else {
      params.append('combat_level', '110');
    }
    
    const response = await apiClient.get<TaskAdvice>(`/slayer/advice/${taskId}`, { params });
    return response.data;
  }

  static async getLocation(taskId: number): Promise<TaskLocationData> {
    const response = await apiClient.get<TaskLocationData>(`/slayer/location/${taskId}`);
    return response.data;
  }
}
