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
  
  fontFamily: '"Trebuchet MS", "Lucida Grande", Tahoma, sans-serif',
  fontFamilyMonospace: 'Consolas, Monaco, "Courier New", monospace',
  
  headings: {
    fontFamily: '"Trebuchet MS", "Lucida Grande", Tahoma, sans-serif',
    fontWeight: '700',
    sizes: {
      h1: { fontSize: '32px', lineHeight: '1.3' },
      h2: { fontSize: '26px', lineHeight: '1.3' },
      h3: { fontSize: '22px', lineHeight: '1.3' },
      h4: { fontSize: '18px', lineHeight: '1.4' },
      h5: { fontSize: '16px', lineHeight: '1.4' },
      h6: { fontSize: '14px', lineHeight: '1.4' },
    },
  },
  
  defaultRadius: 'md',
  
  shadows: {
    xs: '0 1px 3px rgba(0, 0, 0, 0.3)',
    sm: '0 1px 4px rgba(0, 0, 0, 0.4)',
    md: '0 2px 8px rgba(0, 0, 0, 0.5)',
    lg: '0 4px 16px rgba(0, 0, 0, 0.6)',
    xl: '0 8px 24px rgba(0, 0, 0, 0.7)',
  },
  
  components: osrsComponentOverrides,

  other: {
    MantineReactTable: {
      baseBackgroundColor: '#2B1B0E',
      selectedRowBackgroundColor: '#4A360C',
    },
  },
});
