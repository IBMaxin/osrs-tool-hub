import { Box, Table, Group, Stack, Skeleton } from '@mantine/core';

export function ResultsTableSkeleton() {
  return (
    <Box p="md">
      <Table.ScrollContainer minWidth={900}>
        <Table striped highlightOnHover verticalSpacing="md">
          <Table.Thead>
            <Table.Tr>
              <Table.Th>Item</Table.Th>
              <Table.Th style={{ textAlign: 'right' }}>Buy Price</Table.Th>
              <Table.Th style={{ textAlign: 'right' }}>Sell Price</Table.Th>
              <Table.Th style={{ textAlign: 'right' }}>Margin</Table.Th>
              <Table.Th style={{ textAlign: 'right' }}>ROI</Table.Th>
              <Table.Th style={{ textAlign: 'right' }}>Potential Profit</Table.Th>
              <Table.Th style={{ textAlign: 'center' }}>Volume</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {Array.from({ length: 5 }).map((_, i) => (
              <Table.Tr key={i}>
                <Table.Td>
                  <Group gap="sm">
                    <Skeleton height={40} circle />
                    <Stack gap={4}>
                      <Skeleton height={16} width={150} />
                      <Skeleton height={12} width={100} />
                    </Stack>
                  </Group>
                </Table.Td>
                <Table.Td style={{ textAlign: 'right' }}>
                  <Skeleton height={16} width={100} ml="auto" />
                </Table.Td>
                <Table.Td style={{ textAlign: 'right' }}>
                  <Skeleton height={16} width={100} ml="auto" />
                </Table.Td>
                <Table.Td style={{ textAlign: 'right' }}>
                  <Skeleton height={16} width={80} ml="auto" />
                </Table.Td>
                <Table.Td style={{ textAlign: 'right' }}>
                  <Skeleton height={24} width={60} ml="auto" />
                </Table.Td>
                <Table.Td style={{ textAlign: 'right' }}>
                  <Skeleton height={16} width={90} ml="auto" />
                </Table.Td>
                <Table.Td style={{ textAlign: 'center' }}>
                  <Skeleton height={16} width={70} mx="auto" />
                </Table.Td>
              </Table.Tr>
            ))}
          </Table.Tbody>
        </Table>
      </Table.ScrollContainer>
    </Box>
  );
}
