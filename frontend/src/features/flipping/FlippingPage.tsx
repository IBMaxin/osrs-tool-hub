import { useState, useEffect } from 'react';
import { 
  Container, 
  Title, 
  Group, 
  Text, 
  Stack,
  Button,
  Tabs
} from '@mantine/core';
import { IconRefresh, IconCoins, IconHistory, IconChartBar, IconBell } from '@tabler/icons-react';
import { FlipFilters } from '../../lib/api';
import { FiltersBar } from './components/FiltersBar';
import { ResultsTable } from './components/ResultsTable';
import { TradeLogForm } from './components/TradeLogForm';
import { TradeHistory } from './components/TradeHistory';
import { TradeStats } from './components/TradeStats';
import { WatchlistManager } from './components/WatchlistManager';
import { AlertNotifications } from './components/AlertNotifications';
import { useFlips } from './hooks/useFlips';

// Utility to get or create user ID from localStorage
function getUserId(): string {
  const key = 'osrs_tool_hub_user_id';
  let userId = localStorage.getItem(key);
  if (!userId) {
    // Generate a simple UUID-like ID
    userId = 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    localStorage.setItem(key, userId);
  }
  return userId;
}

export function FlippingPage() {
  const [userId] = useState<string>(getUserId());
  const [activeTab, setActiveTab] = useState<string>('opportunities');

  // Filters State
  const [filters, setFilters] = useState<FlipFilters>({
    max_budget: undefined,
    min_roi: 0.0,
    min_volume: 0
  });

  // Use custom hook for flips data and sorting
  const {
    sortedFlips,
    isLoading,
    error,
    refetch,
    isRefetching,
    sortField,
    sortDirection,
    handleSort,
    SortIcon,
  } = useFlips({ filters });

  return (
    <Container size="xl" py="xl">
      <Stack gap="lg">
        <Group justify="space-between" wrap="wrap">
          <div>
            <Title order={2} mb={4}>Flip Finder</Title>
            <Text c="dimmed" size="sm">Find profitable Grand Exchange flips</Text>
          </div>
          {activeTab === 'opportunities' && (
            <Button 
              leftSection={<IconRefresh size={16} />} 
              onClick={() => refetch()} 
              loading={isRefetching}
              variant="light"
            >
              Refresh
            </Button>
          )}
        </Group>

        <Tabs value={activeTab} onChange={(value) => setActiveTab(value || 'opportunities')}>
          <Tabs.List>
            <Tabs.Tab value="opportunities" leftSection={<IconCoins size={16} />}>
              Opportunities
            </Tabs.Tab>
            <Tabs.Tab value="trades" leftSection={<IconHistory size={16} />}>
              My Trades
            </Tabs.Tab>
            <Tabs.Tab value="stats" leftSection={<IconChartBar size={16} />}>
              Stats
            </Tabs.Tab>
          </Tabs.List>

          <Tabs.Panel value="opportunities" pt="md">
            <Stack gap="lg">
              <FiltersBar filters={filters} onFiltersChange={setFilters} />
              <ResultsTable
                flips={sortedFlips}
                isLoading={isLoading}
                error={error}
                sortField={sortField}
                sortDirection={sortDirection}
                onSort={handleSort}
                SortIcon={SortIcon}
                userId={userId}
              />
            </Stack>
          </Tabs.Panel>

          <Tabs.Panel value="trades" pt="md">
            <Stack gap="lg">
              <TradeLogForm userId={userId} />
              <TradeHistory userId={userId} />
            </Stack>
          </Tabs.Panel>

          <Tabs.Panel value="watchlist" pt="md">
            <Stack gap="lg">
              <WatchlistManager userId={userId} />
              <AlertNotifications userId={userId} />
            </Stack>
          </Tabs.Panel>

          <Tabs.Panel value="stats" pt="md">
            <TradeStats userId={userId} />
          </Tabs.Panel>
        </Tabs>
      </Stack>
    </Container>
  );
}
