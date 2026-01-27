/**
 * Types specific to the gear feature.
 */

export interface UseGearProgressionOptions {
  style: string;
}

export interface UseGearProgressionReturn {
  data: any;
  isLoading: boolean;
  error: Error | null;
}
