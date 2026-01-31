/**
 * BonusTable - Bonus comparison table (Item | Bonus | Cost | Δ | Cost/Δ).
 */

import { Table, Text } from '@mantine/core';
import type { WikiGuideBonusRow } from '../../../lib/api/types';

interface BonusTableProps {
  rows: WikiGuideBonusRow[];
  bonusLabel: string;
}

/**
 * Format cost or N/A.
 */
function formatCost(cost: number | null): string {
  if (cost === null) {
    return 'N/A';
  }
  return cost.toLocaleString();
}

/**
 * Bonus comparison table.
 */
export function BonusTable({ rows, bonusLabel }: BonusTableProps) {
  if (!rows || rows.length === 0) {
    return null;
  }
  
  return (
    <Table striped withTableBorder highlightOnHover>
      <Table.Thead>
        <Table.Tr>
          <Table.Th>Item</Table.Th>
          <Table.Th style={{ textAlign: 'center' }}>{bonusLabel}</Table.Th>
          <Table.Th style={{ textAlign: 'right' }}>Cost</Table.Th>
          <Table.Th style={{ textAlign: 'center' }}>Δ</Table.Th>
          <Table.Th style={{ textAlign: 'right' }}>Cost / Δ</Table.Th>
        </Table.Tr>
      </Table.Thead>
      <Table.Tbody>
        {rows.map((row, index) => (
          <Table.Tr key={index}>
            <Table.Td>
              <Text size="sm">{row.item_name}</Text>
            </Table.Td>
            <Table.Td style={{ textAlign: 'center' }}>
              <Text size="sm">{row.bonus}</Text>
            </Table.Td>
            <Table.Td style={{ textAlign: 'right' }}>
              <Text size="sm">{formatCost(row.cost)}</Text>
            </Table.Td>
            <Table.Td style={{ textAlign: 'center' }}>
              <Text size="sm">{row.delta || '—'}</Text>
            </Table.Td>
            <Table.Td style={{ textAlign: 'right' }}>
              <Text size="sm">{formatCost(row.cost_per_delta)}</Text>
            </Table.Td>
          </Table.Tr>
        ))}
      </Table.Tbody>
    </Table>
  );
}
