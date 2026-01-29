import type { MantineThemeOverride } from '@mantine/core';

export const osrsComponentOverrides: MantineThemeOverride['components'] = {
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
  
  Paper: {
    styles: {
      root: {
        backgroundColor: '#2B1B0E',
        border: '2px solid #4A360C',
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
    defaultProps: {
      color: 'neutral',
    },
    styles: {
      root: {
        fontWeight: 700,
        textTransform: 'uppercase',
        letterSpacing: '0.5px',
        '&[data-variant="light"][data-color="profit"]': {
          backgroundColor: 'rgba(34, 139, 34, 0.15)',
          color: '#228B22',
        },
        '&[data-variant="light"][data-color="loss"]': {
          backgroundColor: 'rgba(220, 20, 60, 0.15)',
          color: '#DC143C',
        },
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
  
  Slider: {
    styles: {
      root: {
        '--slider-color': '#D4AF37',
      },
      thumb: {
        backgroundColor: '#D4AF37',
        borderColor: '#FFE799',
      },
      track: {
        '&::before': {
          backgroundColor: '#D4AF37',
        },
      },
    },
  },

  MantineReactTable: {
    styles: {
      thead: {
        backgroundColor: '#4A360C',
        color: '#FFE799',
        fontWeight: 700,
      },
      tbodyTr: {
        '&:nth-of-type(odd)': {
          backgroundColor: '#2B1B0E',
        },
        '&:nth-of-type(even)': {
          backgroundColor: '#1A0F08',
        },
        '&:hover': {
          backgroundColor: '#4A360C',
        },
      },
      cell: {
        color: '#E8D4BB',
        padding: '8px 12px',
      },
      pagination: {
        backgroundColor: '#2B1B0E',
        color: '#D4AF37',
      },
    },
  },
};
