/**
 * Wiki image URL utilities.
 * 
 * These functions handle derivation of OSRS Wiki image URLs from item names.
 * The wiki uses a consistent pattern, but some items require explicit overrides.
 */

const WIKI_BASE_URL = 'https://oldschool.runescape.wiki/images';

/**
 * Derive wiki image filename from item name.
 * 
 * Handles the wiki's filename conventions:
 * - Spaces → underscores
 * - Apostrophes → %27
 * - Preserve (i), (u), (f), etc.
 * - Strip #... anchors
 * 
 * @param itemName - The exact item name from the wiki
 * @returns The derived filename (without path or extension)
 */
function deriveImageFilename(itemName: string): string {
  // Strip section anchors (e.g., "Iron arrow#(unp)" → "Iron arrow")
  let filename = itemName.split('#')[0];
  
  // Replace spaces with underscores
  filename = filename.replace(/\s+/g, '_');
  
  // URL encode apostrophes
  filename = filename.replace(/'/g, '%27');
  
  return filename;
}

/**
 * Get wiki item image URL.
 * 
 * Resolution logic (following plan requirements):
 * 1. If icon_override exists → use it
 * 2. Else derive from name
 * 3. Else fail loudly (throw error - no silent fallback)
 * 
 * @param itemName - The exact item name from the wiki
 * @param iconOverride - Optional wiki image base name override
 * @returns Full wiki image URL
 * @throws Error if itemName is invalid
 */
export function getWikiItemImageUrl(itemName: string, iconOverride?: string): string {
  if (!itemName || typeof itemName !== 'string') {
    throw new Error(
      `Invalid item name for wiki image: ${JSON.stringify(itemName)}. ` +
      `Item name must be a non-empty string.`
    );
  }
  
  let filename: string;
  
  if (iconOverride) {
    // Use explicit override
    filename = iconOverride;
  } else {
    // Derive from item name
    filename = deriveImageFilename(itemName);
  }
  
  // Build full URL with _detail.png suffix
  return `${WIKI_BASE_URL}/${filename}_detail.png`;
}

/**
 * Get wiki item image URL from slot data.
 * 
 * Handles both occupied slots (with name and optional icon_override)
 * and empty slots (null).
 * 
 * @param slotData - Slot data from guide JSON (null or { name, icon_override? })
 * @returns Wiki image URL or null for empty slots
 * @throws Error if slotData structure is invalid
 */
export function getSlotImageUrl(
  slotData: { name: string; icon_override?: string } | null
): string | null {
  if (slotData === null) {
    return null;
  }
  
  if (!slotData || typeof slotData !== 'object') {
    throw new Error(
      `Invalid slot data structure: ${JSON.stringify(slotData)}. ` +
      `Expected null or { name: string, icon_override?: string }.`
    );
  }
  
  if (!slotData.name) {
    throw new Error(
      `Slot data missing required 'name' field: ${JSON.stringify(slotData)}`
    );
  }
  
  return getWikiItemImageUrl(slotData.name, slotData.icon_override);
}
