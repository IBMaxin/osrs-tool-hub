import { Table, Group, Text } from '@mantine/core';

type SortField = 'roi' | 'margin' | 'potential_profit' | 'buy_price';

interface ResultsTableHeaderProps {
  sortField: SortField; // Passed to SortIcon component
  onSort: (field: SortField) => void;
  SortIcon: ({ field }: { field: SortField }) => JSX.Element;
  showLogTrade?: boolean;
}

export function ResultsTableHeader({
  sortField: _sortField,
  onSort,
  SortIcon,
  showLogTrade = false
}: ResultsTableHeaderProps) {
  return (
    <Table.Thead>
      <Table.Tr>
        <Table.Th scope="col">Item</Table.Th>
        <Table.Th scope="col" style={{ textAlign: 'right' }}>
          <Group gap={4} justify="flex-end" style={{ cursor: 'pointer' }} onClick={() => onSort('buy_price')} role="button" tabIndex={0} aria-label="Sort by buy price">
            <Text size="sm">Buy Price</Text>
            <SortIcon field="buy_price" />
          </Group>
        </Table.Th>
        <Table.Th scope="col" style={{ textAlign: 'right' }}>Sell Price</Table.Th>
        <Table.Th scope="col" style={{ textAlign: 'right' }}>
          <Group gap={4} justify="flex-end" style={{ cursor: 'pointer' }} onClick={() => onSort('margin')} role="button" tabIndex={0} aria-label="Sort by margin">
            <Text size="sm">Margin</Text>
            <SortIcon field="margin" />
          </Group>
        </Table.Th>
        <Table.Th scope="col" style={{ textAlign: 'right' }}>
          <Group gap={4} justify="flex-end" style={{ cursor: 'pointer' }} onClick={() => onSort('roi')} role="button" tabIndex={0} aria-label="Sort by ROI">
            <Text size="sm">ROI</Text>
            <SortIcon field="roi" />
          </Group>
        </Table.Th>
        <Table.Th scope="col" style={{ textAlign: 'right' }}>
          <Group gap={4} justify="flex-end" style={{ cursor: 'pointer' }} onClick={() => onSort('potential_profit')} role="button" tabIndex={0} aria-label="Sort by potential profit">
            <Text size="sm">Potential Profit</Text>
            <SortIcon field="potential_profit" />
          </Group>
        </Table.Th>
        <Table.Th scope="col" style={{ textAlign: 'center' }}>Volume</Table.Th>
        {showLogTrade && <Table.Th scope="col" style={{ textAlign: 'center' }}>Actions</Table.Th>}
      </Table.Tr>
    </Table.Thead>
  );
}
