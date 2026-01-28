import type { SlayerTask } from '../../../lib/api/types';

const CATEGORY_KEYS: Record<string, string> = {
  dragons: 'dragon',
  demons: 'demon',
  undead: 'undead',
  kalphite: 'kalphite',
};

export function searchTasks(tasks: SlayerTask[], query: string): SlayerTask[] {
  const q = query.trim().toLowerCase();
  if (!q) return tasks;
  return tasks.filter(
    (t) =>
      t.monster_name.toLowerCase().includes(q) ||
      t.category.toLowerCase().includes(q)
  );
}

export function filterByCategory(
  tasks: SlayerTask[],
  categories: string[]
): SlayerTask[] {
  if (categories.length === 0) return tasks;
  return tasks.filter((t) => {
    const cat = t.category.toLowerCase();
    return categories.some(
      (key) => CATEGORY_KEYS[key] && cat.includes(CATEGORY_KEYS[key])
    );
  });
}

export function sortTasks(tasks: SlayerTask[], sortBy: string): SlayerTask[] {
  const arr = [...tasks];
  if (sortBy === 'combat_level') {
    arr.sort((a, b) => a.combat_level - b.combat_level);
  } else if (sortBy === 'slayer_xp') {
    arr.sort((a, b) => a.slayer_xp - b.slayer_xp);
  } else if (sortBy === 'name') {
    arr.sort((a, b) =>
      a.monster_name.localeCompare(b.monster_name, undefined, { sensitivity: 'base' })
    );
  }
  return arr;
}
