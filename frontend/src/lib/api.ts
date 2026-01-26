import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_URL,
});

export interface SlayerTask {
  task_id: number;
  monster_name: str;
  monster_id: number;
  category: str;
  amount: str;
  weight: number;
  combat_level: number;
  slayer_xp: number;
  is_skippable: boolean;
  is_blockable: boolean;
}

export interface TaskAdvice {
  task: str;
  master: str;
  recommendation: "DO" | "SKIP" | "BLOCK";
  reason: str;
  stats: {
    hp: number;
    def: number;
    xp: number;
  };
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
