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
    return <Skeleton height={42} />;
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
      size="md"
      color="yellow"
    />
  );
}
