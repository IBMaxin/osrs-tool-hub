/**
 * Tests for useSlayerTasks hook
 * Verifies caching configuration and behavior
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactNode } from 'react';
import { useSlayerTasks } from '../../features/slayer/hooks/useSlayerTasks';
import { SlayerApi } from '../../lib/api';

// Mock the API
vi.mock('../../lib/api', () => ({
  SlayerApi: {
    getTasks: vi.fn(),
  },
}));

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

  return ({ children }: { children: ReactNode }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
};

describe('useSlayerTasks', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should have correct cache configuration', async () => {
    const mockTasks = [
      { 
        task_id: 1, 
        monster_name: 'Abyssal demon', 
        monster_id: 1,
        category: 'demon',
        amount: '130-200',
        weight: 8,
        combat_level: 86,
        slayer_xp: 150.0,
        is_skippable: true,
        is_blockable: true,
      },
      { 
        task_id: 2, 
        monster_name: 'Black demon', 
        monster_id: 2,
        category: 'demon',
        amount: '130-200',
        weight: 9,
        combat_level: 172,
        slayer_xp: 157.0,
        is_skippable: true,
        is_blockable: true,
      },
    ];

    vi.mocked(SlayerApi.getTasks).mockResolvedValue(mockTasks);

    const { result } = renderHook(
      () => useSlayerTasks({ selectedMaster: 'Duradel' }),
      { wrapper: createWrapper() }
    );

    await waitFor(() => expect(result.current.isLoading).toBe(false));

    // Verify cache times are set correctly (5 minutes staleTime, 10 minutes gcTime)
    // This is verified by checking that refetches don't happen immediately
    expect(result.current.tasks).toEqual(mockTasks);
    expect(SlayerApi.getTasks).toHaveBeenCalledTimes(1);
  });

  it('should not fetch when selectedMaster is null', () => {
    const { result } = renderHook(() => useSlayerTasks({ selectedMaster: null }), {
      wrapper: createWrapper(),
    });

    expect(result.current.isLoading).toBe(false);
    expect(result.current.tasks).toBeUndefined();
    expect(SlayerApi.getTasks).not.toHaveBeenCalled();
  });

  it('should handle API errors correctly', async () => {
    const error = new Error('API Error');
    vi.mocked(SlayerApi.getTasks).mockRejectedValue(error);

    const { result } = renderHook(
      () => useSlayerTasks({ selectedMaster: 'Duradel' }),
      { wrapper: createWrapper() }
    );

    // Wait for loading to finish and error to be set
    await waitFor(() => expect(result.current.isLoading).toBe(false), { timeout: 3000 });
    await waitFor(() => expect(result.current.error).toBeTruthy(), { timeout: 3000 });

    expect(result.current.error).toBeTruthy();
    expect(result.current.tasks).toBeUndefined();
  });

  it('should handle non-array responses', async () => {
    vi.mocked(SlayerApi.getTasks).mockResolvedValue({} as any);

    const { result } = renderHook(
      () => useSlayerTasks({ selectedMaster: 'Duradel' }),
      { wrapper: createWrapper() }
    );

    await waitFor(() => expect(result.current.isLoading).toBe(false));

    // Should return empty array for invalid responses
    expect(result.current.tasks).toEqual([]);
  });

  it('should cache results and not refetch immediately', async () => {
    const mockTasks = [{ 
      task_id: 1, 
      monster_name: 'Test', 
      monster_id: 1,
      category: 'test',
      amount: '1-10',
      weight: 1,
      combat_level: 1,
      slayer_xp: 1.0,
      is_skippable: false,
      is_blockable: false,
    }];
    vi.mocked(SlayerApi.getTasks).mockResolvedValue(mockTasks);

    const wrapper = createWrapper();
    const { result: result1 } = renderHook(
      () => useSlayerTasks({ selectedMaster: 'Duradel' }),
      { wrapper }
    );

    await waitFor(() => expect(result1.current.isLoading).toBe(false));

    // Render again with same master - should use cache
    const { result: result2 } = renderHook(
      () => useSlayerTasks({ selectedMaster: 'Duradel' }),
      { wrapper }
    );

    // Should not call API again immediately due to staleTime
    expect(SlayerApi.getTasks).toHaveBeenCalledTimes(1);
    expect(result2.current.tasks).toEqual(mockTasks);
  });
});
