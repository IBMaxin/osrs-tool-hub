/**
 * Gear API client
 * Handles all gear-related API requests
 */

import { apiClient } from './client';
import type { DPSComparisonRequest, DPSComparisonResponse } from '../../features/gear/types';
import type { FullProgressionResponse } from './types';

export interface ItemData {
  id: number;
  name: string;
  icon_url?: string | null;
  price: number;
  slot?: string | null;
  members: boolean;
  value: number;
  stats: {
    attack_stab: number;
    attack_slash: number;
    attack_crush: number;
    attack_magic: number;
    attack_ranged: number;
    melee_strength: number;
    ranged_strength: number;
    magic_damage: number;
    prayer_bonus: number;
    defence_stab: number;
    defence_slash: number;
    defence_crush: number;
    defence_magic: number;
    defence_ranged: number;
  };
  requirements: {
    attack: number;
    strength: number;
    defence: number;
    ranged: number;
    magic: number;
    prayer: number;
    quest?: string | null;
    achievement?: string | null;
  };
}

export interface BossData {
  name: string;
  monster_id: number;
  defence_stats: {
    defence_level: number;
    magic_level: number;
    ranged_level: number;
    defence_stab: number;
    defence_slash: number;
    defence_crush: number;
    defence_magic: number;
    defence_ranged: number;
  };
  recommended_styles: string[];
  special_mechanics?: string[];
  weaknesses?: Record<string, boolean>;
  content_tags?: string[];
}

export interface BossesResponse {
  bosses: BossData[];
}

export interface SuggestionsItem {
  id: number;
  name: string;
  relevance?: number; // For sorting only, not displayed
  stats: {
    attack_stab: number;
    attack_slash: number;
    attack_crush: number;
    attack_magic: number;
    attack_ranged: number;
    melee_strength: number;
    ranged_strength: number;
    magic_damage: number;
    defence_stab: number;
    defence_slash: number;
    defence_crush: number;
    defence_magic: number;
    defence_ranged: number;
    prayer_bonus: number;
  };
  icon?: string | null;
}

export class GearApi {
  /**
   * Compare DPS for multiple loadouts side-by-side
   */
  static async compareDPS(request: DPSComparisonRequest): Promise<DPSComparisonResponse> {
    const response = await apiClient.post<DPSComparisonResponse>('/dps/compare', request);
    return response.data;
  }

  /**
   * Get item details by ID
   */
  static async getItem(itemId: number): Promise<ItemData> {
    const response = await apiClient.get<ItemData>(`/gear/items/${itemId}`);
    return response.data;
  }

  /**
   * Get items for a specific slot (suggestions)
   */
  static async getItemsBySlot(
    slot: string,
    style: string = 'melee',
    defenceLevel: number = 99
  ): Promise<SuggestionsItem[]> {
    const response = await apiClient.get<SuggestionsItem[]>('/gear/suggestions', {
      params: { slot, style, defence_level: defenceLevel },
    });
    return response.data;
  }

  /**
   * Get list of available bosses with full data
   */
  static async getBosses(): Promise<BossesResponse> {
    const response = await apiClient.get<BossesResponse>('/gear/bosses');
    return response.data;
  }

  /**
   * Get optimal gear suggestions for a slayer task
   */
  static async getSlayerGear(request: {
    task_id: number;
    stats: Record<string, number>;
    budget?: number;
    combat_style?: 'melee' | 'ranged' | 'magic';
    quests_completed?: string[];
    achievements_completed?: string[];
    ironman?: boolean;
  }): Promise<SlayerGearResponse> {
    const response = await apiClient.post<SlayerGearResponse>('/gear/slayer-gear', request);
    return response.data;
  }
}

export interface SlayerGearResponse {
  task_id: number;
  monster_name: string;
  category: string;
  combat_style: 'melee' | 'ranged' | 'magic';
  attack_type?: 'stab' | 'slash' | 'crush' | null;
  weakness: string[];
  attack_style_recommendation: string;
  tier_loadouts: Array<{
    tier: string;
    level: number;
    loadout: {
      combat_style: string;
      total_cost: number;
      budget_used: number;
      budget_remaining: number;
      dps: {
        dps: number;
        max_hit: number;
        attack_speed: number;
        attack_speed_seconds: number;
        accuracy: number;
        total_attack_bonus: number;
        total_strength_bonus: number;
      };
      slots: Record<string, {
        id: number;
        name: string;
        icon_url?: string | null;
        price: number;
        score: number;
      } | null>;
    };
  }>;
  primary_loadout: {
    combat_style: string;
    total_cost: number;
    budget_used: number;
    budget_remaining: number;
    dps: {
      dps: number;
      max_hit: number;
      attack_speed: number;
      attack_speed_seconds: number;
      accuracy: number;
      total_attack_bonus: number;
      total_strength_bonus: number;
    };
    slots: Record<string, {
      id: number;
      name: string;
      icon_url?: string | null;
      price: number;
      score: number;
    } | null>;
  } | null;
}

/** Fetch full gear progression for a combat style (melee, ranged, magic). */
export async function fetchFullProgression(style: string): Promise<FullProgressionResponse> {
  const response = await apiClient.get<FullProgressionResponse>(`/gear/progression/${style}`);
  return response.data;
}
