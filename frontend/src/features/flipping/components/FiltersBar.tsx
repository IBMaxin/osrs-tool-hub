import { 
  Card, 
  Stack, 
  Group, 
  Text, 
  Divider, 
  Grid, 
  NumberInput, 
  ThemeIcon, 
  ActionIcon 
} from '@mantine/core';
import { IconFilter, IconCoins, IconChartBar, IconX } from '@tabler/icons-react';
import { FlipFilters } from '../../../lib/api';

interface FiltersBarProps {
  filters: FlipFilters;
  onFiltersChange: (filters: FlipFilters) => void;
}

export function FiltersBar({ filters, onFiltersChange }: FiltersBarProps) {
  return (
    <Card withBorder shadow="md" radius="md" p="md">
      <Stack gap="md">
        <Group gap="xs">
          <IconFilter size={18} />
          <Text fw={500} size="sm">Filters</Text>
        </Group>
        <Divider />
        <Grid align="end">
          <Grid.Col span={{ base: 12, sm: 4 }}>
            <NumberInput
              label="Max Budget (GP)"
              placeholder="Unlimited"
              thousandSeparator=","
              min={0}
              leftSection={
                <ThemeIcon size="sm" variant="light" color="yellow">
                  <IconCoins size={16} />
                </ThemeIcon>
              }
              value={filters.max_budget || ''}
              onChange={(val) => onFiltersChange({ ...filters, max_budget: val as number | undefined })}
              rightSection={
                filters.max_budget ? (
                  <ActionIcon
                    variant="subtle"
                    size="sm"
                    onClick={() => onFiltersChange({ ...filters, max_budget: undefined })}
                  >
                    <IconX size={14} />
                  </ActionIcon>
                ) : null
              }
            />
          </Grid.Col>
          <Grid.Col span={{ base: 6, sm: 4 }}>
            <NumberInput
              label="Min ROI (%)"
              placeholder="0.0"
              min={0}
              max={100}
              step={0.1}
              decimalScale={1}
              suffix="%"
              leftSection={
                <ThemeIcon size="sm" variant="light" color="blue">
                  <IconChartBar size={16} />
                </ThemeIcon>
              }
              value={filters.min_roi}
              onChange={(val) => onFiltersChange({ ...filters, min_roi: val as number })}
            />
          </Grid.Col>
          <Grid.Col span={{ base: 6, sm: 4 }}>
            <NumberInput
              label="Min Volume"
              placeholder="0"
              min={0}
              value={filters.min_volume}
              onChange={(val) => onFiltersChange({ ...filters, min_volume: val as number })}
            />
          </Grid.Col>
        </Grid>
      </Stack>
    </Card>
  );
}
