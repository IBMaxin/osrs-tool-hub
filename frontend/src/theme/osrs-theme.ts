import { createTheme } from '@mantine/core';
import {
  osrsBrown,
  osrsGold,
  osrsOrange,
  osrsRed,
  osrsGreen,
  statusColors,
} from './osrs-colors';
import { osrsComponentOverrides } from './osrs-components';

export { statusColors };

export const osrsTheme = createTheme({
  primaryColor: 'osrsBrown',
  colors: {
    osrsBrown,
    osrsGold,
    osrsOrange,
    osrsRed,
    osrsGreen,
    profit: osrsGreen,
    loss: osrsRed,
    warning: osrsOrange,
    info: osrsGold,
    neutral: osrsBrown,
  },
  
  // Standardized spacing scale (4px base unit)
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
  },
  
  // Border radius scale
  radius: {
    xs: '2px',
    sm: '4px',
    md: '6px',
    lg: '8px',
    xl: '12px',
  },
  
  // Typography
  fontFamily: '"Trebuchet MS", "Lucida Grande", Tahoma, sans-serif',
  fontFamilyMonospace: 'Consolas, Monaco, "Courier New", monospace',
  lineHeights: {
    xs: '1.3',
    sm: '1.4',
    md: '1.5',
    lg: '1.6',
    xl: '1.7',
  },
  fontSizes: {
    xs: '12px',
    sm: '14px',
    md: '16px',
    lg: '18px',
    xl: '20px',
  },
  
  headings: {
    fontFamily: '"Trebuchet MS", "Lucida Grande", Tahoma, sans-serif',
    fontWeight: '700',
    sizes: {
      h1: { fontSize: '32px', lineHeight: '1.3', fontWeight: '700' },
      h2: { fontSize: '26px', lineHeight: '1.3', fontWeight: '700' },
      h3: { fontSize: '22px', lineHeight: '1.4', fontWeight: '600' },
      h4: { fontSize: '18px', lineHeight: '1.4', fontWeight: '600' },
      h5: { fontSize: '16px', lineHeight: '1.5', fontWeight: '600' },
      h6: { fontSize: '14px', lineHeight: '1.5', fontWeight: '600' },
    },
  },
  
  defaultRadius: 'md',
  
  // Enhanced shadows for better depth perception
  shadows: {
    xs: '0 1px 2px rgba(0, 0, 0, 0.3)',
    sm: '0 2px 4px rgba(0, 0, 0, 0.35)',
    md: '0 4px 8px rgba(0, 0, 0, 0.4)',
    lg: '0 8px 16px rgba(0, 0, 0, 0.45)',
    xl: '0 12px 24px rgba(0, 0, 0, 0.5)',
  },
  
  components: osrsComponentOverrides,

  other: {
    MantineReactTable: {
      baseBackgroundColor: '#2B1B0E',
      selectedRowBackgroundColor: '#4A360C',
    },
  },
});
