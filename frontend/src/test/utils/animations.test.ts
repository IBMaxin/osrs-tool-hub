import { describe, it, expect } from 'vitest';
import { getStaggerDelay, TRANSITION, EASING } from '../../utils/animations';

describe('animations utilities', () => {
  describe('getStaggerDelay', () => {
    it('calculates delay based on index', () => {
      expect(getStaggerDelay(0)).toBe(0);
      expect(getStaggerDelay(1)).toBe(50);
      expect(getStaggerDelay(2)).toBe(100);
      expect(getStaggerDelay(5)).toBe(250);
    });

    it('accepts custom base delay', () => {
      expect(getStaggerDelay(0, 100)).toBe(0);
      expect(getStaggerDelay(1, 100)).toBe(100);
      expect(getStaggerDelay(2, 100)).toBe(200);
    });
  });

  describe('TRANSITION constants', () => {
    it('has standard durations', () => {
      expect(TRANSITION.fast).toBe(150);
      expect(TRANSITION.normal).toBe(200);
      expect(TRANSITION.slow).toBe(300);
    });
  });

  describe('EASING constants', () => {
    it('has standard easing functions', () => {
      expect(EASING.linear).toBe('linear');
      expect(EASING.ease).toBe('ease');
      expect(EASING.easeIn).toBe('ease-in');
      expect(EASING.easeOut).toBe('ease-out');
      expect(EASING.easeInOut).toBe('ease-in-out');
      expect(EASING.spring).toBe('cubic-bezier(0.68, -0.55, 0.265, 1.55)');
    });
  });
});
