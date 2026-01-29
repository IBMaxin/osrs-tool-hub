/**
 * Loading progress indicators for better UX during async operations
 */
import { Progress, Box, Text, Stack } from '@mantine/core';

export interface LoadingProgressProps {
  /** Current progress value (0-100) */
  value: number;
  /** Optional label */
  label?: string;
  /** Size variant */
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  /** Color variant */
  color?: string;
  /** Whether to show percentage */
  showPercentage?: boolean;
}

/**
 * LoadingProgress provides visual feedback for operations with known progress.
 * Use for long-running operations where progress can be tracked.
 *
 * @example
 * ```tsx
 * <LoadingProgress
 *   value={progress}
 *   label="Loading items..."
 *   showPercentage
 * />
 * ```
 */
export function LoadingProgress({
  value,
  label,
  size = 'md',
  color = 'osrsGold',
  showPercentage = false,
}: LoadingProgressProps) {
  return (
    <Stack gap="xs">
      {(label || showPercentage) && (
        <Box style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          {label && <Text size="sm" c="dimmed">{label}</Text>}
          {showPercentage && <Text size="sm" fw={500}>{Math.round(value)}%</Text>}
        </Box>
      )}
      <Progress
        value={value}
        size={size}
        color={color}
        animated
        aria-label={label || 'Loading progress'}
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={100}
      />
    </Stack>
  );
}
