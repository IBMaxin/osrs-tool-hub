/**
 * Skip link component for keyboard navigation accessibility
 * Allows users to skip directly to main content
 */
import { Box } from '@mantine/core';

interface SkipLinkProps {
  /** Target element ID to skip to */
  targetId: string;
  /** Link text */
  children: string;
}

/**
 * SkipLink provides keyboard users a way to skip navigation and go directly to main content.
 * The link is visually hidden until focused via keyboard navigation.
 */
export function SkipLink({ targetId, children }: SkipLinkProps) {
  const handleClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
    e.preventDefault();
    const target = document.getElementById(targetId);
    if (target) {
      target.focus();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <Box
      component="a"
      href={`#${targetId}`}
      onClick={handleClick}
      style={{
        position: 'absolute',
        left: '-9999px',
        zIndex: 9999,
        padding: '8px 16px',
        backgroundColor: '#D4AF37',
        color: '#1A0F08',
        fontWeight: 700,
        textDecoration: 'none',
        borderRadius: '4px',
        top: '8px',
      }}
      onFocus={(e) => {
        e.currentTarget.style.left = '8px';
      }}
      onBlur={(e) => {
        e.currentTarget.style.left = '-9999px';
      }}
    >
      {children}
    </Box>
  );
}
