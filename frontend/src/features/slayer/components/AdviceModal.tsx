import { 
  Modal, 
  Group, 
  Text, 
  ActionIcon, 
  Stack, 
  Badge, 
  Divider,
  Button,
  Loader
} from '@mantine/core';
import { IconX, IconCopy, IconCheck } from '@tabler/icons-react';
import type { TaskAdvice } from '../../../lib/api';
import { notifications } from '@mantine/notifications';

interface AdviceModalProps {
  opened: boolean;
  onClose: () => void;
  advice: TaskAdvice | undefined;
  isLoading: boolean;
  taskName: string;
}

export function AdviceModal({
  opened,
  onClose,
  advice,
  isLoading,
  taskName
}: AdviceModalProps) {
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

  return (
    <Modal 
      opened={opened} 
      onClose={onClose}
      title={
        <Group justify="space-between" w="100%">
          <Text fw={700} size="lg">Task Advice</Text>
          <ActionIcon
            variant="subtle"
            color="gray"
            onClick={onClose}
          >
            <IconX size={18} />
          </ActionIcon>
        </Group>
      }
      size="lg"
      centered
    >
      {isLoading ? (
        <Stack align="center" gap="md" py="xl">
          <Loader size="lg" />
          <Text c="dimmed">Loading advice...</Text>
        </Stack>
      ) : advice ? (
        <Stack gap="md">
          <Group justify="space-between">
            <Text fw={600} size="lg">{taskName}</Text>
            <Button
              size="xs"
              variant="subtle"
              leftSection={<IconCopy size={14} />}
              onClick={() => handleCopyTaskName(taskName)}
            >
              Copy Name
            </Button>
          </Group>
          
          <Divider />
          
          <Group>
            <Text size="sm" c="dimmed">Recommendation:</Text>
            <Badge 
              size="lg" 
              color={getRecommendationColor(advice.recommendation)}
              variant="light"
            >
              {advice.recommendation}
            </Badge>
          </Group>
          
          <Text size="sm">{advice.reason}</Text>
          
          <Divider />
          <Stack gap="xs">
            <Text fw={600} size="sm">Monster Stats:</Text>
            <Group gap="md">
              <Text size="sm">HP: {advice.stats.hp}</Text>
              <Text size="sm">Defence: {advice.stats.def}</Text>
              <Text size="sm">XP: {advice.stats.xp}</Text>
            </Group>
          </Stack>
        </Stack>
      ) : (
        <Text c="dimmed">No advice available for this task.</Text>
      )}
    </Modal>
  );
}
