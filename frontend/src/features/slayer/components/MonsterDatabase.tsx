import {
  Card,
  Center,
  Checkbox,
  Group,
  SimpleGrid,
  Skeleton,
  Stack,
  Text,
  TextInput,
  Select,
} from '@mantine/core';
import { useMonsterSearch } from '../hooks/useMonsterSearch';
import { TaskCard } from '../TaskCard';

const CATEGORY_OPTIONS = [
  { value: 'dragons', label: 'Dragons' },
  { value: 'demons', label: 'Demons' },
  { value: 'undead', label: 'Undead' },
  { value: 'kalphite', label: 'Kalphite' },
] as const;

const SORT_OPTIONS = [
  { value: 'combat_level', label: 'Combat level' },
  { value: 'slayer_xp', label: 'Slayer XP' },
  { value: 'name', label: 'Name' },
];

interface MonsterDatabaseProps {
  onGetAdvice: (taskId: number) => void;
}

export function MonsterDatabase({ onGetAdvice }: MonsterDatabaseProps) {
  const {
    filteredTasks,
    isLoading,
    error,
    search,
    setSearch,
    sort,
    setSort,
    categories,
    setCategories,
  } = useMonsterSearch();

  if (error) {
    return (
      <Card p="md" withBorder radius="md" style={{ borderColor: 'var(--mantine-color-red-6)' }}>
        <Stack gap="sm">
          <Text fw={600} c="red">Error loading monster database</Text>
          <Text size="sm" c="dimmed">
            {error instanceof Error ? error.message : 'Failed to load. Please try again.'}
          </Text>
        </Stack>
      </Card>
    );
  }

  return (
    <Stack gap="lg">
      <TextInput
        placeholder="Search by name or category..."
        value={search}
        onChange={(e) => setSearch(e.currentTarget.value)}
        size="md"
      />
      <Group wrap="wrap" gap="lg">
        <Checkbox.Group value={categories} onChange={setCategories} label="Filter by category">
          <Group gap="md" mt="xs">
            {CATEGORY_OPTIONS.map(({ value, label }) => (
              <Checkbox key={value} value={value} label={label} />
            ))}
          </Group>
        </Checkbox.Group>
        <Select
          label="Sort by"
          data={SORT_OPTIONS}
          value={sort}
          onChange={(v) => v && setSort(v)}
          w={180}
        />
      </Group>

      {isLoading ? (
        <SimpleGrid cols={{ base: 1, sm: 2, lg: 3, xl: 4 }} spacing="md" style={{ justifyItems: 'center' }}>
          {Array.from({ length: 6 }).map((_, i) => (
            <Card key={i} w={280} p="md" withBorder radius="md">
              <Stack gap="md" align="center">
                <Skeleton height={96} width={96} circle />
                <Skeleton height={20} width="80%" />
                <Skeleton height={16} width="60%" />
                <Group justify="space-between" w="100%">
                  <Skeleton height={24} width={80} />
                  <Skeleton height={32} width={100} />
                </Group>
              </Stack>
            </Card>
          ))}
        </SimpleGrid>
      ) : filteredTasks.length > 0 ? (
        <SimpleGrid cols={{ base: 1, sm: 2, lg: 3, xl: 4 }} spacing="md" style={{ justifyItems: 'center' }}>
          {filteredTasks.map((task, index) => (
            <TaskCard
              key={task.task_id}
              task={task}
              onGetAdvice={onGetAdvice}
              index={index}
            />
          ))}
        </SimpleGrid>
      ) : (
        <Center p="xl">
          <Stack align="center" gap="md">
            <Text size="xl" c="dimmed">📜</Text>
            <div style={{ textAlign: 'center' }}>
              <Text fw={500} size="lg" mb={4}>No monsters match your filters</Text>
              <Text c="dimmed" size="sm">
                Try adjusting your search or category filters.
              </Text>
            </div>
          </Stack>
        </Center>
      )}
    </Stack>
  );
}
