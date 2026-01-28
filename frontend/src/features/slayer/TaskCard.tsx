import { useEffect, useRef, useState } from 'react';
import { Card, Group, Text, Badge, Button, Stack, Avatar, Box, Image } from '@mantine/core';
import { IconSword } from '@tabler/icons-react';
import { SlayerTask } from '../../lib/api';
import { getMonsterIconUrl, getCategoryColor } from './utils/monsterImages';

interface TaskCardProps {
  task: SlayerTask;
  onGetAdvice: (taskId: number) => void;
  index?: number;
}

export function TaskCard({ task, onGetAdvice, index = 0 }: TaskCardProps) {
  const categoryColor = getCategoryColor(task.category);
  const hasHighWeight = task.weight > 10;
  const cardRef = useRef<HTMLDivElement>(null);
  const [imageError, setImageError] = useState(false);
  const [imageUrl, setImageUrl] = useState(getMonsterIconUrl(task.monster_name));
  
  useEffect(() => {
    if (cardRef.current) {
      const delay = index * 50;
      setTimeout(() => {
        if (cardRef.current) {
          cardRef.current.style.opacity = '1';
          cardRef.current.style.transform = 'translateY(0)';
        }
      }, delay);
    }
  }, [index]);
  
  return (
    <Card
      ref={cardRef}
      w={280}
      p="lg"
      withBorder
      radius="md"
      style={{
        borderLeftWidth: 4,
        borderLeftColor: `var(--mantine-color-${categoryColor}-6)`,
        transition: 'transform 0.2s ease, box-shadow 0.2s ease, opacity 0.5s ease, border-color 0.2s ease',
        opacity: 0,
        transform: 'translateY(10px)',
        cursor: 'pointer',
        backgroundColor: 'var(--mantine-color-dark-7)',
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = 'translateY(-4px)';
        e.currentTarget.style.boxShadow = 'var(--mantine-shadow-md)';
        e.currentTarget.style.borderLeftColor = `var(--mantine-color-${categoryColor}-7)`;
        e.currentTarget.style.backgroundColor = 'var(--mantine-color-dark-6)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = 'translateY(0)';
        e.currentTarget.style.boxShadow = 'var(--mantine-shadow-sm)';
        e.currentTarget.style.borderLeftColor = `var(--mantine-color-${categoryColor}-6)`;
        e.currentTarget.style.backgroundColor = 'var(--mantine-color-dark-7)';
      }}
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onGetAdvice(task.task_id);
        }
      }}
    >
      <Stack gap="lg" align="center">
        {/* Top Section: Monster Icon with Combat Level Badge */}
        <Box pos="relative" mb={4}>
          {!imageError ? (
            <Image
              src={imageUrl}
              alt={task.monster_name}
              w={96}
              h={96}
              fit="contain"
              radius="md"
              style={{ 
                border: '2px solid var(--mantine-color-gray-4)',
                backgroundColor: 'var(--mantine-color-dark-8)'
              }}
              onError={() => {
                // Try base version if detail fails
                if (imageUrl.includes('_detail')) {
                  const baseUrl = imageUrl.replace('_detail.png', '.png');
                  setImageUrl(baseUrl);
                  // Reset error state to try again
                  setImageError(false);
                } else {
                  // Both failed, show fallback
                  setImageError(true);
                }
              }}
            />
          ) : (
            <Avatar
              size={96}
              radius="md"
              bg="dark.8"
              style={{ border: '2px solid var(--mantine-color-gray-4)' }}
            >
              <IconSword size={48} />
            </Avatar>
          )}
          <Badge
            size="sm"
            color="dark"
            variant="filled"
            pos="absolute"
            bottom={-8}
            left="50%"
            style={{ transform: 'translateX(-50%)', fontWeight: 600 }}
          >
            Lvl {task.combat_level}
          </Badge>
        </Box>

        {/* Middle Section: Monster Name and Amount */}
        <Stack gap={6} align="center" style={{ flex: 1, width: '100%' }}>
          <Text fw={700} size="lg" ta="center" lineClamp={2} c="gray.0" lh={1.3}>
            {task.monster_name}
          </Text>
          <Text size="sm" c="dimmed" ta="center" fw={500}>
            {task.amount} {task.category}
          </Text>
        </Stack>

        {/* Bottom Row: Weight Badge and Get Advice Button */}
        <Group justify="space-between" w="100%" mt="md">
          <Badge
            size="sm"
            color={hasHighWeight ? 'blue' : 'gray'}
            variant="light"
            style={{ fontWeight: 600 }}
          >
            Weight: {task.weight}
          </Badge>
          <Button
            size="sm"
            variant="filled"
            color="yellow"
            onClick={() => onGetAdvice(task.task_id)}
            style={{ fontWeight: 600 }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'scale(1.05)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'scale(1)';
            }}
          >
            Get Advice
          </Button>
        </Group>

        {/* Block/Skip Indicators */}
        {(task.is_blockable || task.is_skippable) && (
          <Group gap="xs" mt={-4}>
            {task.is_blockable && (
              <Badge size="xs" color="red" variant="dot" style={{ fontWeight: 600 }}>
                BLOCK
              </Badge>
            )}
            {task.is_skippable && (
              <Badge size="xs" color="yellow" variant="dot" style={{ fontWeight: 600 }}>
                SKIP
              </Badge>
            )}
          </Group>
        )}
      </Stack>
    </Card>
  );
}
