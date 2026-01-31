/**
 * ContentSpecificTable - Equipment/upgrade table with buy cost and hourly cost.
 */

import { Table, Text } from '@mantine/core';
import type { WikiGuideContentSpecific } from '../../../lib/api/types';

interface ContentSpecificTableProps {
  rows: WikiGuideContentSpecific[];
  costLabel: string;
}

/**
 * Format cost (number or null for N/A).
 */
function formatCost(cost: number | null): string {
  if (cost === null) {
    return 'N/A';
  }
  return cost.toLocaleString();
}

/**
 * Content-specific equipment table.
 */
export function ContentSpecificTable({ rows, costLabel }: ContentSpecificTableProps) {
  if (!rows || rows.length === 0) {
    return null;
  }
  
  return (
    <Table striped withTableBorder highlightOnHover>
      <Table.Thead>
        <Table.Tr>
          <Table.Th>Equipment / Upgrade</Table.Th>
          <Table.Th style={{ textAlign: 'right' }}>Cost (Buy)</Table.Th>
          <Table.Th style={{ textAlign: 'right' }}>{costLabel}</Table.Th>
        </Table.Tr>
      </Table.Thead>
      <Table.Tbody>
        {rows.map((row, index) => (
          <Table.Tr key={index}>
            <Table.Td>
              <Text size="sm">
                {row.name}
                {row.use_case && (
                  <Text span size="xs" c="dimmed" ml={4}>
                    ({row.use_case})
                  </Text>
                )}
              </Text>
            </Table.Td>
            <Table.Td style={{ textAlign: 'right' }}>
              <Text size="sm">{formatCost(row.cost_buy)}</Text>
            </Table.Td>
            <Table.Td style={{ textAlign: 'right' }}>
              <Text size="sm">{formatCost(row.cost_per_hour)}</Text>
            </Table.Td>
          </Table.Tr>
        ))}
      </Table.Tbody>
    </Table>
  );
}
