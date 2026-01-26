import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { 
  Container, 
  Title, 
  Select, 
  Table, 
  Button, 
  Paper, 
  Group, 
  Modal, 
  Text, 
  Badge, 
  Stack,
  Loader,
  Center
} from '@mantine/core';
import { SlayerApi, SlayerTask, TaskAdvice } from '../../lib/api';

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
  const { data: tasks, isLoading: tasksLoading } = useQuery({
    queryKey: ['slayerTasks', selectedMaster],
    queryFn: () => SlayerApi.getTasks(selectedMaster!),
    enabled: !!selectedMaster
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

  return (
    <Container size="lg" py="xl">
      <Stack gap="lg">
        <Title order={2}>Slayer Task Helper</Title>
        
        <Paper p="md" withBorder>
          <Select
            label="Select Slayer Master"
            placeholder="Choose a master..."
            data={masters || []}
            value={selectedMaster}
            onChange={setSelectedMaster}
            disabled={mastersLoading}
            searchable
          />
        </Paper>

        {selectedMaster && (
          <Paper p="md" withBorder>
            <Title order={3} mb="md">Task List ({selectedMaster})</Title>
            
            {tasksLoading ? (
              <Center p="xl"><Loader /></Center>
            ) : (
              <Table striped highlightOnHover>
                <Table.Thead>
                  <Table.Tr>
                    <Table.Th>Monster</Table.Th>
                    <Table.Th>Category</Table.Th>
                    <Table.Th>Amount</Table.Th>
                    <Table.Th>Weight</Table.Th>
                    <Table.Th>Action</Table.Th>
                  </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                  {tasks?.map((task) => (
                    <Table.Tr key={task.task_id}>
                      <Table.Td style={{ fontWeight: 500 }}>{task.monster_name}</Table.Td>
                      <Table.Td>{task.category}</Table.Td>
                      <Table.Td>{task.amount}</Table.Td>
                      <Table.Td>{task.weight}</Table.Td>
                      <Table.Td>
                        <Button 
                          size="xs" 
                          variant="light"
                          onClick={() => handleGetAdvice(task.task_id)}
                        >
                          Get Advice
                        </Button>
                      </Table.Td>
                    </Table.Tr>
                  ))}
                </Table.Tbody>
              </Table>
            )}
          </Paper>
        )}
      </Stack>

      <Modal 
        opened={adviceModalOpen} 
        onClose={() => setAdviceModalOpen(false)}
        title="Task Advice"
      >
        {adviceLoading ? (
          <Center p="lg"><Loader /></Center>
        ) : advice ? (
          <Stack>
            <Group justify="space-between">
              <Text size="lg" fw={700}>{advice.task}</Text>
              <Badge 
                size="lg" 
                color={getRecommendationColor(advice.recommendation)}
              >
                {advice.recommendation}
              </Badge>
            </Group>
            
            <Text c="dimmed">Master: {advice.master}</Text>
            
            <Paper p="sm" bg="gray.1">
              <Text fw={500}>Reasoning:</Text>
              <Text>{advice.reason}</Text>
            </Paper>

            <Group gap="xs">
              <Badge variant="outline">HP: {advice.stats.hp}</Badge>
              <Badge variant="outline">Def: {advice.stats.def}</Badge>
              <Badge variant="outline">XP: {advice.stats.xp}</Badge>
            </Group>
          </Stack>
        ) : null}
      </Modal>
    </Container>
  );
}
