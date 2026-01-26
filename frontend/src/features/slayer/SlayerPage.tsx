import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Container, Title, Text, Stack } from '@mantine/core';
import { SlayerApi } from '../../lib/api';
import type { TaskAdvice } from '../../lib/api';
import { MasterSelector } from './components/MasterSelector';
import { TaskGrid } from './components/TaskGrid';
import { AdviceModal } from './components/AdviceModal';

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
        const result = await SlayerApi.getTasks(selectedMaster!);
        if (!Array.isArray(result)) {
          console.error('ERROR: Result is not an array!', result);
          return [];
        }
        return result;
      } catch (error: any) {
        console.error('API Error:', error);
        throw error;
      }
    },
    enabled: !!selectedMaster,
    staleTime: 0,
    gcTime: 0,
    refetchOnMount: true,
    refetchOnWindowFocus: true,
    retry: 1
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

  const handleMasterChange = (master: string) => {
    setSelectedMaster(null);
    setTimeout(() => {
      setSelectedMaster(master);
    }, 0);
  };

  const handleCloseAdvice = () => {
    setAdviceModalOpen(false);
    setSelectedTaskId(null);
  };

  const selectedTask = tasks?.find(t => t.task_id === selectedTaskId);
  const taskName = selectedTask?.monster_name || 'Unknown Task';

  return (
    <Container size="xl" py="xl">
      <Stack gap="lg">
        <div>
          <Title order={2} mb={4}>Slayer Task Helper</Title>
          <Text c="dimmed" size="sm">Choose your master and browse available tasks</Text>
        </div>
        
        <MasterSelector
          masters={masters}
          isLoading={mastersLoading}
          selectedMaster={selectedMaster}
          onMasterChange={handleMasterChange}
        />

        {selectedMaster && (
          <TaskGrid
            tasks={tasks}
            isLoading={tasksLoading}
            error={tasksError}
            selectedMaster={selectedMaster}
            onGetAdvice={handleGetAdvice}
          />
        )}
      </Stack>

      <AdviceModal
        opened={adviceModalOpen}
        onClose={handleCloseAdvice}
        advice={advice}
        isLoading={adviceLoading}
        taskName={taskName}
      />
    </Container>
  );
}
