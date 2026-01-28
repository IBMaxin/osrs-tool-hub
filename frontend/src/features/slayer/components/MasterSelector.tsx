import { SegmentedControl, Skeleton } from '@mantine/core';

interface MasterSelectorProps {
  masters: string[] | undefined;
  isLoading: boolean;
  selectedMaster: string | null;
  onMasterChange: (master: string) => void;
}

export function MasterSelector({
  masters,
  isLoading,
  selectedMaster,
  onMasterChange
}: MasterSelectorProps) {
  if (isLoading) {
    return <Skeleton height={48} radius="md" />;
  }

  if (!masters || masters.length === 0) {
    return null;
  }

  return (
    <SegmentedControl
      value={selectedMaster || ''}
      onChange={(value) => {
        onMasterChange(value);
      }}
      data={masters.map(master => ({ value: master, label: master }))}
      fullWidth
      size="lg"
      color="yellow"
      radius="md"
      style={{
        backgroundColor: 'var(--mantine-color-dark-7)',
      }}
    />
  );
}
