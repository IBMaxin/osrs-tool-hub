import { Group, Text, Badge } from '@mantine/core';

interface WeaknessesSectionProps {
  weaknesses: string[];
}

export function WeaknessesSection({ weaknesses }: WeaknessesSectionProps) {
  if (weaknesses.length === 0) return null;

  return (
    <Group gap="xs">
      <Text size="sm" fw={600} c="dimmed">
        Weaknesses:
      </Text>
      {weaknesses.map((weakness, i) => (
        <Badge key={i} size="sm" color="osrsRed" variant="light">
          {weakness}
        </Badge>
      ))}
    </Group>
  );
}
