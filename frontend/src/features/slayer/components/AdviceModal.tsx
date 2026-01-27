import { 
  Modal, 
  Group, 
  Text, 
  ActionIcon, 
  Stack, 
  Badge, 
  Divider,
  Button,
  Loader,
  ScrollArea,
} from '@mantine/core';
import { IconX, IconCopy, IconCheck } from '@tabler/icons-react';
import { useQuery } from '@tanstack/react-query';
import type { TaskAdvice } from '../../../lib/api';
import { SlayerApi } from '../../../lib/api';
import { notifications } from '@mantine/notifications';
import { LocationSection } from './LocationSection';

interface AdviceModalProps {
  opened: boolean;
  onClose: () => void;
  advice: TaskAdvice | undefined;
  isLoading: boolean;
  taskName: string;
  taskId: number | null;
}

export function AdviceModal({
  opened,
  onClose,
  advice,
  isLoading,
  taskName,
  taskId,
}: AdviceModalProps) {
  // Fetch location data when modal opens
  const { data: locationData, isLoading: locationLoading } = useQuery({
    queryKey: ['slayer', 'location', taskId],
    queryFn: () => taskId ? SlayerApi.getLocation(taskId) : null,
    enabled: opened && taskId !== null,
  });

  const getRecommendationColor = (rec: string) => {
    switch (rec) {
      case 'DO': return 'osrsGreen';
      case 'SKIP': return 'osrsOrange';
      case 'BLOCK': return 'osrsRed';
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
          <Text fw={700} size="lg" c="osrsGold.4">Task Advice</Text>
          <ActionIcon
            variant="subtle"
            color="osrsGold"
            onClick={onClose}
          >
            <IconX size={18} />
          </ActionIcon>
        </Group>
      }
      size="xl"
      centered
      scrollAreaComponent={ScrollArea.Autosize}
      styles={{
        body: {
          maxHeight: '80vh',
        },
      }}
    >
      {isLoading ? (
        <Stack align="center" gap="md" py="xl">
          <Loader size="lg" color="osrsOrange" />
          <Text c="dimmed">Loading advice...</Text>
        </Stack>
      ) : advice ? (
        <Stack gap="md">
          {/* Task Header */}
          <Group justify="space-between">
            <Text fw={600} size="lg" c="osrsGold.4">{taskName}</Text>
            <Button
              size="xs"
              variant="subtle"
              color="osrsGold"
              leftSection={<IconCopy size={14} />}
              onClick={() => handleCopyTaskName(taskName)}
            >
              Copy Name
            </Button>
          </Group>
          
          <Divider color="osrsBrown.6" />
          
          {/* Recommendation */}
          <Group>
            <Text size="sm" c="dimmed" fw={600}>Recommendation:</Text>
            <Badge 
              size="lg" 
              color={getRecommendationColor(advice.recommendation)}
              variant="filled"
              style={{ textShadow: '1px 1px 2px rgba(0, 0, 0, 0.8)' }}
            >
              {advice.recommendation}
            </Badge>
          </Group>
          
          <Text size="sm" style={{ lineHeight: 1.6 }}>{advice.reason}</Text>
          
          <Divider color="osrsBrown.6" />
          
          {/* Monster Stats */}
          <Stack gap="xs">
            <Text fw={600} size="sm" c="osrsGold.4">Monster Stats:</Text>
            <Group gap="md">
              <Badge size="md" color="osrsRed" variant="light">
                HP: {advice.stats.hp}
              </Badge>
              <Badge size="md" color="osrsOrange" variant="light">
                Defence: {advice.stats.def}
              </Badge>
              <Badge size="md" color="osrsGreen" variant="light">
                XP: {advice.stats.xp}
              </Badge>
            </Group>
          </Stack>

          {/* Location Section */}
          {locationLoading ? (
            <>
              <Divider color="osrsBrown.6" />
              <Stack align="center" gap="xs" py="md">
                <Loader size="sm" color="osrsOrange" />
                <Text size="sm" c="dimmed">Loading location data...</Text>
              </Stack>
            </>
          ) : locationData ? (
            <>
              <Divider color="osrsBrown.6" />
              <LocationSection
                locations={locationData.locations}
                strategy={locationData.strategy}
                weaknesses={locationData.weakness}
                itemsNeeded={locationData.items_needed}
                alternatives={locationData.alternatives}
                hasDetailedData={locationData.has_detailed_data}
              />
            </>
          ) : null}
        </Stack>
      ) : (
        <Text c="dimmed">No advice available for this task.</Text>
      )}
    </Modal>
  );
}
