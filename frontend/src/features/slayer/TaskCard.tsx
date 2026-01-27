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
      p="md"
      withBorder
      radius="md"
      style={{
        borderLeftWidth: 4,
        borderLeftColor: `var(--mantine-color-${categoryColor}-6)`,
        transition: 'transform 0.2s ease, box-shadow 0.2s ease, opacity 0.5s ease, border-color 0.2s ease',
        opacity: 0,
        transform: 'translateY(10px)',
        cursor: 'pointer',
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = 'translateY(-4px)';
        e.currentTarget.style.boxShadow = 'var(--mantine-shadow-md)';
        e.currentTarget.style.borderLeftColor = `var(--mantine-color-${categoryColor}-7)`;
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = 'translateY(0)';
        e.currentTarget.style.boxShadow = 'var(--mantine-shadow-sm)';
        e.currentTarget.style.borderLeftColor = `var(--mantine-color-${categoryColor}-6)`;
      }}
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onGetAdvice(task.task_id);
        }
      }}
    >
      <Stack gap="md" align="center">
        {/* Top Section: Monster Icon with Combat Level Badge */}
        <Box pos="relative">
          {!imageError ? (
            <Image
              src={imageUrl}
              alt={task.monster_name}
              w={96}
              h={96}
              fit="contain"
              radius="md"
              style={{ 
                border: '2px solid var(--mantine-color-gray-3)',
                backgroundColor: 'var(--mantine-color-gray-1)'
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
              bg="gray.1"
              style={{ border: '2px solid var(--mantine-color-gray-3)' }}
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
            style={{ transform: 'translateX(-50%)' }}
          >
            Lvl {task.combat_level}
          </Badge>
        </Box>

        {/* Middle Section: Monster Name and Amount */}
        <Stack gap={4} align="center" style={{ flex: 1, width: '100%' }}>
          <Text fw={700} size="lg" ta="center" lineClamp={2}>
            {task.monster_name}
          </Text>
          <Text size="sm" c="dimmed" ta="center">
            {task.amount} {task.category}
          </Text>
        </Stack>

        {/* Bottom Row: Weight Badge and Get Advice Button */}
        <Group justify="space-between" w="100%" mt="auto">
          <Badge
            size="sm"
            color={hasHighWeight ? 'blue' : 'gray'}
            variant="light"
          >
            Weight: {task.weight}
          </Badge>
          <Button
            size="xs"
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
          <Group gap="xs" mt={-8}>
            {task.is_blockable && (
              <Badge size="xs" color="red" variant="dot">
                BLOCK
              </Badge>
            )}
            {task.is_skippable && (
              <Badge size="xs" color="yellow" variant="dot">
                SKIP
              </Badge>
            )}
          </Group>
        )}
      </Stack>
    </Card>
  );
}
