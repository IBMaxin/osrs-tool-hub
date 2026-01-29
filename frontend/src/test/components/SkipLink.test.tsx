import { render, screen } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';
import { describe, it, expect, beforeEach } from 'vitest';
import { SkipLink } from '../../lib/components/SkipLink';
import { MantineProvider } from '@mantine/core';

const renderWithProviders = (ui: React.ReactElement) => {
  return render(<MantineProvider>{ui}</MantineProvider>);
};

describe('SkipLink', () => {
  beforeEach(() => {
    // Create a target element
    const target = document.createElement('div');
    target.id = 'main-content';
    target.tabIndex = -1;
    document.body.appendChild(target);
  });

  it('renders with correct text', () => {
    renderWithProviders(<SkipLink targetId="main-content">Skip to content</SkipLink>);
    expect(screen.getByText('Skip to content')).toBeInTheDocument();
  });

  it('has correct href attribute', () => {
    renderWithProviders(<SkipLink targetId="main-content">Skip to content</SkipLink>);
    const link = screen.getByText('Skip to content');
    expect(link).toHaveAttribute('href', '#main-content');
  });

  it('is visually hidden by default', () => {
    renderWithProviders(<SkipLink targetId="main-content">Skip to content</SkipLink>);
    const link = screen.getByText('Skip to content');
    expect(link).toHaveStyle({ position: 'absolute', left: '-9999px' });
  });

  it('focuses and scrolls to target when clicked', async () => {
    const user = userEvent.setup();
    renderWithProviders(<SkipLink targetId="main-content">Skip to content</SkipLink>);
    
    const link = screen.getByText('Skip to content');
    const target = document.getElementById('main-content');
    
    await user.click(link);
    
    expect(target).toHaveFocus();
  });

  it('prevents default link behavior', async () => {
    const user = userEvent.setup();
    renderWithProviders(<SkipLink targetId="main-content">Skip to content</SkipLink>);
    
    const link = screen.getByText('Skip to content');
    await user.click(link);
    
    // Should not navigate (URL should not change)
    expect(window.location.hash).toBe('');
  });
});
