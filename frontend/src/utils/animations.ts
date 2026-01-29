/**
 * Animation utilities for consistent transitions
 * Provides reusable animation styles and helpers
 */

/**
 * Standard transition durations (in ms)
 */
export const TRANSITION = {
  fast: 150,
  normal: 200,
  slow: 300,
} as const;

/**
 * Standard easing functions
 */
export const EASING = {
  linear: 'linear',
  ease: 'ease',
  easeIn: 'ease-in',
  easeOut: 'ease-out',
  easeInOut: 'ease-in-out',
  spring: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
} as const;

/**
 * Standard card hover animation styles
 */
export const cardHoverStyles = {
  transition: `transform ${TRANSITION.normal}ms ${EASING.easeOut}, box-shadow ${TRANSITION.normal}ms ${EASING.easeOut}`,
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
 * Subtle card hover (less dramatic)
 */
export const subtleHoverStyles = {
  transition: `transform ${TRANSITION.fast}ms ${EASING.easeOut}, opacity ${TRANSITION.fast}ms ${EASING.easeOut}`,
  cursor: 'pointer',
  onMouseEnter: (e: React.MouseEvent<HTMLElement>) => {
    e.currentTarget.style.transform = 'translateY(-2px)';
    e.currentTarget.style.opacity = '0.9';
  },
  onMouseLeave: (e: React.MouseEvent<HTMLElement>) => {
    e.currentTarget.style.transform = 'translateY(0)';
    e.currentTarget.style.opacity = '1';
  },
};

/**
 * Scale on hover animation
 */
export const scaleHoverStyles = {
  transition: `transform ${TRANSITION.normal}ms ${EASING.spring}`,
  cursor: 'pointer',
  onMouseEnter: (e: React.MouseEvent<HTMLElement>) => {
    e.currentTarget.style.transform = 'scale(1.05)';
  },
  onMouseLeave: (e: React.MouseEvent<HTMLElement>) => {
    e.currentTarget.style.transform = 'scale(1)';
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

/**
 * Fade in with slide animation
 */
export const fadeInUpStyles = (delay: number = 0) => ({
  animation: `fadeInUp 0.4s ${EASING.easeOut} ${delay}ms forwards`,
  opacity: 0,
  '@keyframes fadeInUp': {
    from: {
      opacity: 0,
      transform: 'translateY(20px)',
    },
    to: {
      opacity: 1,
      transform: 'translateY(0)',
    },
  },
});

/**
 * Slide in from right
 */
export const slideInRightStyles = (delay: number = 0) => ({
  animation: `slideInRight 0.4s ${EASING.easeOut} ${delay}ms forwards`,
  opacity: 0,
  '@keyframes slideInRight': {
    from: {
      opacity: 0,
      transform: 'translateX(20px)',
    },
    to: {
      opacity: 1,
      transform: 'translateX(0)',
    },
  },
});

/**
 * Pulse animation (for attention)
 */
export const pulseStyles = {
  animation: 'pulse 2s ease-in-out infinite',
  '@keyframes pulse': {
    '0%, 100%': {
      opacity: 1,
    },
    '50%': {
      opacity: 0.7,
    },
  },
};

/**
 * Shimmer effect for loading states
 */
export const shimmerStyles = {
  background: 'linear-gradient(90deg, #2B1B0E 0%, #4A360C 50%, #2B1B0E 100%)',
  backgroundSize: '200% 100%',
  animation: 'shimmer 1.5s ease-in-out infinite',
  '@keyframes shimmer': {
    '0%': {
      backgroundPosition: '200% 0',
    },
    '100%': {
      backgroundPosition: '-200% 0',
    },
  },
};

/**
 * Rotate animation
 */
export const rotateStyles = {
  animation: 'rotate 1s linear infinite',
  '@keyframes rotate': {
    from: {
      transform: 'rotate(0deg)',
    },
    to: {
      transform: 'rotate(360deg)',
    },
  },
};

/**
 * Bounce animation (for notifications/badges)
 */
export const bounceStyles = {
  animation: 'bounce 0.6s ease-in-out',
  '@keyframes bounce': {
    '0%, 100%': {
      transform: 'translateY(0)',
    },
    '50%': {
      transform: 'translateY(-10px)',
    },
  },
};
