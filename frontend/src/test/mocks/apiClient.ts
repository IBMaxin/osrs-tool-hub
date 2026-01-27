/**
 * Mock API client for testing
 * Provides mock implementations of API calls
 */

import { vi } from 'vitest'
import type { AxiosInstance } from 'axios'

export const mockApiClient = {
  get: vi.fn(),
  post: vi.fn(),
  put: vi.fn(),
  delete: vi.fn(),
  patch: vi.fn(),
} as unknown as AxiosInstance

export const mockFlippingApi = {
  getOpportunities: vi.fn(),
}

export const mockSlayerApi = {
  getMasters: vi.fn(),
  getTasks: vi.fn(),
  getAdvice: vi.fn(),
}

export const mockGearApi = {
  getProgression: vi.fn(),
  getWikiProgression: vi.fn(),
}
