/**
 * Types specific to the slayer feature.
 */

import type { SlayerTask, TaskAdvice } from '../../lib/api/types';

export interface UseSlayerMastersReturn {
  masters: string[] | undefined;
  isLoading: boolean;
}

export interface UseSlayerTasksOptions {
  selectedMaster: string | null;
}

export interface UseSlayerTasksReturn {
  tasks: SlayerTask[] | undefined;
  isLoading: boolean;
  error: Error | null;
}

export interface UseSlayerAdviceOptions {
  selectedTaskId: number | null;
  enabled: boolean;
}

export interface UseSlayerAdviceReturn {
  advice: TaskAdvice | undefined;
  isLoading: boolean;
}
