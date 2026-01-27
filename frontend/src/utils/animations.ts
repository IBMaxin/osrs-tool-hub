/**
 * Animation utilities for consistent transitions
 * Provides reusable animation styles and helpers
 */

/**
 * Standard card hover animation styles
 */
export const cardHoverStyles = {
  transition: 'transform 0.2s ease, box-shadow 0.2s ease',
  cursor: 'pointer',
  onMouseEnter: (e: React.MouseEvent<HTMLElement>) => {
    e.currentTarget.style.transform = 'translateY(-4px)';
    e.currentTarget.style.boxShadow = 'var(--mantine-shadow-md)';
  },
  onMouseLeave: (e: React.MouseEvent<HTMLElement>) => {
    e.currentTarget.style.transform = 'translateY(0)';
    e.currentTarget.style.boxShadow = 'var(--mantine-shadow-sm)';
  },
};

/**
 * Stagger animation delay calculator
 * Returns a delay based on index for staggered animations
 */
export function getStaggerDelay(index: number, baseDelay: number = 50): number {
  return index * baseDelay;
}

/**
 * Fade in animation styles
 */
export const fadeInStyles = {
  animation: 'fadeIn 0.3s ease-in',
  '@keyframes fadeIn': {
    from: { opacity: 0 },
    to: { opacity: 1 },
  },
};
