import { render, screen } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';
import { describe, it, expect, beforeEach } from 'vitest';
import { MantineProvider } from '@mantine/core';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import App from '../../App';

const renderApp = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  return render(
    <QueryClientProvider client={queryClient}>
      <MantineProvider>
        <App />
      </MantineProvider>
    </QueryClientProvider>
  );
};

describe('App Mobile Navigation', () => {
  beforeEach(() => {
    // Reset viewport to mobile size
    Object.defineProperty(window, 'innerWidth', {
      writable: true,
      configurable: true,
      value: 375, // Mobile viewport
    });
  });

  it('renders burger menu button on mobile', () => {
    renderApp();
    const burger = screen.getByRole('button', { name: /toggle navigation menu/i });
    expect(burger).toBeInTheDocument();
  });

  it('burger button has accessible label', () => {
    renderApp();
    const burger = screen.getByRole('button', { name: /toggle navigation menu/i });
    expect(burger).toHaveAccessibleName('Toggle navigation menu');
  });

  it('renders app title in mobile header', () => {
    renderApp();
    expect(screen.getByText('OSRS Tool Hub')).toBeInTheDocument();
  });

  it('burger button can be clicked to toggle', async () => {
    const user = userEvent.setup();
    renderApp();
    
    const burger = screen.getByRole('button', { name: /toggle navigation menu/i });
    
    // Burger exists and can be clicked
    expect(burger).toBeInTheDocument();
    await user.click(burger);
    
    // Click again
    await user.click(burger);
    expect(burger).toBeInTheDocument();
  });

  it('navigation items remain accessible', async () => {
    const user = userEvent.setup();
    renderApp();
    
    const burger = screen.getByRole('button', { name: /toggle navigation menu/i });
    
    // Open drawer
    await user.click(burger);
    
    // Navigation items should be visible/accessible
    const gearNav = screen.getByLabelText(/gear tools/i);
    expect(gearNav).toBeInTheDocument();
    
    // Can click navigation item
    await user.click(gearNav);
    expect(gearNav).toBeInTheDocument();
  });

  it('keyboard accessible burger button', () => {
    renderApp();
    
    const burger = screen.getByRole('button', { name: /toggle navigation menu/i });
    
    // Focus the burger button
    burger.focus();
    expect(burger).toHaveFocus();
    
    // Can receive keyboard interaction
    expect(burger).toBeEnabled();
  });
});
