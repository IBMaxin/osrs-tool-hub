/**
 * Types specific to the slayer feature.
 */

export interface UseSlayerMastersReturn {
  masters: string[] | undefined;
  isLoading: boolean;
}

export interface UseSlayerTasksOptions {
  selectedMaster: string | null;
}

export interface UseSlayerTasksReturn {
  tasks: any[] | undefined;
  isLoading: boolean;
  error: Error | null;
}

export interface UseSlayerAdviceOptions {
  selectedTaskId: number | null;
  enabled: boolean;
}

export interface UseSlayerAdviceReturn {
  advice: any | undefined;
  isLoading: boolean;
}
