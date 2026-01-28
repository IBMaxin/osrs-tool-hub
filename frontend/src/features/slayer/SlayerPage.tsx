import { useState } from 'react';
import { Container, Title, Text, Stack, Tabs } from '@mantine/core';
import { IconList, IconDatabase } from '@tabler/icons-react';
import { MasterSelector } from './components/MasterSelector';
import { TaskGrid } from './components/TaskGrid';
import { MonsterDatabase } from './components/MonsterDatabase';
import { AdviceModal } from './components/AdviceModal';
import { useSlayerMasters } from './hooks/useSlayerMasters';
import { useSlayerTasks } from './hooks/useSlayerTasks';
import { useSlayerAdvice } from './hooks/useSlayerAdvice';

export function SlayerPage() {
  const [activeTab, setActiveTab] = useState<string | null>('tasks');
  const [selectedMaster, setSelectedMaster] = useState<string | null>(null);
  const [adviceModalOpen, setAdviceModalOpen] = useState(false);
  const [selectedTaskId, setSelectedTaskId] = useState<number | null>(null);

  const { masters, isLoading: mastersLoading } = useSlayerMasters();
  const { tasks, isLoading: tasksLoading, error: tasksError } = useSlayerTasks({ selectedMaster });
  const { advice, isLoading: adviceLoading } = useSlayerAdvice({
    selectedTaskId,
    enabled: adviceModalOpen,
  });

  const handleGetAdvice = (taskId: number) => {
    setSelectedTaskId(taskId);
    setAdviceModalOpen(true);
  };

  const handleMasterChange = (master: string) => {
    setSelectedMaster(null);
    setTimeout(() => setSelectedMaster(master), 0);
  };

  const handleCloseAdvice = () => {
    setAdviceModalOpen(false);
    setSelectedTaskId(null);
  };

  const selectedTask = tasks?.find((t) => t.task_id === selectedTaskId);
  const taskName = advice?.task ?? selectedTask?.monster_name ?? 'Unknown Task';

  return (
    <Container size="xl" py="xl">
      <Stack gap="lg">
        <div>
          <Title order={2} mb={4}>Slayer Task Helper</Title>
          <Text c="dimmed" size="sm">Choose your master and browse available tasks</Text>
        </div>

        <Tabs value={activeTab} onChange={setActiveTab}>
          <Tabs.List>
            <Tabs.Tab value="tasks" leftSection={<IconList size={16} />}>
              Task Helper
            </Tabs.Tab>
            <Tabs.Tab value="database" leftSection={<IconDatabase size={16} />}>
              Monster Database
            </Tabs.Tab>
          </Tabs.List>

          <Tabs.Panel value="tasks" pt="md">
            <Stack gap="lg">
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
          </Tabs.Panel>

          <Tabs.Panel value="database" pt="md">
            <MonsterDatabase onGetAdvice={handleGetAdvice} />
          </Tabs.Panel>
        </Tabs>
      </Stack>

      <AdviceModal
        opened={adviceModalOpen}
        onClose={handleCloseAdvice}
        advice={advice}
        isLoading={adviceLoading}
        taskName={taskName}
        taskId={selectedTaskId}
      />
    </Container>
  );
}
