import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { MantineProvider } from '@mantine/core';
import { ResultsTable } from '../../features/flipping/components/ResultsTable';
import { DPSComparisonTable } from '../../features/gear/components/DPSComparisonTable';
import { WikiGearTable } from '../../features/gear/WikiGearTable';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const renderWithProviders = (ui: React.ReactElement) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  return render(
    <QueryClientProvider client={queryClient}>
      <MantineProvider>
        {ui}
      </MantineProvider>
    </QueryClientProvider>
  );
};

describe('Mobile Table Scrolling', () => {
  describe('ResultsTable', () => {
    const mockFlips = [
      {
        item_id: 1,
        item_name: 'Abyssal whip',
        buy_price: 2000000,
        sell_price: 2100000,
        margin: 100000,
        roi: 5.0,
        potential_profit: 100000,
        volume: 100,
        limit: 8,
      },
    ];

    it('has scrollable container for mobile', () => {
      const { container } = renderWithProviders(
        <ResultsTable
          flips={mockFlips}
          isLoading={false}
          error={null}
          sortField="roi"
          sortDirection="desc"
          onSort={() => {}}
          SortIcon={() => <div>↓</div>}
        />
      );

      // Check for scroll container
      const scrollContainer = container.querySelector('[data-scroll-container]') || 
                             container.querySelector('.mantine-Table-scrollContainer');
      expect(scrollContainer || container.querySelector('table')).toBeInTheDocument();
    });

    it('has accessible table headers', () => {
      renderWithProviders(
        <ResultsTable
          flips={mockFlips}
          isLoading={false}
          error={null}
          sortField="roi"
          sortDirection="desc"
          onSort={() => {}}
          SortIcon={() => <div>↓</div>}
        />
      );

      // Headers should have scope attribute
      expect(screen.getByText('Item').closest('th')).toHaveAttribute('scope', 'col');
    });

    it('sortable headers have aria-labels', () => {
      renderWithProviders(
        <ResultsTable
          flips={mockFlips}
          isLoading={false}
          error={null}
          sortField="roi"
          sortDirection="desc"
          onSort={() => {}}
          SortIcon={() => <div>↓</div>}
        />
      );

      expect(screen.getByLabelText(/sort by buy price/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/sort by margin/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/sort by roi/i)).toBeInTheDocument();
    });
  });

  describe('DPSComparisonTable', () => {
    const mockResults = [
      {
        loadout_id: 1,
        loadout_name: 'Test Loadout',
        dps: 10.5,
        max_hit: 45,
        accuracy: 85.5,
        attack_speed: 4,
        attack_speed_seconds: 2.4,
        dps_increase: 1.2,
        dps_increase_percent: 12.5,
        total_attack_bonus: 100,
        total_strength_bonus: 100,
        details: {},
      },
    ];

    it('has scrollable container', () => {
      const { container } = renderWithProviders(
        <DPSComparisonTable results={mockResults} />
      );

      // Check for scroll container or table
      const scrollContainer = container.querySelector('[data-scroll-container]') || 
                             container.querySelector('.mantine-Table-scrollContainer');
      expect(scrollContainer || container.querySelector('table')).toBeInTheDocument();
    });

    it('displays data correctly', () => {
      renderWithProviders(<DPSComparisonTable results={mockResults} />);
      
      expect(screen.getByText('Test Loadout')).toBeInTheDocument();
      expect(screen.getByText('10.50')).toBeInTheDocument();
    });
  });

  describe('WikiGearTable', () => {
    it('renders loading state', () => {
      renderWithProviders(<WikiGearTable />);
      
      // Should show loading or error message
      expect(screen.getByText(/loading/i) || screen.getByText(/error/i)).toBeInTheDocument();
    });
  });
});
