import { useMemo, useState } from 'react';
import { useDebouncedValue } from '@mantine/hooks';
import { useSlayerTasks } from './useSlayerTasks';
import {
  searchTasks,
  filterByCategory,
  sortTasks,
} from '../utils/slayerFilters';

const MONSTER_DB_MASTER = 'Duradel';

export function useMonsterSearch() {
  const { tasks, isLoading, error } = useSlayerTasks({
    selectedMaster: MONSTER_DB_MASTER,
  });
  const [search, setSearch] = useState('');
  const [sort, setSort] = useState<string>('combat_level');
  const [categories, setCategories] = useState<string[]>([]);
  const [debouncedSearch] = useDebouncedValue(search, 300);

  const filteredTasks = useMemo(() => {
    let result = tasks ?? [];
    result = searchTasks(result, debouncedSearch);
    result = filterByCategory(result, categories);
    result = sortTasks(result, sort);
    return result;
  }, [tasks, debouncedSearch, categories, sort]);

  return {
    filteredTasks,
    isLoading,
    error,
    search,
    setSearch,
    sort,
    setSort,
    categories,
    setCategories,
  };
}
