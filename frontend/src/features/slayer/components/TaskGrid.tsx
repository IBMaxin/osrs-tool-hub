import { 
  SimpleGrid, 
  Card, 
  Stack, 
  Skeleton, 
  Center, 
  Text,
  Group
} from '@mantine/core';
import { SlayerTask } from '../../../lib/api';
import { TaskCard } from '../TaskCard';

interface TaskGridProps {
  tasks: SlayerTask[] | undefined;
  isLoading: boolean;
  error: Error | null;
  selectedMaster: string | null;
  onGetAdvice: (taskId: number) => void;
}

export function TaskGrid({
  tasks,
  isLoading,
  error,
  selectedMaster,
  onGetAdvice
}: TaskGridProps) {
  if (error) {
    return (
      <Card p="md" withBorder radius="md" style={{ borderColor: 'var(--mantine-color-red-6)' }}>
        <Stack gap="sm">
          <Text fw={600} c="red">Error loading tasks</Text>
          <Text size="sm" c="dimmed">
            {error instanceof Error ? error.message : 'Failed to load tasks. Please try again.'}
          </Text>
          <Text size="xs" c="dimmed" style={{ fontFamily: 'monospace' }}>
            Selected master: {selectedMaster}
          </Text>
        </Stack>
      </Card>
    );
  }

  if (isLoading) {
    return (
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
    );
  }

  if (tasks !== undefined && tasks.length > 0) {
    return (
      <SimpleGrid cols={{ base: 1, sm: 2, lg: 3, xl: 4 }} spacing="md" style={{ justifyItems: 'center' }}>
        {tasks.map((task, index) => (
          <TaskCard
            key={task.task_id}
            task={task}
            onGetAdvice={onGetAdvice}
            index={index}
          />
        ))}
      </SimpleGrid>
    );
  }

  return (
    <Center p="xl">
      <Stack align="center" gap="md">
        <Text size="xl" c="dimmed">📜</Text>
        <div style={{ textAlign: 'center' }}>
          <Text fw={500} size="lg" mb={4}>No tasks found</Text>
          <Text c="dimmed" size="sm">
            No tasks available for {selectedMaster} at this time.
          </Text>
        </div>
      </Stack>
    </Center>
  );
}
