import { Table, Group, Text, Badge, Avatar, Stack } from '@mantine/core';
import { FlipOpportunity } from '../../../lib/api';
import { formatGP, formatNumber, formatPrice } from '../utils/format';

interface ResultsTableRowProps {
  flip: FlipOpportunity;
}

export function ResultsTableRow({ flip }: ResultsTableRowProps) {
  return (
    <Table.Tr key={flip.item_id}>
      <Table.Td>
        <Group gap="sm">
          <Avatar src={flip.icon_url} size="md" radius="sm" bg="gray.1">
            {flip.item_name.charAt(0)}
          </Avatar>
          <Stack gap={4}>
            <Group gap="xs" align="center">
              <Text size="md" fw={700} lineClamp={1}>{flip.item_name}</Text>
              {flip.limit && (
                <Badge variant="light" color="blue" size="sm">
                  Limit: {formatNumber(flip.limit)}
                </Badge>
              )}
            </Group>
          </Stack>
        </Group>
      </Table.Td>
      <Table.Td style={{ textAlign: 'right' }}>
        <Text size="sm" ff="monospace" fw={500}>
          {formatPrice(flip.buy_price)}
        </Text>
      </Table.Td>
      <Table.Td style={{ textAlign: 'right' }}>
        <Text size="sm" ff="monospace" fw={500}>
          {formatPrice(flip.sell_price)}
        </Text>
      </Table.Td>
      <Table.Td style={{ textAlign: 'right' }}>
        <Stack gap={2} align="flex-end">
          <Text c={flip.margin > 0 ? 'green' : 'red'} fw={700} size="sm">
            {flip.margin > 0 ? '+' : ''}{formatPrice(flip.margin)}
          </Text>
          {flip.tax && (
            <Text size="xs" c="dimmed">Tax: {formatPrice(flip.tax)}</Text>
          )}
        </Stack>
      </Table.Td>
      <Table.Td style={{ textAlign: 'right' }}>
        <Badge 
          variant="light" 
          color={
            flip.roi >= 10 ? 'green' : 
            flip.roi >= 5 ? 'teal' : 
            flip.roi >= 2 ? 'blue' : 
            flip.roi >= 0 ? 'gray' : 'red'
          }
          size="lg"
        >
          {flip.roi >= 0 ? '+' : ''}{flip.roi.toFixed(2)}%
        </Badge>
      </Table.Td>
      <Table.Td style={{ textAlign: 'right' }}>
        <Text 
          fw={700} 
          size="sm"
          c={
            (flip.potential_profit || 0) >= 10_000_000 ? 'orange' :
            (flip.potential_profit || 0) >= 1_000_000 ? 'yellow' :
            'dark'
          }
        >
          {flip.potential_profit ? formatPrice(flip.potential_profit) : 'N/A'}
        </Text>
      </Table.Td>
      <Table.Td style={{ textAlign: 'center' }}>
        <Text size="sm" c={flip.volume > 0 ? 'dark' : 'dimmed'}>
          {flip.volume > 0 ? formatGP(flip.volume) : 'N/A'}
        </Text>
      </Table.Td>
    </Table.Tr>
  );
}
