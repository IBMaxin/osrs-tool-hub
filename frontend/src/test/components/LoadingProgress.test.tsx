import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { MantineProvider } from '@mantine/core';
import { LoadingProgress } from '../../lib/components/LoadingProgress';

const renderWithProviders = (ui: React.ReactElement) => {
  return render(<MantineProvider>{ui}</MantineProvider>);
};

describe('LoadingProgress', () => {
  it('renders progress bar', () => {
    const { container } = renderWithProviders(<LoadingProgress value={50} />);
    const progressBar = container.querySelector('[role="progressbar"]');
    expect(progressBar).toBeInTheDocument();
  });

  it('displays label when provided', () => {
    renderWithProviders(<LoadingProgress value={50} label="Loading..." />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('displays percentage when showPercentage is true', () => {
    renderWithProviders(<LoadingProgress value={75} showPercentage />);
    expect(screen.getByText('75%')).toBeInTheDocument();
  });

  it('has accessible ARIA attributes', () => {
    const { container } = renderWithProviders(
      <LoadingProgress value={60} label="Processing" />
    );
    
    const progressBar = container.querySelector('[role="progressbar"]');
    expect(progressBar).toHaveAttribute('aria-label', 'Processing');
    expect(progressBar).toHaveAttribute('aria-valuenow', '60');
    expect(progressBar).toHaveAttribute('aria-valuemin', '0');
    expect(progressBar).toHaveAttribute('aria-valuemax', '100');
  });

  it('rounds percentage value', () => {
    renderWithProviders(<LoadingProgress value={33.7} showPercentage />);
    expect(screen.getByText('34%')).toBeInTheDocument();
  });
});
