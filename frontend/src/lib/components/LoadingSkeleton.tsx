import { Skeleton, Stack } from '@mantine/core';

interface LoadingSkeletonProps {
  rows?: number;
}

export function LoadingSkeleton({ rows = 5 }: LoadingSkeletonProps) {
  return (
    <Stack gap="sm">
      {Array.from({ length: rows }).map((_, i) => (
        <Skeleton
          key={i}
          height={40}
          radius="md"
          animate
          styles={{ root: { backgroundColor: '#4A360C' } }}
        />
      ))}
    </Stack>
  );
}
