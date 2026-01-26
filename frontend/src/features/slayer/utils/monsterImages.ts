/**
 * Utilities for generating monster image URLs from OSRS Wiki.
 */

/**
 * Generate monster icon URL (OSRS wiki format).
 * 
 * @param monsterName - Monster name
 * @returns URL to monster image
 */
export function getMonsterIconUrl(monsterName: string): string {
  // OSRS wiki monster images typically use: Monster_name.png or Monster_name_detail.png
  // Names are usually title case with underscores
  let safeName = monsterName
    .trim()
    .replace(/ /g, '_')
    .replace(/'/g, '%27');
  
  // OSRS wiki uses title case for monster names
  // e.g., "Abyssal demon" -> "Abyssal_demon"
  safeName = safeName.split('_').map(word => {
    // Handle special cases
    if (word.toLowerCase() === 'demon') return 'demon';
    if (word.toLowerCase() === 'devil') return 'devil';
    if (word.toLowerCase() === 'spectre') return 'spectre';
    // Capitalize first letter, rest lowercase
    return word.charAt(0).toUpperCase() + word.slice(1).toLowerCase();
  }).join('_');
  
  // Try detail version first (most common for monsters)
  return `https://oldschool.runescape.wiki/images/${safeName}_detail.png`;
}

/**
 * Get category color for visual styling.
 * 
 * @param category - Monster category
 * @returns Color name
 */
export function getCategoryColor(category: string): string {
  const lower = category.toLowerCase();
  if (lower.includes('demon')) return 'red';
  if (lower.includes('dragon')) return 'green';
  if (lower.includes('undead')) return 'gray';
  if (lower.includes('kalphite')) return 'yellow';
  return 'blue';
}
