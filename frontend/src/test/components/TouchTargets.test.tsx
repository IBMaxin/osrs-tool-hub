import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { MantineProvider, Button, Select, TextInput, Checkbox, Radio, ActionIcon } from '@mantine/core';
import { IconX } from '@tabler/icons-react';
import { osrsTheme } from '../../theme/osrs-theme';

const renderWithTheme = (ui: React.ReactElement) => {
  return render(<MantineProvider theme={osrsTheme}>{ui}</MantineProvider>);
};

describe('Touch Target Sizes', () => {
  const MINIMUM_SIZE = 44; // 44px minimum for WCAG AA

  it('Button meets minimum touch target size', () => {
    renderWithTheme(<Button>Click me</Button>);
    const button = screen.getByRole('button');
    
    const styles = window.getComputedStyle(button);
    const minHeight = parseInt(styles.minHeight);
    const minWidth = parseInt(styles.minWidth);
    
    expect(minHeight).toBeGreaterThanOrEqual(MINIMUM_SIZE);
    expect(minWidth).toBeGreaterThanOrEqual(MINIMUM_SIZE);
  });

  it('Select meets minimum touch target size', () => {
    const { container } = renderWithTheme(
      <Select
        label="Choose"
        data={[{ value: '1', label: 'Option 1' }]}
      />
    );
    
    const input = container.querySelector('input');
    expect(input).toBeTruthy();
    
    if (input) {
      const styles = window.getComputedStyle(input);
      const minHeight = parseInt(styles.minHeight);
      expect(minHeight).toBeGreaterThanOrEqual(MINIMUM_SIZE);
    }
  });

  it('TextInput meets minimum touch target size', () => {
    renderWithTheme(<TextInput label="Name" />);
    
    const input = screen.getByRole('textbox');
    const styles = window.getComputedStyle(input);
    const minHeight = parseInt(styles.minHeight);
    
    expect(minHeight).toBeGreaterThanOrEqual(MINIMUM_SIZE);
  });

  it('Checkbox container meets minimum touch target size', () => {
    renderWithTheme(<Checkbox label="Accept terms" />);
    
    const checkbox = screen.getByRole('checkbox');
    // Check the parent container
    const body = checkbox.closest('.mantine-Checkbox-body');
    
    if (body) {
      const styles = window.getComputedStyle(body);
      const minHeight = parseInt(styles.minHeight);
      expect(minHeight).toBeGreaterThanOrEqual(MINIMUM_SIZE);
    }
  });

  it('Radio container meets minimum touch target size', () => {
    renderWithTheme(
      <Radio.Group>
        <Radio value="1" label="Option 1" />
      </Radio.Group>
    );
    
    const radio = screen.getByRole('radio');
    // Check the parent container
    const body = radio.closest('.mantine-Radio-body');
    
    if (body) {
      const styles = window.getComputedStyle(body);
      const minHeight = parseInt(styles.minHeight);
      expect(minHeight).toBeGreaterThanOrEqual(MINIMUM_SIZE);
    }
  });

  it('ActionIcon meets minimum touch target size', () => {
    renderWithTheme(
      <ActionIcon aria-label="Close">
        <IconX />
      </ActionIcon>
    );
    
    const button = screen.getByRole('button', { name: 'Close' });
    const styles = window.getComputedStyle(button);
    const minHeight = parseInt(styles.minHeight);
    const minWidth = parseInt(styles.minWidth);
    
    expect(minHeight).toBeGreaterThanOrEqual(MINIMUM_SIZE);
    expect(minWidth).toBeGreaterThanOrEqual(MINIMUM_SIZE);
  });
});
