/**
 * Helper functions for WikiGearTable component.
 */

export interface WikiItem {
  id: number | null;
  name: string;
  icon: string;
  price: number | null;
  wiki_url: string;
}

export interface TierGroup {
  tier: string;
  items: WikiItem[];
}

/**
 * Format price in compact form (e.g., 1.2m, 450k).
 */
export function formatPrice(price: number | null): string {
  if (price === null || price === 0) return 'Untradeable';
  if (price >= 1000000) return `${(price / 1000000).toFixed(1)}m`;
  if (price >= 1000) return `${(price / 1000).toFixed(0)}k`;
  return `${price} gp`;
}

/**
 * Get color for tier badge based on tier name.
 */
export function getTierColor(tierName: string): string {
  const upperTier = tierName.toLowerCase();
  if (upperTier.includes('torva') || upperTier.includes('bis') || upperTier.includes('shadow') || 
      upperTier.includes('twisted') || upperTier.includes('ancestral') || upperTier.includes('masori')) {
    return 'orange';
  }
  if (upperTier.includes('inquisitor') || upperTier.includes('oathplate') || 
      upperTier.includes('zaryte') || upperTier.includes('virtus')) {
    return 'red';
  }
  if (upperTier.includes('bandos') || upperTier.includes('neitiznot') || 
      upperTier.includes('crystal') || upperTier.includes('ahrim')) {
    return 'blue';
  }
  return 'gray';
}

/**
 * Slot order for sorting.
 */
export const SLOT_ORDER: Record<string, number> = {
  "head": 1,
  "cape": 2,
  "neck": 3,
  "ammo": 4,
  "weapon": 5,
  "body": 6,
  "shield": 7,
  "legs": 8,
  "gloves": 9,
  "boots": 10,
  "ring": 11,
};
