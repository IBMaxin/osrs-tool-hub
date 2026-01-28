/**
 * Shared formatting utilities for numbers, prices, and currency.
 */

/**
 * Format GP value in compact form (e.g., 1.5M, 500k).
 * 
 * @param val - Value in GP
 * @returns Formatted string
 */
export function formatGP(val: number): string {
  if (val >= 1_000_000) return `${(val / 1_000_000).toFixed(1)}M`;
  if (val >= 1_000) return `${(val / 1_000).toFixed(0)}k`;
  return val.toString();
}

/**
 * Format number with thousand separators (e.g., 1,234,567).
 * 
 * @param val - Number to format
 * @returns Formatted string
 */
export function formatNumber(val: number): string {
  return new Intl.NumberFormat().format(val);
}

/**
 * Format price with "gp" suffix (e.g., 1,234,567 gp).
 * 
 * @param val - Price in GP
 * @returns Formatted string
 */
export function formatPrice(val: number): string {
  return `${formatNumber(val)} gp`;
}

/**
 * Format price with null handling.
 * 
 * @param price - Price value or null
 * @returns Formatted string or 'N/A'
 */
export function formatPriceOrNA(price: number | null | undefined): string {
  if (price === null || price === undefined) return 'N/A';
  return formatPrice(price);
}
