import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_URL,
});

// Slayer Types
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

// Flipping Types
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

export const SlayerApi = {
  getMasters: async () => {
    const response = await api.get<string[]>('/slayer/masters');
    return response.data;
  },
  
  getTasks: async (master: string) => {
    const response = await api.get<SlayerTask[]>(`/slayer/tasks/${master}`);
    return response.data;
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
