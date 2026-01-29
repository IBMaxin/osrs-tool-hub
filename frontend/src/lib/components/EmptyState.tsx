/**
 * Enhanced empty state component for better UX
 */
import { Stack, Text, Button, Box } from '@mantine/core';
import { ReactNode } from 'react';

export interface EmptyStateProps {
  /** Icon to display (React element) */
  icon: ReactNode;
  /** Title of the empty state */
  title: string;
  /** Description/message */
  description: string;
  /** Optional action button */
  action?: {
    label: string;
    onClick: () => void;
  };
  /** Size variant */
  size?: 'sm' | 'md' | 'lg';
}

/**
 * EmptyState provides a consistent UI for empty/no-data states.
 * Use this instead of simple "No data" text to provide better user guidance.
 *
 * @example
 * ```tsx
 * <EmptyState
 *   icon={<IconCoins size={48} />}
 *   title="No flips found"
 *   description="Try adjusting your filters to see more results."
 *   action={{
 *     label: 'Reset Filters',
 *     onClick: () => resetFilters()
 *   }}
 * />
 * ```
 */
export function EmptyState({
  icon,
  title,
  description,
  action,
  size = 'md',
}: EmptyStateProps) {
  const titleSize = {
    sm: 'md',
    md: 'lg',
    lg: 'xl',
  }[size] as 'md' | 'lg' | 'xl';

  const descSize = {
    sm: 'xs',
    md: 'sm',
    lg: 'md',
  }[size] as 'xs' | 'sm' | 'md';

  const padding = {
    sm: 'md',
    md: 'xl',
    lg: 'xl',
  }[size];

  return (
    <Box p={padding}>
      <Stack align="center" gap="md" style={{ maxWidth: 400, margin: '0 auto' }}>
        <Box
          style={{
            color: 'var(--mantine-color-gray-5)',
            opacity: 0.6,
          }}
          aria-hidden="true"
        >
          {icon}
        </Box>

        <Stack align="center" gap="xs" style={{ textAlign: 'center' }}>
          <Text fw={600} size={titleSize} c="dimmed">
            {title}
          </Text>
          <Text size={descSize} c="dimmed" style={{ lineHeight: 1.6 }}>
            {description}
          </Text>
        </Stack>

        {action && (
          <Button
            variant="light"
            onClick={action.onClick}
            mt="xs"
            aria-label={action.label}
          >
            {action.label}
          </Button>
        )}
      </Stack>
    </Box>
  );
}
