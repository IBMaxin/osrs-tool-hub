import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_URL,
});

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log('🚀 API Request:', config.method?.toUpperCase(), config.url);
    console.log('   Full URL:', (config.baseURL || '') + (config.url || ''));
    return config;
  },
  (error) => {
    console.error('❌ Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log('✅ API Response:', response.status, response.config.url);
    console.log('   Data type:', typeof response.data);
    console.log('   Is array:', Array.isArray(response.data));
    console.log('   Data length:', Array.isArray(response.data) ? response.data.length : 'N/A');
    return response;
  },
  (error) => {
    console.error('❌ Response Error:', error.response?.status, error.config?.url);
    console.error('   Error data:', error.response?.data);
    return Promise.reject(error);
  }
);

// --- Gear Types ---
export interface ItemData {
  id: number | null;
  name: string;
  icon_url?: string;
  price?: number;
  wiki_url?: string;
  stats?: Record<string, number>;
  requirements?: Record<string, number | string>;
  not_found?: boolean;
}

export interface TierData {
  tier: string;
  items: ItemData[];
}

export interface SlotData {
  [key: string]: TierData[];
}

export interface FullProgressionResponse {
  combat_style: string;
  slots: {
    [slot: string]: TierData[];
  };
}

export interface SlotProgressionResponse {
  combat_style: string;
  slot: string;
  tiers: TierData[];
}

// --- Slayer Types ---
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

export interface Location {
  name: string;
  requirements: string[];
  multi_combat: boolean | null;
  cannon: boolean | null;
  safespot: boolean | null;
  notes: string;
  pros: string[];
  cons: string[];
  best_for: string;
}

export interface Alternative {
  name: string;
  notes: string;
  recommended_for?: string;
}

export interface TaskLocationData {
  task_id: number;
  monster_name: string;
  category: string;
  master: string;
  locations: Location[];
  alternatives: Alternative[];
  strategy: string;
  weakness: string[];
  items_needed: string[];
  attack_style: string;
  has_detailed_data: boolean;
}

