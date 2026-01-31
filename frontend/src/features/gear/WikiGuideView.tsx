/**
 * WikiGuideView - Main wiki guide component.
 * 
 * Renders the exact wiki page structure with game stages, tier tables,
 * content-specific tables, and bonus table.
 */

import { useState } from 'react';
import {
  Stack,
  Title,
  Text,
  Tabs,
  Loader,
  Alert,
  Accordion,
  Paper,
  Box,
  Group,
} from '@mantine/core';
import { IconAlertCircle } from '@tabler/icons-react';
import { useWikiGuide } from './hooks/useWikiGuide';
import { EquipmentInterface } from './components/EquipmentInterface';
import { ContentSpecificTable } from './components/ContentSpecificTable';
import { BonusTable } from './components/BonusTable';

/**
 * Main wiki guide view with style tabs.
 */
export function WikiGuideView() {
  const [style, setStyle] = useState<string>('magic');
  
  const { data, isLoading, error } = useWikiGuide(style);
  
  if (isLoading) {
    return (
      <Stack align="center" gap="md" py="xl">
        <Loader size="xl" />
        <Text c="dimmed">Loading wiki guide...</Text>
      </Stack>
    );
  }
  
  if (error) {
    return (
      <Alert
        icon={<IconAlertCircle size={16} />}
        title="Error Loading Guide"
        color="red"
        variant="light"
      >
        {error instanceof Error ? error.message : 'Failed to load wiki guide'}
      </Alert>
    );
  }
  
  if (!data || !data.game_stages) {
    return (
      <Alert
        icon={<IconAlertCircle size={16} />}
        title="No Guide Data"
        color="yellow"
        variant="light"
      >
        No guide data available for {style}. Please check back later.
      </Alert>
    );
  }
  
  return (
    <Stack gap="lg">
      {/* Style Tabs */}
      <Paper p="md" withBorder>
        <Tabs value={style} onChange={(val) => setStyle(val || 'magic')}>
          <Tabs.List>
            <Tabs.Tab value="melee">Melee</Tabs.Tab>
            <Tabs.Tab value="ranged">Ranged</Tabs.Tab>
            <Tabs.Tab value="magic">Magic</Tabs.Tab>
          </Tabs.List>
        </Tabs>
      </Paper>
      
      {/* Title */}
      <Box>
        <Title order={1} tt="capitalize">{style} Gear Progression</Title>
        <Text c="dimmed" size="sm" mt="xs">
          Exact mirror of the OSRS Wiki gear progression guide
        </Text>
      </Box>
      
      {/* Game Stages */}
      <Accordion variant="separated" defaultValue={data.game_stages[0]?.id}>
        {data.game_stages.map((stage) => (
          <Accordion.Item key={stage.id} value={stage.id}>
            <Accordion.Control>
              <Title order={3}>{stage.title}</Title>
            </Accordion.Control>
            <Accordion.Panel>
              <Stack gap="lg">
                {/* Equipment Interfaces - Side by Side */}
                {stage.tiers && stage.tiers.length > 0 && (
                  <Box>
                    <Group gap="lg" align="flex-start" wrap="wrap" justify="center">
                      {stage.tiers.map((tier, index) => (
                        <EquipmentInterface key={`${tier.label}-${index}`} tier={tier} />
                      ))}
                    </Group>
                  </Box>
                )}
                
                {/* Content-Specific Table */}
                {stage.content_specific && stage.content_specific.length > 0 && (
                  <Box mt="xl">
                    <Title order={4} mb="sm">Content Specific Equipment</Title>
                    <ContentSpecificTable
                      rows={stage.content_specific}
                      costLabel={data.cost_per_hour_label}
                    />
                  </Box>
                )}
              </Stack>
            </Accordion.Panel>
          </Accordion.Item>
        ))}
      </Accordion>
      
      {/* Bonus Table */}
      {data.bonus_table && data.bonus_table.length > 0 && (
        <Box>
          <Title order={2} mb="md">
            {style === 'magic' ? 'Magic Damage' : style === 'ranged' ? 'Ranged Strength' : 'Strength'} bonus / Cost
          </Title>
          <BonusTable
            rows={data.bonus_table}
            bonusLabel={style === 'magic' ? 'Magic Damage' : style === 'ranged' ? 'Ranged Strength' : 'Strength'}
          />
        </Box>
      )}
    </Stack>
  );
}
