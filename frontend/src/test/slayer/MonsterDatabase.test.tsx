/**
 * Tests for MonsterDatabase component
 * Covers search, category filters, sorting, and grid display
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { act, render, screen, waitFor } from '../utils/testUtils';
import userEvent from '@testing-library/user-event';
import { MonsterDatabase } from '../../features/slayer/components/MonsterDatabase';
import { SlayerApi } from '../../lib/api';
import type { SlayerTask } from '../../lib/api/types';

vi.mock('../../lib/api', () => ({
  SlayerApi: {
    getTasks: vi.fn(),
    getMasters: vi.fn(),
    getAdvice: vi.fn(),
    getLocation: vi.fn(),
  },
}));

const mockTasks: SlayerTask[] = [
  { task_id: 1, monster_name: 'Abyssal demon', monster_id: 1, category: 'Abyssal demons', amount: '120-185', weight: 12, combat_level: 124, slayer_xp: 150, is_skippable: true, is_blockable: true },
  { task_id: 2, monster_name: 'Black dragon', monster_id: 2, category: 'Black dragons', amount: '30-60', weight: 8, combat_level: 247, slayer_xp: 200, is_skippable: true, is_blockable: true },
  { task_id: 3, monster_name: 'Blue dragon', monster_id: 3, category: 'Blue dragons', amount: '110-170', weight: 6, combat_level: 111, slayer_xp: 150, is_skippable: true, is_blockable: true },
  { task_id: 4, monster_name: 'Ankou', monster_id: 4, category: 'Undead', amount: '80-120', weight: 5, combat_level: 75, slayer_xp: 80, is_skippable: true, is_blockable: true },
  { task_id: 5, monster_name: 'Kalphite worker', monster_id: 5, category: 'Kalphite', amount: '100-150', weight: 4, combat_level: 28, slayer_xp: 40, is_skippable: true, is_blockable: true },
  { task_id: 6, monster_name: 'Greater demon', monster_id: 6, category: 'Greater demons', amount: '150-200', weight: 10, combat_level: 92, slayer_xp: 87, is_skippable: true, is_blockable: true },
  { task_id: 7, monster_name: 'Bronze dragon', monster_id: 7, category: 'Bronze dragons', amount: '30-60', weight: 7, combat_level: 131, slayer_xp: 105, is_skippable: true, is_blockable: true },
  { task_id: 8, monster_name: 'Dust devil', monster_id: 8, category: 'Dust devils', amount: '130-170', weight: 9, combat_level: 93, slayer_xp: 105, is_skippable: true, is_blockable: true },
  { task_id: 9, monster_name: 'Ghost', monster_id: 9, category: 'Undead', amount: '50-80', weight: 3, combat_level: 40, slayer_xp: 45, is_skippable: true, is_blockable: true },
  { task_id: 10, monster_name: 'Gargoyle', monster_id: 10, category: 'Gargoyles', amount: '120-170', weight: 11, combat_level: 111, slayer_xp: 105, is_skippable: true, is_blockable: true },
];

function renderMonsterDatabase() {
  const onGetAdvice = vi.fn();
  render(<MonsterDatabase onGetAdvice={onGetAdvice} />);
  return { onGetAdvice };
}

describe('MonsterDatabase', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(SlayerApi.getTasks).mockImplementation(async (master: string) => {
      if (master === 'Duradel') return mockTasks;
      return [];
    });
  });

  it('renders search bar, category checkboxes, sort dropdown, and grid after load', async () => {
    renderMonsterDatabase();

    expect(screen.getByPlaceholderText(/search by name or category/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/filter by category/i)).toBeInTheDocument();
    expect(screen.getByRole('textbox', { name: /sort by/i })).toBeInTheDocument();

    await waitFor(() => {
      expect(SlayerApi.getTasks).toHaveBeenCalledWith('Duradel');
    });

    await waitFor(() => {
      expect(screen.getByText('Abyssal demon')).toBeInTheDocument();
      expect(screen.getByText('Black dragon')).toBeInTheDocument();
      expect(screen.getByText('Gargoyle')).toBeInTheDocument();
    });
  });

  it('filters tasks by search query', async () => {
    const user = userEvent.setup();
    renderMonsterDatabase();

    await waitFor(() => {
      expect(screen.getByText('Abyssal demon')).toBeInTheDocument();
    });

    const search = screen.getByPlaceholderText(/search by name or category/i);
    await user.type(search, 'dragon');

    await waitFor(() => {
      expect(screen.getByText('Black dragon')).toBeInTheDocument();
      expect(screen.getByText('Blue dragon')).toBeInTheDocument();
      expect(screen.getByText('Bronze dragon')).toBeInTheDocument();
      expect(screen.queryByText('Abyssal demon')).not.toBeInTheDocument();
      expect(screen.queryByText('Gargoyle')).not.toBeInTheDocument();
    });
  });

  it('filters tasks by category checkbox', async () => {
    const user = userEvent.setup();
    renderMonsterDatabase();

    await waitFor(() => {
      expect(screen.getByText('Abyssal demon')).toBeInTheDocument();
    });

    const dragonsCheckbox = screen.getByLabelText('Dragons');
    await user.click(dragonsCheckbox);

    await waitFor(() => {
      expect(screen.getByText('Black dragon')).toBeInTheDocument();
      expect(screen.getByText('Blue dragon')).toBeInTheDocument();
      expect(screen.getByText('Bronze dragon')).toBeInTheDocument();
      expect(screen.queryByText('Abyssal demon')).not.toBeInTheDocument();
      expect(screen.queryByText('Gargoyle')).not.toBeInTheDocument();
    });
  });

  describe('sorting', () => {
    beforeEach(() => {
      vi.useFakeTimers({ shouldAdvanceTime: true });
    });

    afterEach(() => {
      vi.runOnlyPendingTimers();
      vi.useRealTimers();
    });

    it('sorts tasks by combat level', async () => {
      const user = userEvent.setup();
      renderMonsterDatabase();

      await waitFor(() => {
        expect(screen.getByText('Abyssal demon')).toBeInTheDocument();
      });

      const sortSelect = screen.getByRole('textbox', { name: /sort by/i });
      await user.click(sortSelect);
      const combatOption = await screen.findByRole('option', { name: /^combat level$/i });
      await user.click(combatOption);

      await act(async () => {
        vi.runAllTimers();
      });

      const sortedByCombat = [...mockTasks].sort((a, b) => a.combat_level - b.combat_level);
      expect(screen.getByText(sortedByCombat[0].monster_name)).toBeInTheDocument();
      expect(screen.getByText(sortedByCombat[sortedByCombat.length - 1].monster_name)).toBeInTheDocument();
    });

    it('sorts tasks by name', async () => {
      const user = userEvent.setup();
      renderMonsterDatabase();

      await waitFor(() => {
        expect(screen.getByText('Abyssal demon')).toBeInTheDocument();
      });

      const sortSelect = screen.getByRole('textbox', { name: /sort by/i });
      await user.click(sortSelect);
      const nameOption = await screen.findByRole('option', { name: /^name$/i });
      await user.click(nameOption);

      await act(async () => {
        vi.runAllTimers();
      });

      const sortedByName = [...mockTasks].sort((a, b) =>
        a.monster_name.localeCompare(b.monster_name, undefined, { sensitivity: 'base' })
      );
      expect(screen.getByText(sortedByName[0].monster_name)).toBeInTheDocument();
      expect(screen.getByText(sortedByName[sortedByName.length - 1].monster_name)).toBeInTheDocument();
    });
  });

  it('shows empty state when no tasks match filters', async () => {
    const user = userEvent.setup();
    renderMonsterDatabase();

    await waitFor(() => {
      expect(screen.getByText('Abyssal demon')).toBeInTheDocument();
    });

    const search = screen.getByPlaceholderText(/search by name or category/i);
    await user.type(search, 'xyznonexistent');

    await waitFor(() => {
      expect(screen.getByText(/no monsters match your filters/i)).toBeInTheDocument();
    });
  });

  it('calls onGetAdvice when Get Advice is clicked', async () => {
    const { onGetAdvice } = renderMonsterDatabase();

    await waitFor(() => {
      expect(screen.getByText('Abyssal demon')).toBeInTheDocument();
    });

    const adviceButtons = screen.getAllByRole('button', { name: /get advice/i });
    await userEvent.setup().click(adviceButtons[0]);

    const sortedByCombat = [...mockTasks].sort((a, b) => a.combat_level - b.combat_level);
    expect(onGetAdvice).toHaveBeenCalledWith(sortedByCombat[0].task_id);
  });
});