export interface TaskAdvice {
  task: string;
  category: string;
  master: string;
  recommendation: "DO" | "SKIP" | "BLOCK";
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

export interface SlayerStats {
  slayer_level?: number;
  combat_level?: number;
}

// --- Flipping Types ---
export interface FlipOpportunity {
  item_id: number;
  item_name: string;
  icon_url: string;
  buy_price: number;
  sell_price: number;
  limit: number;
  volume: number;
  margin: number;
  roi: number;
  potential_profit: number;
  tax: number;
}

export interface FlipFilters {
  max_budget?: number;
  min_roi?: number;
  min_volume?: number;
}

// --- API Methods ---

export const fetchFullProgression = async (style: string): Promise<FullProgressionResponse> => {
  const response = await api.get<FullProgressionResponse>(`/gear/progression/${style}`);
  return response.data;
};

export const fetchSlotProgression = async (style: string, slot: string): Promise<SlotProgressionResponse> => {
  const response = await api.get<SlotProgressionResponse>(`/gear/progression/${style}/${slot}`);
  return response.data;
};

// Legacy method alias if needed
export const fetchWikiProgression = fetchFullProgression;

export const SlayerApi = {
  getMasters: async () => {
    const response = await api.get<string[]>('/slayer/masters');
    return response.data;
  },
  
  getTasks: async (master: string) => {
    console.log('SlayerApi.getTasks called with master:', master);
    const url = `/slayer/tasks/${encodeURIComponent(master)}`;
    console.log('API URL:', url);
    try {
      const response = await api.get<SlayerTask[]>(url);
      console.log('API response status:', response.status);
      console.log('API response data length:', response.data?.length);
      return response.data;
    } catch (error: any) {
      console.error('API error details:', {
        message: error.message,
        response: error.response?.data,
        status: error.response?.status,
        url: error.config?.url
      });
      throw error;
    }
  },
  
  getAdvice: async (taskId: number, stats?: SlayerStats) => {
    const params = new URLSearchParams();
    
    // Default to level 85 slayer and 110 combat if not provided
    // These are reasonable mid-high level defaults
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
    
    const response = await api.get<TaskAdvice>(`/slayer/advice/${taskId}`, { params });
    return response.data;
  },
  
  getLocation: async (taskId: number) => {
    const response = await api.get<TaskLocationData>(`/slayer/location/${taskId}`);
    return response.data;
  }
};

export const FlippingApi = {
  getOpportunities: async (filters: FlipFilters = {}) => {
    const params = new URLSearchParams();
    if (filters.max_budget) params.append('max_budget', filters.max_budget.toString());
    if (filters.min_roi) params.append('min_roi', filters.min_roi.toString());
    if (filters.min_volume) params.append('min_volume', filters.min_volume.toString());
    
    const response = await api.get<FlipOpportunity[]>('/flips/opportunities', { params });
    return response.data;
  }
};

// Trade types
export interface Trade {
  id: number;
  user_id: string;
  item_id: number;
  item_name: string;
  buy_price: number;
  sell_price: number | null;
  quantity: number;
  profit: number;
  status: 'bought' | 'sold' | 'cancelled';
  created_at: string;
  updated_at: string;
}

export interface TradeCreateRequest {
  user_id: string;
  item_id: number;
  buy_price: number;
  quantity: number;
  sell_price?: number | null;
  status?: 'bought' | 'sold' | 'cancelled';
}

export interface TradeStats {
  total_profit: number;
  total_trades: number;
  sold_trades: number;
  profit_per_hour: number;
  best_items: Array<{
    item_name: string;
    profit: number;
  }>;
  profit_by_item: Record<string, number>;
}

export interface TradeFilters {
  status?: 'bought' | 'sold' | 'cancelled';
  item_id?: number;
  start_date?: string;
  end_date?: string;
  limit?: number;
}

export const TradeApi = {
  createTrade: async (trade: TradeCreateRequest): Promise<Trade> => {
    const response = await api.post<Trade>('/trades', trade);
    return response.data;
  },
  
  getTrades: async (userId: string, filters: TradeFilters = {}): Promise<Trade[]> => {
    const params = new URLSearchParams();
    params.append('user_id', userId);
    if (filters.status) params.append('status', filters.status);
    if (filters.item_id) params.append('item_id', filters.item_id.toString());
    if (filters.start_date) params.append('start_date', filters.start_date);
    if (filters.end_date) params.append('end_date', filters.end_date);
    if (filters.limit) params.append('limit', filters.limit.toString());
    
    const response = await api.get<Trade[]>('/trades', { params });
    return response.data;
  },
  
  getStats: async (userId: string, days?: number): Promise<TradeStats> => {
    const params = new URLSearchParams();
    params.append('user_id', userId);
    if (days) params.append('days', days.toString());
    
    const response = await api.get<TradeStats>('/trades/stats', { params });
    return response.data;
  }
};

// Watchlist types
export interface WatchlistItem {
  id: number;
  user_id: string;
  item_id: number;
  item_name: string;
  alert_type: 'price_below' | 'price_above' | 'margin_above';
  threshold: number;
  is_active: boolean;
  created_at: string;
  last_triggered_at: string | null;
}

export interface WatchlistAlert {
  id: number;
  watchlist_item_id: number;
  triggered_at: string;
  current_value: number;
  threshold_value: number;
  message: string;
}

export interface WatchlistCreateRequest {
  user_id: string;
  item_id: number;
  alert_type: 'price_below' | 'price_above' | 'margin_above';
  threshold: number;
}

export const WatchlistApi = {
  addToWatchlist: async (watchlist: WatchlistCreateRequest): Promise<WatchlistItem> => {
    const response = await api.post<WatchlistItem>('/watchlist', watchlist);
    return response.data;
  },
  
  getWatchlist: async (userId: string, includeInactive: boolean = false): Promise<WatchlistItem[]> => {
    const params = new URLSearchParams();
    params.append('user_id', userId);
    if (includeInactive) params.append('include_inactive', 'true');
    
    const response = await api.get<WatchlistItem[]>('/watchlist', { params });
    return response.data;
  },
  
  removeFromWatchlist: async (watchlistItemId: number, userId: string): Promise<void> => {
    const params = new URLSearchParams();
    params.append('user_id', userId);
    
    await api.delete(`/watchlist/${watchlistItemId}`, { params });
  },
  
  getAlerts: async (userId: string, limit: number = 50): Promise<WatchlistAlert[]> => {
    const params = new URLSearchParams();
    params.append('user_id', userId);
    params.append('limit', limit.toString());
    
    const response = await api.get<WatchlistAlert[]>('/watchlist/alerts', { params });
    return response.data;
  }
};

// DPS Lab types
export interface LoadoutInput {
  name: string;
  loadout: Record<string, number | null>;
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

export const GearApi = {
  compareDPS: async (request: DPSComparisonRequest): Promise<DPSComparisonResponse> => {
    const response = await api.post<DPSComparisonResponse>('/gear/compare-dps', request);
    return response.data;
  }
};
