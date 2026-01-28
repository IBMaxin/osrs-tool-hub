import { apiClient } from './client';
import type { SlayerTask, TaskAdvice, TaskLocationData } from './types';

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

  static async getAdvice(taskId: number): Promise<TaskAdvice> {
    const response = await apiClient.get<TaskAdvice>(`/slayer/advice/${taskId}`);
    return response.data;
  }

  static async getLocation(taskId: number): Promise<TaskLocationData> {
    const response = await apiClient.get<TaskLocationData>(`/slayer/location/${taskId}`);
    return response.data;
  }
}
