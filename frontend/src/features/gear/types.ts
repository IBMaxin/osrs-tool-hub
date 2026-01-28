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

// DPS Lab types
export interface LoadoutInput {
  name: string;
  loadout: Record<string, number | null>; // slot -> item_id
}

export interface DPSComparisonRequest {
  loadouts: LoadoutInput[];
  combat_style: 'melee' | 'ranged' | 'magic';
  attack_type?: 'stab' | 'slash' | 'crush';
  player_stats?: {
    attack?: number;
    strength?: number;
    ranged?: number;
    magic?: number;
  };
  target_monster?: Record<string, any>;
}

export interface DPSComparisonResult {
  loadout_id: number;
  loadout_name: string;
  dps: number;
  max_hit: number;
  attack_speed: number;
  attack_speed_seconds: number;
  accuracy: number;
  total_attack_bonus: number;
  total_strength_bonus: number;
  dps_increase?: number;
  dps_increase_percent?: number;
  details: Record<string, any>;
}

export interface DPSComparisonResponse {
  results: DPSComparisonResult[];
}
