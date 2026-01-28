/**
 * Shared TypeScript types for API requests and responses.
 */

// ============================================================================
// Error Response Types
// ============================================================================

export interface ErrorDetail {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}

export interface ErrorResponse {
  error: ErrorDetail;
}

// ============================================================================
// Flipping API Types
// ============================================================================

export interface FlipFilters {
  max_budget?: number;
  min_roi?: number;
  min_volume?: number;
}

export interface FlipOpportunity {
  item_id: number;
  item_name: string;
  buy_price: number;
  sell_price: number;
  margin: number;
  roi: number;
  volume: number;
  potential_profit?: number;
  limit?: number;
  tax?: number;
  icon_url?: string;
  wiki_url?: string;
}

// ============================================================================
// Slayer API Types
// ============================================================================

export type SlayerMaster = string;

export interface SlayerTask {
  task_id: number;
  monster_name: string;
  monster_id: number;
  category: string;
  amount: string;
  weight: number;
  combat_level: number;
  slayer_xp: number;
  is_skippable: boolean;
  is_blockable: boolean;
}

export interface TaskAdvice {
  task: string;
  category: string;
  master: string;
  recommendation: 'DO' | 'SKIP' | 'BLOCK';
  reason: string;
  stats: {
    hp: number;
    def: number;
    xp: number;
  };
  meta: {
    xp_rate: number;
    profit_rate: number;
    attack_style: string;
    items_needed: string[];
    weakness: string[];
  };
}

export interface TaskLocationData {
  task_id: number;
  monster_name: string;
  monster_id: number;
  category: string;
  master: string;
  locations: Array<{
    name: string;
    requirements: string[];
    multi_combat: boolean | null;
    cannon: boolean | null;
    safespot: boolean | null;
    notes: string;
    pros: string[];
    cons: string[];
    best_for: string;
  }>;
  alternatives: Array<{ name: string; notes: string; recommended_for?: string }>;
  strategy: string;
  weakness: string[];
  items_needed: string[];
  attack_style: string;
  has_detailed_data: boolean;
}

// ============================================================================
// Gear API Types
// ============================================================================

export interface GearSet {
  id: number;
  name: string;
  description?: string;
  items: Record<number, number>;
  total_cost: number;
  created_at: string;
  updated_at: string;
}

export interface GearSetCreate {
  name: string;
  items: Record<number, number>;
  description?: string;
}

export interface ProgressionItem {
  id: number | null;
  name: string;
  icon_url?: string;
  price: number | null;
  wiki_url: string;
  requirements?: {
    attack?: number;
    strength?: number;
    defence?: number;
    ranged?: number;
    magic?: number;
    prayer?: number;
    quest?: string | null;
    achievement?: string | null;
  };
  stats?: {
    melee_strength?: number;
    ranged_strength?: number;
    magic_damage?: number;
    prayer_bonus?: number;
    attack_stab?: number;
    attack_slash?: number;
    attack_crush?: number;
    attack_magic?: number;
    attack_ranged?: number;
  };
  not_found?: boolean;
}

export interface ProgressionTier {
  tier: string;
  items: ProgressionItem[];
}

export interface FullProgressionResponse {
  combat_style: string;
  slots: Record<string, ProgressionTier[]>;
}
