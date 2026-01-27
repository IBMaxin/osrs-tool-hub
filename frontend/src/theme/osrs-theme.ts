import { createTheme, MantineColorsTuple } from '@mantine/core';

// OSRS-inspired color palette
const osrsBrown: MantineColorsTuple = [
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

const osrsGold: MantineColorsTuple = [
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

const osrsOrange: MantineColorsTuple = [
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

const osrsRed: MantineColorsTuple = [
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

const osrsGreen: MantineColorsTuple = [
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

export const osrsTheme = createTheme({
  primaryColor: 'osrsBrown',
  colors: {
    osrsBrown,
    osrsGold,
    osrsOrange,
    osrsRed,
    osrsGreen,
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
  
  components: {
    AppShell: {
      styles: {
        root: {
          backgroundColor: '#1A0F08',
        },
        navbar: {
          backgroundColor: '#2B1B0E',
          borderRight: '3px solid #4A360C',
        },
        main: {
          backgroundColor: '#1A0F08',
        },
      },
    },
    
    NavLink: {
      styles: {
        root: {
          color: '#D4AF37',
          fontWeight: 600,
          padding: '12px 16px',
          borderRadius: '4px',
          transition: 'all 0.2s ease',
          '&:hover': {
            backgroundColor: '#4A360C',
            color: '#FFE799',
          },
          '&[data-active]': {
            backgroundColor: '#8B6914',
            color: '#FFF9E6',
            borderLeft: '4px solid #D4AF37',
          },
        },
      },
    },
    
    Card: {
      styles: {
        root: {
          backgroundColor: '#2B1B0E',
          border: '2px solid #4A360C',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.5)',
          transition: 'all 0.2s ease',
          '&:hover': {
            borderColor: '#8B6914',
            boxShadow: '0 4px 12px rgba(212, 175, 55, 0.3)',
          },
        },
      },
    },
    
    Button: {
      styles: {
        root: {
          fontWeight: 700,
          textShadow: '1px 1px 2px rgba(0, 0, 0, 0.8)',
          transition: 'all 0.2s ease',
          '&:hover': {
            transform: 'translateY(-1px)',
            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.4)',
          },
        },
      },
      defaultProps: {
        color: 'osrsOrange',
      },
    },
    
    Modal: {
      styles: {
        content: {
          backgroundColor: '#2B1B0E',
          border: '3px solid #8B6914',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.8)',
        },
        header: {
          backgroundColor: '#4A360C',
          borderBottom: '2px solid #8B6914',
          color: '#D4AF37',
        },
        title: {
          color: '#FFE799',
          fontWeight: 700,
          fontSize: '20px',
        },
      },
    },
    
    Badge: {
      styles: {
        root: {
          fontWeight: 700,
          textTransform: 'uppercase',
          letterSpacing: '0.5px',
        },
      },
    },
    
    Text: {
      styles: {
        root: {
          color: '#E8D4BB',
        },
      },
    },
    
    Title: {
      styles: {
        root: {
          color: '#FFE799',
        },
      },
    },
  },
});
