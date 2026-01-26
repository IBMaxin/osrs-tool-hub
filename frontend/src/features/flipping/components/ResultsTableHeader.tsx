import { Table, Group, Text } from '@mantine/core';

type SortField = 'roi' | 'margin' | 'potential_profit' | 'buy_price';

interface ResultsTableHeaderProps {
  sortField: SortField; // Passed to SortIcon component
  onSort: (field: SortField) => void;
  SortIcon: ({ field }: { field: SortField }) => JSX.Element;
}

export function ResultsTableHeader({
  sortField: _sortField,
  onSort,
  SortIcon
}: ResultsTableHeaderProps) {
  return (
    <Table.Thead>
      <Table.Tr>
        <Table.Th>Item</Table.Th>
        <Table.Th style={{ textAlign: 'right' }}>
          <Group gap={4} justify="flex-end" style={{ cursor: 'pointer' }} onClick={() => onSort('buy_price')}>
            <Text size="sm">Buy Price</Text>
            <SortIcon field="buy_price" />
          </Group>
        </Table.Th>
        <Table.Th style={{ textAlign: 'right' }}>Sell Price</Table.Th>
        <Table.Th style={{ textAlign: 'right' }}>
          <Group gap={4} justify="flex-end" style={{ cursor: 'pointer' }} onClick={() => onSort('margin')}>
            <Text size="sm">Margin</Text>
            <SortIcon field="margin" />
          </Group>
        </Table.Th>
        <Table.Th style={{ textAlign: 'right' }}>
          <Group gap={4} justify="flex-end" style={{ cursor: 'pointer' }} onClick={() => onSort('roi')}>
            <Text size="sm">ROI</Text>
            <SortIcon field="roi" />
          </Group>
        </Table.Th>
        <Table.Th style={{ textAlign: 'right' }}>
          <Group gap={4} justify="flex-end" style={{ cursor: 'pointer' }} onClick={() => onSort('potential_profit')}>
            <Text size="sm">Potential Profit</Text>
            <SortIcon field="potential_profit" />
          </Group>
        </Table.Th>
        <Table.Th style={{ textAlign: 'center' }}>Volume</Table.Th>
      </Table.Tr>
    </Table.Thead>
  );
}
