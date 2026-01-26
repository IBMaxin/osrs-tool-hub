import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { 
  Container, 
  Title, 
  SegmentedControl,
  SimpleGrid,
  Group, 
  Modal, 
  Text, 
  Badge, 
  Stack,
  Skeleton,
  Center,
  Button,
  Card,
  Divider,
  ActionIcon,
  Tooltip
} from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { IconCopy, IconX, IconCheck } from '@tabler/icons-react';
import { SlayerApi, SlayerTask, TaskAdvice } from '../../lib/api';
import { TaskCard } from './TaskCard';

export function SlayerPage() {
  const [selectedMaster, setSelectedMaster] = useState<string | null>(null);
  const [adviceModalOpen, setAdviceModalOpen] = useState(false);
  const [selectedTaskId, setSelectedTaskId] = useState<number | null>(null);

  // 1. Fetch Masters
  const { data: masters, isLoading: mastersLoading } = useQuery({
    queryKey: ['slayerMasters'],
    queryFn: SlayerApi.getMasters
  });

  // 2. Fetch Tasks (conditional)
  const { data: tasks, isLoading: tasksLoading, error: tasksError } = useQuery({
    queryKey: ['slayerTasks', selectedMaster],
    queryFn: async () => {
      try {
        console.log('Fetching tasks for master:', selectedMaster);
        const result = await SlayerApi.getTasks(selectedMaster!);
        console.log('Tasks fetched:', result, 'Count:', result?.length);
        return result;
      } catch (error) {
        console.error('Error fetching tasks:', error);
        throw error;
      }
    },
    enabled: !!selectedMaster,
    staleTime: 0, // Always refetch to avoid cache issues
    gcTime: 0 // React Query v5 uses gcTime instead of cacheTime
  });

  // 3. Fetch Advice (conditional)
  const { data: advice, isLoading: adviceLoading } = useQuery({
    queryKey: ['taskAdvice', selectedTaskId],
    queryFn: () => SlayerApi.getAdvice(selectedTaskId!),
    enabled: !!selectedTaskId && adviceModalOpen
  });

  const handleGetAdvice = (taskId: number) => {
    setSelectedTaskId(taskId);
    setAdviceModalOpen(true);
  };

  const getRecommendationColor = (rec: string) => {
    switch (rec) {
      case 'DO': return 'green';
      case 'SKIP': return 'yellow';
      case 'BLOCK': return 'red';
      default: return 'gray';
    }
  };

  const handleCopyTaskName = (taskName: string) => {
    navigator.clipboard.writeText(taskName);
    notifications.show({
      title: 'Copied!',
      message: `Task name "${taskName}" copied to clipboard`,
      color: 'green',
      icon: <IconCheck size={16} />,
      autoClose: 2000,
    });
  };

  // Calculate XP/hour estimate (simplified - would need actual data)
  const getXpPerHour = (advice: TaskAdvice | undefined): string | null => {
    if (!advice) return null;
    // Simplified calculation - in real app, this would use actual kill rates
    const estimatedKillsPerHour = 200; // Placeholder
    const xpPerKill = advice.stats.xp;
    const totalXp = estimatedKillsPerHour * xpPerKill;
    return `${totalXp.toLocaleString()} XP/hr`;
  };

  return (
    <Container size="xl" py="xl">
      <Stack gap="lg">
        <div>
          <Title order={2} mb={4}>Slayer Task Helper</Title>
          <Text c="dimmed" size="sm">Choose your master and browse available tasks</Text>
        </div>
        
        {/* Master Selection */}
        {mastersLoading ? (
          <Skeleton height={42} />
        ) : masters && masters.length > 0 ? (
          <SegmentedControl
            value={selectedMaster || ''}
            onChange={(value) => {
              console.log('Master selected:', value);
              setSelectedMaster(value);
            }}
            data={masters.map(master => ({ value: master, label: master }))}
            fullWidth
            size="md"
          />
        ) : null}

        {/* Task Grid */}
        {selectedMaster && (
          <>
            {tasksError ? (
              <Card p="md" withBorder radius="md" style={{ borderColor: 'var(--mantine-color-red-6)' }}>
                <Stack gap="sm">
                  <Text fw={600} c="red">Error loading tasks</Text>
                  <Text size="sm" c="dimmed">
                    {tasksError instanceof Error ? tasksError.message : 'Failed to load tasks. Please try again.'}
                  </Text>
                  <Text size="xs" c="dimmed" style={{ fontFamily: 'monospace' }}>
                    Selected master: {selectedMaster}
                  </Text>
                </Stack>
              </Card>
            ) : tasksLoading ? (
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
            ) : tasks !== undefined && tasks.length > 0 ? (
              <SimpleGrid cols={{ base: 1, sm: 2, lg: 3, xl: 4 }} spacing="md" style={{ justifyItems: 'center' }}>
                {tasks.map((task, index) => (
                  <TaskCard
                    key={task.task_id}
                    task={task}
                    onGetAdvice={handleGetAdvice}
                    index={index}
                  />
                ))}
              </SimpleGrid>
            ) : (
              <Center p="xl">
                <Stack align="center" gap="md">
                  <Text size="xl" c="dimmed">📜</Text>
                  <div style={{ textAlign: 'center' }}>
                    <Text fw={500} size="lg" mb={4}>No tasks found</Text>
                    <Text c="dimmed" size="sm">
                      No tasks available for {selectedMaster} at this time.
                    </Text>
                    {tasksError && (
                      <Card p="sm" mt="md" withBorder style={{ borderColor: 'var(--mantine-color-red-6)' }}>
                        <Text size="xs" c="red" fw={600}>API Error:</Text>
                        <Text size="xs" c="dimmed">
                          {tasksError instanceof Error ? tasksError.message : String(tasksError)}
                        </Text>
                      </Card>
                    )}
                    {tasks !== undefined && tasks.length === 0 && !tasksError && (
                      <Text size="xs" c="dimmed" mt="xs">
                        The API returned an empty array. Check browser console for details.
                        <br />
                        Debug: tasks={JSON.stringify(tasks)}, loading={String(tasksLoading)}, error={String(tasksError)}
                      </Text>
                    )}
                    {tasks === undefined && !tasksLoading && !tasksError && (
                      <Text size="xs" c="dimmed" mt="xs">
                        Tasks data is undefined. Check the browser console for API errors.
                      </Text>
                    )}
                  </div>
                </Stack>
              </Center>
            )}
          </>
        )}
      </Stack>

      <Modal 
        opened={adviceModalOpen} 
        onClose={() => {
          setAdviceModalOpen(false);
          setSelectedTaskId(null);
        }}
        title={
          <Group justify="space-between" w="100%">
            <Text fw={700} size="lg">Task Advice</Text>
            <ActionIcon
              variant="subtle"
              color="gray"
              onClick={() => {
                setAdviceModalOpen(false);
                setSelectedTaskId(null);
              }}
            >
              <IconX size={18} />
            </ActionIcon>
          </Group>
        }
        size="md"
        radius="md"
        styles={{
          content: {
            background: 'linear-gradient(135deg, var(--mantine-color-dark-7) 0%, var(--mantine-color-dark-8) 100%)',
            border: '2px solid var(--mantine-color-yellow-6)',
          },
          header: {
            background: 'transparent',
            borderBottom: '1px solid var(--mantine-color-yellow-6)',
          },
          body: {
            padding: 'var(--mantine-spacing-lg)',
          }
        }}
      >
        {adviceLoading ? (
          <Stack gap="md">
            <Skeleton height={40} />
            <Skeleton height={100} />
            <Skeleton height={60} />
          </Stack>
        ) : advice ? (
          <Stack gap="md">
            {/* Task Name with Copy Button */}
            <Group justify="space-between" wrap="nowrap">
              <Text size="xl" fw={700} c="white" style={{ flex: 1 }}>
                {advice.task}
              </Text>
              <Tooltip label="Copy task name for OSRS chat">
                <ActionIcon
                  variant="light"
                  color="yellow"
                  onClick={() => handleCopyTaskName(advice.task)}
                >
                  <IconCopy size={18} />
                </ActionIcon>
              </Tooltip>
            </Group>

            {/* Recommendation Badge */}
            <Group>
              <Badge 
                size="xl" 
                color={getRecommendationColor(advice.recommendation)}
                variant="filled"
                style={{ 
                  fontSize: '16px',
                  padding: '8px 16px',
                  fontWeight: 700
                }}
              >
                {advice.recommendation}
              </Badge>
              {getXpPerHour(advice) && (
                <Badge size="lg" variant="light" color="blue">
                  {getXpPerHour(advice)}
                </Badge>
              )}
            </Group>

            <Divider color="yellow.6" />

            {/* Master Info */}
            <Text c="dimmed" size="sm">
              <Text span fw={600} c="yellow.4">Master:</Text> {advice.master}
            </Text>
            
            {/* Reasoning */}
            <Card p="md" bg="dark.6" withBorder radius="sm" style={{ borderColor: 'var(--mantine-color-yellow-6)' }}>
              <Text fw={600} c="yellow.4" mb="xs">Reasoning:</Text>
              <Text c="gray.3" size="sm" style={{ lineHeight: 1.6 }}>
                {advice.reason}
              </Text>
            </Card>

            {/* Stats */}
            <Group gap="xs" mt="xs">
              <Badge variant="filled" color="red" size="lg">
                HP: {advice.stats.hp}
              </Badge>
              <Badge variant="filled" color="blue" size="lg">
                Def: {advice.stats.def}
              </Badge>
              <Badge variant="filled" color="green" size="lg">
                XP: {advice.stats.xp}
              </Badge>
            </Group>
          </Stack>
        ) : null}
      </Modal>
    </Container>
  );
}
