import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_URL,
});

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log('🚀 API Request:', config.method?.toUpperCase(), config.url);
    console.log('   Full URL:', config.baseURL + config.url);
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

export interface TaskAdvice {
  task: string;
  master: string;
  recommendation: "DO" | "SKIP" | "BLOCK";
  reason: string;
  stats: {
    hp: number;
    def: number;
    xp: number;
  };
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
  
  getAdvice: async (taskId: number) => {
    const response = await api.get<TaskAdvice>(`/slayer/advice/${taskId}`);
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
