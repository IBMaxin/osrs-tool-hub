import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
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

describe('App Accessibility', () => {
  it('has skip link for keyboard navigation', () => {
    renderApp();
    expect(screen.getByText('Skip to main content')).toBeInTheDocument();
  });

  it('has accessible main navigation landmark', () => {
    renderApp();
    const nav = screen.getByRole('navigation', { name: /main navigation/i });
    expect(nav).toBeInTheDocument();
  });

  it('has accessible main content landmark', () => {
    renderApp();
    const main = screen.getByRole('main', { name: /main content/i });
    expect(main).toBeInTheDocument();
  });

  it('main content is focusable for skip link', () => {
    renderApp();
    const main = document.getElementById('main-content');
    expect(main).toBeInTheDocument();
    expect(main).toHaveAttribute('tabIndex', '-1');
  });

  it('navigation items have descriptive aria-labels', () => {
    renderApp();
    expect(screen.getByLabelText(/flipping tools/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/gear tools/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/slayer tools/i)).toBeInTheDocument();
  });

  it('navigation items have aria-expanded state', () => {
    renderApp();
    const flippingNav = screen.getByLabelText(/flipping tools/i);
    expect(flippingNav).toHaveAttribute('aria-expanded');
  });

  it('active navigation items have aria-current', () => {
    renderApp();
    // The default active tab is flipping/scanner
    const scannerLink = screen.getByLabelText(/flip scanner/i);
    expect(scannerLink).toHaveAttribute('aria-current', 'page');
  });

  it('badges have descriptive aria-labels', () => {
    renderApp();
    expect(screen.getByLabelText('New feature')).toBeInTheDocument();
    expect(screen.getByLabelText('Beta feature')).toBeInTheDocument();
  });
});
