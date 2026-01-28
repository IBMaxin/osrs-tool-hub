import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { GearApi, type SlayerGearResponse } from '../../../../lib/api/gear';

const DEFAULT_STATS = {
  attack: 70,
  strength: 70,
  defence: 70,
  ranged: 70,
  magic: 70,
  prayer: 43,
};

interface UseSlayerGearSuggestionsOptions {
  taskId: number | null;
  enabled: boolean;
}

export function useSlayerGearSuggestions({ taskId, enabled }: UseSlayerGearSuggestionsOptions) {
  const [stats, setStats] = useState(DEFAULT_STATS);
  const [budget, setBudget] = useState(100_000_000);
  const [ironman, setIronman] = useState(false);
  const [combatStyle, setCombatStyle] = useState<'melee' | 'ranged' | 'magic' | null>(null);
  const [shouldFetch, setShouldFetch] = useState(false);

  const { data: gearData, isLoading, error } = useQuery<SlayerGearResponse>({
    queryKey: ['slayer', 'gear', taskId, stats, budget, ironman, combatStyle],
    queryFn: async () => {
      if (!taskId) {
        throw new Error('Task ID is required');
      }
      return GearApi.getSlayerGear({
        task_id: taskId,
        stats,
        budget,
        combat_style: combatStyle || undefined,
        ironman,
      });
    },
    enabled: enabled && shouldFetch && taskId !== null,
  });

  const handleGetSuggestions = () => {
    setShouldFetch(true);
  };

  return {
    stats,
    setStats,
    budget,
    setBudget,
    ironman,
    setIronman,
    combatStyle,
    setCombatStyle,
    gearData,
    isLoading,
    error,
    handleGetSuggestions,
  };
}
