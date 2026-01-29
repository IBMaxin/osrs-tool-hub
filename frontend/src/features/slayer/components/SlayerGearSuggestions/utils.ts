import type { SlayerGearResponse } from '../../../../lib/api/gear';

// Equipment slots arranged in wiki-style grid layout
export const EQUIPMENT_GRID = [
  ['head', 'cape', 'neck'],
  ['weapon', 'body', 'shield'],
  ['legs', 'hands', 'feet'],
  ['ring', 'ammo', null],
] as const;

export function getAllItems(
  gearData: SlayerGearResponse | undefined
): Array<{ slot: string; item: NonNullable<SlayerGearResponse['primary_loadout']>['slots'][string]; context: string }> {
  if (!gearData?.primary_loadout) return [];
  
  const primaryLoadout = gearData.primary_loadout;
  const items: Array<{ slot: string; item: NonNullable<SlayerGearResponse['primary_loadout']>['slots'][string]; context: string }> = [];
  
  EQUIPMENT_GRID.flat()
    .filter((slot): slot is NonNullable<typeof slot> => slot !== null)
    .forEach((slot) => {
      const item = primaryLoadout.slots[slot];
      if (!item) return;
      
      // Type assertion: we've already checked item is not null
      const nonNullItem = item as NonNullable<typeof item>;
      
      // Determine context/use case based on item name and slot
      let context = '';
      if (slot === 'weapon') {
        if (nonNullItem.name.toLowerCase().includes('whip') || nonNullItem.name.toLowerCase().includes('tentacle')) {
          context = 'General Slayer';
        } else if (nonNullItem.name.toLowerCase().includes('rapier')) {
          context = 'Combat training / Slayer';
        } else if (nonNullItem.name.toLowerCase().includes('blade')) {
          context = 'Slash weak enemies';
        }
      } else if (slot === 'head' && nonNullItem.name.toLowerCase().includes('serpentine')) {
        context = 'Venom immunity';
      } else if (slot === 'body' && nonNullItem.name.toLowerCase().includes('bandos')) {
        context = 'Strength bonus';
      }
      
      items.push({
        slot,
        item: nonNullItem,
        context,
      });
    });
  
  return items;
}

export function getCombatStyleColor(style: string): string {
  switch (style) {
    case 'melee': return 'osrsRed';
    case 'ranged': return 'osrsGreen';
    case 'magic': return 'osrsBlue';
    default: return 'gray';
  }
}
