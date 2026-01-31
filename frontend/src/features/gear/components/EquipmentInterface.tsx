/**
 * EquipmentInterface - OSRS equipment paperdoll layout.
 * 
 * Renders one full loadout with the classic OSRS equipment screen:
 * - Brown equipment interface background
 * - Slots positioned exactly as in-game
 * - Gold coin icon + cost below
 */

import { Box, Image, Text, Tooltip, Stack, Group } from '@mantine/core';
import type { WikiGuideTier } from '../../../lib/api/types';
import { getSlotImageUrl } from '../../../lib/utils/wikiImages';

interface EquipmentInterfaceProps {
  tier: WikiGuideTier;
}

/**
 * Format price with K/M suffix.
 */
function formatPrice(price: number): string {
  if (price >= 1000000) {
    return `${(price / 1000000).toFixed(3)}M`;
  }
  if (price >= 1000) {
    return `${(price / 1000).toFixed(0)}K`;
  }
  return `${price}`;
}

/**
 * Single equipment slot with image or empty.
 */
function EquipmentSlot({ slotData, slotName }: { slotData: any; slotName: string }) {
  try {
    const imageUrl = getSlotImageUrl(slotData);
    
    const slotStyle = {
      width: '44px',
      height: '44px',
      backgroundColor: '#3d3530',
      border: '2px solid #1a1613',
      borderRadius: '3px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      position: 'relative' as const,
    };
    
    if (imageUrl === null) {
      // Empty slot
      return <Box style={slotStyle} />;
    }
    
    // Occupied slot with wiki image
    return (
      <Tooltip label={slotData.name} position="top" withinPortal>
        <Box style={slotStyle}>
          <Image
            src={imageUrl}
            alt={slotData.name}
            width={36}
            height={36}
            fit="contain"
            style={{ imageRendering: 'pixelated' }}
          />
        </Box>
      </Tooltip>
    );
  } catch (error) {
    // Fail loudly
    console.error(`Error rendering slot '${slotName}':`, error);
    return (
      <Tooltip
        label={`Error: ${error instanceof Error ? error.message : 'Unknown'}`}
        position="top"
        color="red"
        withinPortal
      >
        <Box
          style={{
            width: '44px',
            height: '44px',
            backgroundColor: '#ff4444',
            border: '2px solid #cc0000',
            borderRadius: '3px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Text size="xl" c="white" fw={700}>!</Text>
        </Box>
      </Tooltip>
    );
  }
}

/**
 * Equipment interface with in-game layout.
 */
export function EquipmentInterface({ tier }: EquipmentInterfaceProps) {
  const slots = tier.slots;
  
  return (
    <Stack gap="xs" align="center">
      {/* Tier label */}
      <Text size="sm" fw={600} ta="center" c="dark">
        {tier.label}
      </Text>
      
      {/* Equipment paperdoll */}
      <Box
        style={{
          backgroundColor: '#5a4a3a',
          border: '3px solid #3d3530',
          borderRadius: '6px',
          padding: '12px',
          boxShadow: 'inset 0 2px 4px rgba(0,0,0,0.3)',
          width: '180px',
        }}
      >
        <Stack gap={4} align="center">
          {/* Row 1: Head */}
          <Group gap={4} wrap="nowrap" justify="center">
            <EquipmentSlot slotData={slots.head} slotName="head" />
          </Group>
          
          {/* Row 2: Cape, Neck, Ammo */}
          <Group gap={4} wrap="nowrap" justify="center">
            <EquipmentSlot slotData={slots.cape} slotName="cape" />
            <EquipmentSlot slotData={slots.neck} slotName="neck" />
            <EquipmentSlot slotData={slots.ammo} slotName="ammo" />
          </Group>
          
          {/* Row 3: Weapon, Body, Shield */}
          <Group gap={4} wrap="nowrap" justify="center">
            <EquipmentSlot slotData={slots.weapon} slotName="weapon" />
            <EquipmentSlot slotData={slots.body} slotName="body" />
            <EquipmentSlot slotData={slots.shield} slotName="shield" />
          </Group>
          
          {/* Row 4: Legs */}
          <Group gap={4} wrap="nowrap" justify="center">
            <EquipmentSlot slotData={slots.legs} slotName="legs" />
          </Group>
          
          {/* Row 5: Hands, Feet, Ring */}
          <Group gap={4} wrap="nowrap" justify="center">
            <EquipmentSlot slotData={slots.hands} slotName="hands" />
            <EquipmentSlot slotData={slots.feet} slotName="feet" />
            <EquipmentSlot slotData={slots.ring} slotName="ring" />
          </Group>
        </Stack>
      </Box>
      
      {/* Total cost with gold coin icon */}
      <Group gap={4} align="center">
        <Text size="xl" style={{ color: '#FFD700' }}>🪙</Text>
        <Text size="sm" fw={600} c="blue">
          {formatPrice(tier.total_cost)}
        </Text>
      </Group>
    </Stack>
  );
}
