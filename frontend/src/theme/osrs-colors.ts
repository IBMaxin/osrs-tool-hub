import { MantineColorsTuple } from '@mantine/core';

// OSRS-inspired color palette
export const osrsBrown: MantineColorsTuple = [
  '#F5E6D3',
  '#E8D4BB',
  '#D4B896',
  '#C09D71',
  '#A67C52',
  '#8B6914', // Primary brown
  '#6B4E11',
  '#4A360C',
  '#2B1B0E',
  '#1A0F08',
];

export const osrsGold: MantineColorsTuple = [
  '#FFF9E6',
  '#FFF0CC',
  '#FFE799',
  '#FFD966',
  '#FFCC33',
  '#D4AF37', // Primary gold
  '#B8982F',
  '#9C8127',
  '#806A1F',
  '#645317',
];

export const osrsOrange: MantineColorsTuple = [
  '#FFF4E6',
  '#FFE8CC',
  '#FFD699',
  '#FFC466',
  '#FFB133',
  '#FF981F', // OSRS orange
  '#E6891C',
  '#CC7A19',
  '#B36B16',
  '#995C13',
];

export const osrsRed: MantineColorsTuple = [
  '#FFE6E6',
  '#FFCCCC',
  '#FF9999',
  '#FF6666',
  '#FF3333',
  '#DC143C', // Crimson red
  '#C61235',
  '#B0102E',
  '#9A0E27',
  '#840C20',
];

export const osrsGreen: MantineColorsTuple = [
  '#E6F4EA',
  '#CCEAD5',
  '#99D5AB',
  '#66C081',
  '#33AB57',
  '#228B22', // Forest green
  '#1E7A1E',
  '#1A691A',
  '#165816',
  '#124712',
];

/** Semantic status colors (profit/loss/warning/info/neutral) for WCAG AA contrast on #1A0F08 */
export const statusColors = {
  profit: '#228B22',
  loss: '#DC143C',
  warning: '#FF981F',
  info: '#D4AF37',
  neutral: '#8B6914',
} as const;
